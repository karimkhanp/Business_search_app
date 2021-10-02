import re
from typing import Container
import pandas as pd
from pymongo import MongoClient

url = 'mongodb+srv://Api_Admin:DbApi_admin@cluster0.idnak.mongodb.net/?retryWrites=true&w=majority'
db_name = 'DataInsight_DB'
colls_name = 'Company_Details_Colls'

client = MongoClient(url)

database = client.get_database(name=db_name)

container = database.get_collection(name=colls_name)



pipeline = [
    {
        '$search': {
            'index': 'Text_Search_Index',
            'compound': {
                'filter': [
                    {
                        'text': {
                            'query': 'Manager',
                            'path': 'JobTitle'
                        }
                    },
                    {
                        'text': {
                            'query': ['Agriculture', 'Business Services'],
                            'path': 'Industry'
                        }
                    },
                    {
                        'range': {
                            'path': 'MinNumOfEmployees',
                            'gte': 250
                        }
                    },
                    {
                        'range': {
                            'path': 'MaxNumOfEmployees',
                            'lte': 500
                        }
                    },
                ]
            }
        }
    },
    # { $expr: { $gt: [{ $toDouble: "$price" }, 30]}}
    {
        '$match': {
            '$and': [
                { '$expr': { '$gte': [{ '$toDouble': "$minrevenue" }, 50000000]}},
                { '$expr': { '$lte': [{ '$toDouble': "$maxrevenue" }, 100000000]}},
                # {'minrevenue': {'$gte': ['50000000']}},
                # {'maxrevenue': {'$lte': '200000000'}}
            ]            
        }
    }
]

docs = container.aggregate(pipeline)


for doc in docs:
    print('{} - {} - {} - {} - {} - {}'.format(
            doc.get('JobTitle'),
            doc.get('MinNumOfEmployees'),
            doc.get('MaxNumOfEmployees'),
            doc.get('Industry'),
            doc.get('minrevenue'),
            doc.get('maxrevenue')
        )
    )