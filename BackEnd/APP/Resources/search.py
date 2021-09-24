from flask_restful import Resource, reqparse, request
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import random
import os
import string
import time
import openpyxl
from pathlib import Path
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
        # print(args)
        # print()
        filters = list()
        match = list()
        # Country filter
        # if args.get('Country') != None and args.get('Country') != "":
        #     if len(args.get('Country')) != 0:
        #         filters.append({'text':{'path': 'Country', 'query':args.get('Country'), 'score': {'boost': {'value': 5}}}})

        
        # State/Region filter
        if args.get('State/Region') != None and args.get('State/Region') != "":
            filters.append({'text':{'path': 'State/Region', 'query':args.get('State/Region')}})

        # City filter
        if args.get('City') != None and args.get('City') != "":
            filters.append({'text':{'path': 'City', 'query':args.get('City')}})

        #Category filter
        # if args.get('category') != None and args.get('category') != "":
        #     filters.append({'text':{'path': 'Industry', 'query':args.get('category')}})
        # if args.get('category') != None and args.get('category') != "":
        #     filters.append({'text':{'path': 'Industry', 'query':args.get('category')}})

        #jobtitle filter


        # Text Search Parameter
        path = ['AssetName','JobTitle', 'CompanyName','Industry','CampaignName']
        if args.get('search_type') == 'job':
            path = 'JobTitle'

        if(args.get('keyword')!=""):
            filters.append({'text':{'path': path, 'query':args.get('keyword')}})
        # print ("\nfilters : ",filters,"\n")
        # print(match)
        return filters,match

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
            filters,match = self._arguments(args=args)
            query = {
                'index': 'Text_Search_Index',
                'compound': {
                    'must': filters
                }
            }
            # print(query)





            if args.get('score'):
                scoring, addon_score = self._scorecalculator(filters=query, score=args.get('score', 100))
            else:
                addon_score = 0
            rows = args.get('limit')
            page = args.get('page')

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

            if args.get('country'):
                b = args.get('country')
                print(b)
                query4 = {"Country": {"$in": b}}

            else:
                query4 = {}

            if args.get('Max_Revenue'):
                a = args.get('Max_Revenue')
                query5 = {"Max_Revenue": {"$lte": a}}
            else:
                query5 = {}

            if args.get('Min_Revenue'):
                b = args.get('Min_Revenue')
                query6 = {"Min_Revenue": {"$gte": b}}

            else:
                query6 = {}
            print(query4)

            str1 = args.get('category')

            list1 = str1.split(',')
            print(list1)

            if list1:
                b = list1
                print(b)
                query8 = {"Industry": {"$in": b}}

            else:
                query8 = {}

            if args.get('company_name'):
                b = args.get('company_name')
                print(b)
                query7 = {"CompanyName": {"$in": b}}
            elif 'file' in request.files:
                file = request.files['file']
                print(file)

                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    print(filename)
                    print(os.getcwd())

                    def get_random_string(length):
                        letters = string.ascii_lowercase
                        result_str = ''.join(random.choice(letters) for i in range(length))
                        print("Random string of length", length, "is:", result_str)
                        return result_str

                    dir = get_random_string(4)
                    path = os.getcwd()
                    full_path = path + '/' + dir
                    os.mkdir(full_path)
                    path1 = full_path
                    file.save(os.path.join(path1, filename))

                    # data_file1 = open(path1 + '/'+filename, "rb")
                    # your_matrix = pe.get_array(file_name=path1 + '/'+filename)
                    # print(your_matrix)

                    list1 = []
                    xlsx_file = Path('SimData', path1 + '/' + filename)
                    wb_obj = openpyxl.load_workbook(xlsx_file)
                    sheet = wb_obj.active
                    for row in sheet.iter_rows():
                        for cell in row:
                            a = cell.value
                            list1.append(a)
                    print(list1)
                    # data_file1.close()

                    if os.path.exists(path1):
                        time.sleep(30)
                        os.remove(path1 + "/" + filename)

                        os.rmdir(path1)
                    query7 = {"CompanyName": {"$in": list1}}
            else:
                query7 = {}




            pipeline = [
                {'$search': query},{'$match': query4}, {'$match': query3},{'$match': query2},{'$match': query5},{'$match': query6},{'$match': query7},{'$match': query8},
                {'$project': projection},

                # {'$match': {'employees': match}},    # not worth it takeing more than 2 minutes for backend filtering
                {'$skip': rows*(page-1) if page > 0 else 0},
                {'$limit': args.get('limit', 20)},

            ]
            # Update Keyword Collection for every Search
            Mongodb.Update(
                colls = Config.KEYWORD_COLLS,
                docs = {'keyword': args.get('keyword').strip().capitalize()},
                update = {'$inc': {'qty': 1}}
            )

            response = Mongodb.Aggregation(
                pipeline = pipeline
            )



            output = list()
            for i in response:
                # print("i",i)
                i['score'] = int(i['score'] * addon_score)
                output.append(i)
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
