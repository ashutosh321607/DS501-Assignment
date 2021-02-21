try:
    from flask import app,Flask
    from flask_restful import Resource, Api, reqparse
    import elasticsearch
    from elasticsearch import Elasticsearch
    import datetime
    import concurrent.futures
    import requests
    import json

except Exception as e:
    print("Modules Missing {}".format(e))


app = Flask(__name__)
api = Api(app)

#------------------------------------------------------------------------------------------------------------

NODE_NAME = 'netflix-index'
es = Elasticsearch()

#------------------------------------------------------------------------------------------------------------


class Movies(Resource):
    def __init__(self):
        self.query = parser.parse_args().get("query", None)
        # self.baseQuery = {
        #     "size": 0,
        #     "aggs": {
        #         "rating": {
        #             "terms": {
        #                 "field": "rating",
        #                 "size": 10
        #             }
        #         }
        #     },
        #     "query": {
        #         "bool": {
        #             "must": [],
        #             "filter": [],
        #             "should": [
        #                 {
        #                     "wildcard": {
        #                         "rating": {
        #                             "value": None
        #                         }
        #                     }
        #                 }
        #             ],
        #             "must_not": []
        #         }
        #     }
        # }
        self.baseQuery = {
            "size": 5,
            "query": {
                "bool": {
                    "must": [],
                    "filter": [],
                    "should": [
                        {
                            "wildcard": {
                                "title": {
                                    "value": None,
                                    "case_insensitive": True
                                }
                            }
                        }
                    ],
                    "must_not": []
                }
            }
        }

    def get(self):
        print("In")
        value = str(self.query).upper()
        self.baseQuery["query"]["bool"]["should"][0]["wildcard"]["title"]["value"] = "{}*".format(value)
        res = es.search(index=NODE_NAME, size=0, body=self.baseQuery)
        return res


parser = reqparse.RequestParser()
parser.add_argument("query", type=str, required=True, help="title parameter is Required ")

api.add_resource(Movies, '/query')


if __name__ == '__main__':
    app.run(debug=True)