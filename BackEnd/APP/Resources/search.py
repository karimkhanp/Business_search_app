import werkzeug
from flask_restful import Resource, reqparse
from io import StringIO

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
                    'query': [x.strip() for x in args.get('country').split(',')]
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
                    'query': [x.strip() for x in args.get('category').split(',')]
                }
            })

        if args['company_name'] or args['company_names_file']:
            dcn = {"CompanyName": {"$in": []}}
            if args['company_name']:
                cn = [x.strip() for x in args.get('company_name').split(',')]
                dcn["CompanyName"]["$in"].extend(cn)

            if args['company_names_file']:
                try:
                    cn = args['company_names_file'].readlines()
                    cn = [x.decode('utf-8').strip() for x in cn]
                    dcn["CompanyName"]["$in"].extend(cn)
                except:
                    raise Exception("Invalid Text file...")
            dcn["CompanyName"]["$in"] = list(set(dcn["CompanyName"]["$in"]))
            match.append(dcn)

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
        parser.add_argument(name='category', location='form', type=str)
        parser.add_argument(name='jobtitle', location='form', type=str)
        parser.add_argument(name='search_type', location='form', type=str, required=True)
        parser.add_argument(name='keyword', location='form', type=str, required=True)
        parser.add_argument(name='country', location='form', type=str)
        parser.add_argument(name='state', location='form', type=str, dest='State/Region')
        parser.add_argument(name='city', location='form', type=str, dest='City')
        parser.add_argument(name='company_name', location='form', type=str)

        parser.add_argument(name='employee', location='form', type=str)
        parser.add_argument(name='score', location='form', type=int)
        parser.add_argument(name='Max_Num_Of_Employees', location='form', type=int)
        parser.add_argument(name='Min_Num_Of_Employees', location='form', type=int)
        parser.add_argument(name='Max_Revenue', location='form', type=int)
        parser.add_argument(name='Min_Revenue', location='form', type=int)
        parser.add_argument(name='company_names_file', location='files', type=werkzeug.datastructures.FileStorage)

        # page and limit being retrived from the url post method
        parser.add_argument(name='limit', location='args', type=int, required=True)
        parser.add_argument(name='page', location='args', type=int, required=True)
        args = parser.parse_args(strict=True)
        # try:
        print(args)
        filters, match = self._arguments(args=args)
        print(filters)
        print(match)

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
        # except Exception as e:
        #     result = dict()
        #     print ("\nError!!!\n",e)
        #     result['status'] = 'failure'
        #     result['message'] = 'InternalError'
        #     result['description'] = str(e)
        #     return result, 500
