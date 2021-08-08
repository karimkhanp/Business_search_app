from flask_restful import reqparse, Resource
import re
# User-defined Modules
from APP import Mongodb
from APP.Resources import projection

class Popular(Resource):

    def _arguments(self, args: dict):
        print(args)
        print()
        filters = list()
        match = list()
        # Country filter
        # if len(args.get('Country')) != 0:
        if args.get('Country') != None and args.get('Country') != "":
            filters.append(
                {'text': {'path': 'Country', 'query': args.get('Country')}})

        # Category filter
        if args.get('Industry') != None and args.get('Industry') != "":
            filters.append({'text': {'path': 'Industry', 'query': args.get('Industry')}})



        # Text Search Parameter
        path = ['JobTitle', 'AssetName', 'CampaignName', 'CompanyName', 'Industry']
        if args.get('search_type') == 'job':
            path = 'JobTitle'

        if (args.get('keyword') != ""):
            filters.append({'text': {'path': path, 'query': args.get('keyword')}})
        print("\nfilters : ", filters, "\n")
        print(match)
        return filters, match

    def _scorecalculator(self, filters: list, score: int):
        pipeline = [
            {'$search': filters},
            {'$limit': 1},
            {'$project': {'score': {'$meta': 'searchScore'}}}
        ]
        max_score = list(Mongodb.Aggregation(pipeline))[0].get('score')
        addon_score = 75 - max_score
        return addon_score

    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(name='search_type', location='args', type=str, required=True)
        parser.add_argument(name='keyword', location='args', type=str, required=True)
        parser.add_argument(name='Country', location='args', type=str )
        parser.add_argument(name='Industry', location='args', type=str)
        parser.add_argument(name='JobTitle', location='args', type=str)
        parser.add_argument(name='Max_Num_Of_Employees', location='args', type=int)
        parser.add_argument(name='Min_Num_Of_Employees', location='args', type=int)
        args = parser.parse_args(strict=True)
        try:
            # path = ['JobTitle', 'AssetName', 'CampaignName', 'CompanyName', 'Industry']
            # if args.get('search_type') == 'job':
            #     path = 'JobTitle'
            # query = {
            #     'index': 'Text_Search_Index',
            #     'text': {'path': path, 'query': args.get('keyword')}
            # }

            filters, match = self._arguments(args=args)
            query = {
                'index': 'Text_Search_Index',
                'compound': {
                    'must': filters
                }
            }



            # if args.get('Industry'):
            #     query2 = {
            #
            #         "Industry": {"$eq": args.get('Industry')}
            #     }
            # else:
            #     query2={}


            # if args.get('Country'):
            #     query3 = {
            #
            #         "Country": {"$eq": args.get('Country')}
            #     }
            # else:
            #     query3={}


            if args.get('Max_Num_Of_Employees'):
                a = args.get('Max_Num_Of_Employees')
                query4 = {"MaxNumOfEmployees": {"$lte": a}}
            else:
                query4 = {}


            if args.get('Min_Num_Of_Employees'):
                b = args.get('Min_Num_Of_Employees')
                query5 = {"MinNumOfEmployees": {"$gte": b}}

            else:
                query5 = {}



            pattern = r'[^A-Za-z ]'
            regex = re.compile(pattern)
            result1=[]
            if args.get('JobTitle'):
                result1 = regex.sub('', args.get('JobTitle')).split(' ')
                # print(result1)
            else:
                pass

            if args.get('score'):
                addon_score = self._scorecalculator(filters=query, score=args.get('score', 100))
            else:
                addon_score = self._scorecalculator(filters=query, score=100)


            pipeline = [
                {'$search': query},{'$match': query4}, {'$match': query5}, #{'$match': query2},{'$match': query3},
                {'$project': projection},
                {'$skip': 0},
                {'$limit': args.get('limit', 20)}
            ]
            response = Mongodb.Aggregation(
                pipeline = pipeline
            )
            output = list()
            for i in response:
                i['score'] = int(i['score'] + addon_score)

                if result1:
                    if any(ele in i['job_title'] for ele in result1):
                        # print("inside if 2")
                        print(any(ele in i['job_title'] for ele in result1))
                        output.append(i)
                    print(output)
                else:
                    output.append(i)
            result = dict()
            result['status'] = 'sucess'
            result['data'] = output
            return result, 200
        except Exception as e:
            result = dict()
            result['status'] = 'failure'
            result['message'] = 'Internal Error'
            result['description'] = str(e)
            return result, 500
