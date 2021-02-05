from flask_restful import Resource, reqparse, abort

from QA.database import Database
from QA.key import Key

import sqlite3

import os

# Error types
from sqlite3 import OperationalError as TYPE_OPERATIONAL_ERROR
from werkzeug.exceptions import ServiceUnavailable as TYPE_SERVICE_UNAVAILABLE

class Insert(Resource):
    def __init__(self):
        """Connects to MySQL database"""
        try:
            self.sqlConn, self.sqlCursor = Database().connect("localhost", "root", "YJH030412yjh_g", "testing")
        except TYPE_SERVICE_UNAVAILABLE:
            abort(503, message="Unable to connect to MySQL database. Due to incorrect credentials")

        """Connects to SQLITE3 database"""
        try:
            os.getcwd()
            os.chdir("..")
            PATH = os.getcwd() + "\\endpoints\\databases\\insertDb.db"
            PATH = "C:\\Users\\YAP JIA HONG\\Documents\\coding\\python\\Web API\\env-api\\endpoints\\databases\\insertDb.db"
            print(PATH)

            self.liteConn = sqlite3.connect(PATH)
            self.liteCursor = self.liteConn.cursor()

        except TYPE_OPERATIONAL_ERROR or FileNotFoundError:
            abort(400, message="local SQLITE table not found. Try again, one should be created now. If this persists ask the IT department for help.")

        args = reqparse.RequestParser()
        args.add_argument("key", type=str)
        args.add_argument("user", type=str)

        self.args = args.parse_args()

    def put(self):
        key, user = self.args["key"], self.args["user"]

        Key().verifyKey(user, key)

        return {"success": [key, user]}
