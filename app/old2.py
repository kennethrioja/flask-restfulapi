#!flask/bin/python
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
api = Api(app)


class UserAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("title", type=str, required=True, help="No task title provided", location="json")
        self.reqparse.add_argument("description", type=str, default='', location="json")
        super(UserAPI, self).__init__()

    def get(self, id):
        pass

    def post(self, id):
        pass


api.add_resource(UserAPI, '/users/<int:id>', endpoint='user')
