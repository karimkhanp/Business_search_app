
url = open(file='APP/creds.txt', mode='r').read().strip()

class Config:
    SECRET_KEY = 'datainsight_db_api'
    MONGO_URL = url
    DB_NAME = 'test_db'
    COMPANY_COLLS_NAME = 'Company_Details_Colls'
    KEYWORD_COLLS = 'Keyword_Colls'
    COUNTRY_COLLS = 'test_col' #'Country_State_City_Colls'
    COUNTRY_GROUP_COLLS = 'Country_Group_Colls'