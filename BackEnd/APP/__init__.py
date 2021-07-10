from flask import Flask
from flask_cors import CORS
from flask_restful import Api

# User-Defined Modules
from APP.config import Config
from APP.Utils.db import MongoDB

app = Flask(import_name=__name__)
api = Api(app=app)
CORS(app=app)

app.config.from_object(obj=Config)

print('app.config: ', app.config)

# DB Initialisation
Mongodb = MongoDB(
    url = app.config['MONGO_URL'],
    db_name = app.config['DB_NAME'],
    colls_name = app.config['COMPANY_COLLS_NAME']
)

# Resources Path
from APP.Resources import Version
from APP.Resources.search import Search
from APP.Resources.search_num_employees import SearchNumEmployees
from APP.Resources.popular import Popular
from APP.Resources.autocomplete import AutoComplete
from APP.Resources.others import State, Cities, CountryGroups, Keywords, ListGroups, Country ,Category,JobTitle
from APP.Resources.searchNew import SearchNew
# Routing
api.add_resource(Version, '/')
api.add_resource(State, '/states')
api.add_resource(Cities, '/cities')
api.add_resource(Search, '/search')
api.add_resource(Country, '/country')
api.add_resource(Popular, '/popular')
api.add_resource(Keywords, '/keywords')
api.add_resource(Category, '/category')
api.add_resource(JobTitle, '/jobtitle')
api.add_resource(CountryGroups, '/group')
api.add_resource(ListGroups, '/listgroups')
api.add_resource(AutoComplete, '/autocomplete')
api.add_resource(SearchNumEmployees, '/search_num_employees')
api.add_resource(SearchNew, '/searchnew')