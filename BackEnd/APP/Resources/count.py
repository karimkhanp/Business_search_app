from flask_restful import Resource, reqparse
from bson.objectid import ObjectId

# User-Defined Modules
from APP import Mongodb
from APP.config import Config
from APP.Resources import projection


class Count(Resource):

    # Argument Parser
    def _arguments(self, args: dict):
        # print(args)
        # print()
        filters = list()
        match = list()
        # Country filter
        if args.get('Country') != None and args.get('Country') != "":
            if len(args.get('Country')) != 0:
                filters.append(
                    {'text': {'path': 'Country', 'query': args.get('Country'), 'score': {'boost': {'value': 5}}}})

        # State/Region filter
        if args.get('State/Region') != None and args.get('State/Region') != "":
            filters.append({'text': {'path': 'State/Region', 'query': args.get('State/Region')}})

        # City filter
        if args.get('City') != None and args.get('City') != "":
            filters.append({'text': {'path': 'City', 'query': args.get('City')}})

        # Category filter
        if args.get('category') != None and args.get('category') != "":
            filters.append({'text': {'path': 'Industry', 'query': args.get('category')}})
        if args.get('category') != None and args.get('category') != "":
            filters.append({'text': {'path': 'Industry', 'query': args.get('category')}})

        # jobtitle filter

        # Text Search Parameter
        path = ['JobTitle', 'AssetName', 'CampaignName', 'CompanyName', 'Industry']
        if args.get('search_type') == 'job':
            path = 'JobTitle'

        if (args.get('keyword') != ""):
            filters.append({'text': {'path': path, 'query': args.get('keyword')}})
        # print ("\nfilters : ",filters,"\n")
        # print(match)
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

    def _updatekeyword(self, keyword):
        pass

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(name='category', location='json', type=str)
        parser.add_argument(name='jobtitle', location='json', type=str)
        parser.add_argument(name='search_type', location='json', type=str, required=True)
        parser.add_argument(name='keyword', location='json', type=str, required=True)
        parser.add_argument(name='country', location='json', type=list, dest='Country')
        parser.add_argument(name='state', location='json', type=str, dest='State/Region')
        parser.add_argument(name='city', location='json', type=str, dest='City')

        parser.add_argument(name='employee', location='json', type=str)
        parser.add_argument(name='score', location='json', type=int)
        parser.add_argument(name='Max_Num_Of_Employees', location='json', type=int)
        parser.add_argument(name='Min_Num_Of_Employees', location='json', type=int)

        # page and limit being retrived from the url post method

        args = parser.parse_args(strict=True)
        try:
            filters, match = self._arguments(args=args)
            query = {
                'index': 'Text_Search_Index',
                'compound': {
                    'must': filters
                }
            }
            print(query)

            if args.get('score'):
                scoring, addon_score = self._scorecalculator(filters=query, score=args.get('score', 100))
            else:
                addon_score = 0

            if args.get('Max_Num_Of_Employees'):
                a = args.get('Max_Num_Of_Employees')
                query3 = {"MaxNumOfEmployees": {"$lte": a}}
            else:
                query3 = {}

            if args.get('Min_Num_Of_Employees'):
                b = args.get('Min_Num_Of_Employees')
                query2 = {"MinNumOfEmployees": {"$gte": b}}

            else:
                query2 = {}


            pipeline = [
                {'$search': query}, {'$match': query2}, {'$match': query3},
                { "$group": {"_id": None, "count": { "$sum": 1}}},
            { "$project": {"_id": 0}}

            ]

            response2 = Mongodb.Aggregation(
                pipeline=pipeline)


            for i in response2:
                print(i)

                count=i['count']



            output = list()

            result = dict()
            result['status'] = 'sucess'

            result['count'] = count
            return result, 200
        except Exception as e:
            result = dict()
            print("\nError!!!\n", e)
            result['status'] = 'failure'
            result['message'] = 'InternalError'
            result['description'] = str(e)
            return result, 500