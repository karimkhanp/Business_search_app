from flask_restful import Resource, reqparse


# User-Defined Modules
from APP import Mongodb
from APP.config import Config
from APP.Resources import projection


ALLOWED_EXTENSIONS = set(['xlsx'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Search(Resource):

    # Argument Parser    
    def _arguments(self, args: dict):
        filters = list()
        match = list()

        # Keyword Filters
        filters.append({
            'text': {
                'path': ['AssetName','JobTitle', 'CompanyName','Industry','CampaignName'],
                'query': args['keyword']
            }
        })

        if args.get('Max_Num_Of_Employees'):
            filters.append({
                'range': {
                    'path': 'MaxNumOfEmployees',
                    'lte': args.get('Max_Num_Of_Employees')
                }
            })

        if args.get('Min_Num_Of_Employees'):
            filters.append({
                'range': {
                    'path': 'MinNumOfEmployees',
                    'gte': args.get('Min_Num_Of_Employees') - 1
                }
            })
        
        if args['country']:
            filters.append({
                'text': {
                    'path': 'Country',
                    'query': args['country']
                }
            })

        if args.get('State/Region'):
            filters.append({
            'text': {
                'path': 'State/Region',
                'query': args['State/Region']
            }
        })

        if args.get('City'):
            filters.append({
                'text': {
                    'path': 'City',
                    'query': args.get('City')
                }
            })
        
        if args['category']:
            filters.append({
                'text': {
                    'path': 'Industry',
                    'query': args.get('category')
                }
            })

        if args['company_name']:
            match.append({
                "CompanyName": {"$in": args['company_name']}
            })

        # Employess
        if args['Min_Revenue']:
            match.append({ '$expr': { '$gte': ["$minrevenue", args['Min_Revenue']*1000000] }})

        if args['Max_Revenue']:
            match.append({ '$expr': { '$lte': ["$maxrevenue", args['Max_Revenue']*1000000] }})

        return filters, match


    def _scorecalculator(self, filters: list, score: int):
        pipeline = [
            {'$search': filters},
            {'$limit': 1},
            {'$project': {'score': {'$meta': 'searchScore'}}}
        ]
        response = list(Mongodb.Aggregation(pipeline))
        if len(response) != 0:
            max_score = response[0].get('score')
            scoring = max_score * (score / 75)
            addon_score = 75 / max_score
            return scoring, addon_score
        return 75, 75

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(name='category', location='json', type=list)
        parser.add_argument(name='jobtitle', location='json', type=str)
        parser.add_argument(name='search_type', location='json', type=str, required=True)
        parser.add_argument(name='keyword', location='json', type=str, required=True)
        parser.add_argument(name='country', location='json', type=list)
        parser.add_argument(name='state', location='json', type=str, dest='State/Region')
        parser.add_argument(name='city', location='json', type=str, dest='City')
        parser.add_argument(name='company_name', location='json', type=list)

        parser.add_argument(name='employee', location='json', type=str)
        parser.add_argument(name='score', location='json', type=int)
        parser.add_argument(name='Max_Num_Of_Employees', location='json', type=int)
        parser.add_argument(name='Min_Num_Of_Employees', location='json', type=int)
        parser.add_argument(name='Max_Revenue', location='json', type=int)
        parser.add_argument(name='Min_Revenue', location='json', type=int)

        #page and limit being retrived from the url post method
        parser.add_argument(name='limit', location='args', type=int, required=True)
        parser.add_argument(name='page', location='args', type=int, required=True)
        args = parser.parse_args(strict=True)
        try:
            # print(args)
            filters, match = self._arguments(args=args)
            # print(filters)

            query = {
                'index': 'Text_Search_Index',
                'compound': {
                    'filter': filters
                }
            }

            rows = args.get('limit')
            page = args.get('page')

            pipeline = [
                {'$search': query},
                {'$match': {} if not match else {'$and': match}},
                {'$project': projection},
                {'$skip': rows*(page-1) if page > 0 else 0},
                {'$limit': args.get('limit', 20)},

            ]

            # print('\n\n\n')
            # print(pipeline)
            # Update Keyword Collection for every Search
            Mongodb.Update(
                colls = Config.KEYWORD_COLLS,
                docs = {'keyword': args.get('keyword').strip().capitalize()},
                update = {'$inc': {'qty': 1}}
            )

            # print('pipeline: ', pipeline)

            response = Mongodb.Aggregation(
                pipeline = pipeline
            )
            output = list(response)

            result = dict()
            result['status'] = 'sucess'
            result['data'] = output
            result['count'] = len(output)
            return result, 200
        except Exception as e:
            result = dict()
            print ("\nError!!!\n",e)
            result['status'] = 'failure'
            result['message'] = 'InternalError'
            result['description'] = str(e)
            return result, 500
