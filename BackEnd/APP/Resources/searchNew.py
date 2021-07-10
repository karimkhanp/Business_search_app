from flask_restful import Resource, reqparse

# User-Defined Modules
from APP import Mongodb


# User-Defined Modules


# User-Defined Modules

class SearchNew(Resource):

    def _arguments(self, args):
        param = {}
        rows = args.get('limit')
        page = args.get('page')
        param['skip'] = rows * (page - 1) if page > 0 else 0
        param['limit'] = args.get('limit', 20)
        # Country filter
        country = args.get('Country')
        if isinstance(country, list):
            param["Country"] = {"$in": country}
        else:
            param["Country"] = country
        # city filter
        city = args.get("City")
        if city is not None and len(city) > 0:
            param["City"] = city

        return param

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)

        # page and limit being retrived from the url post method
        parser.add_argument(name='limit', location='args', type=int, required=True)
        parser.add_argument(name='page', location='args', type=int, required=True)
        parser.add_argument(name='country', location='json', type=list, dest='Country')
        parser.add_argument(name='city', location='json', type=str, dest='City')
        args = parser.parse_args(strict=True)

        query = self._arguments(args=args)
        response = list(Mongodb.find(query))
        result = dict()
        result['status'] = 'sucess'
        result['data'] = response
        result['count'] = len(response)
        return result
