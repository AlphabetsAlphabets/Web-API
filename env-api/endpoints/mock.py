import datetime

from PIL import Image

from flask_restful import Resource, reqparse, abort
from werkzeug.datastructures import FileStorage

class Mock(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument("first")
        parser.add_argument("second")

        self.parsed = parser.parse_args()

    def put(self, third):
        print("=="*20 + " NEW GET REQUEST " + "=="*20)
        print("- API: MOCK")
        print(f"- Current date and time: {datetime.datetime.now()}")

        first, second = self.parsed["first"], self.parsed["second"]
        print(f"\nfirst: {first}, second: {second}, third: {third}")
        print("=="*48)

       # C:\Users\YAP JIA HONG\Documents\coding\python\Web API\src\images 


        return {"message": "request successful", "code": 200}