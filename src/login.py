from flask import Flask # pip install flask
from flask_restful import abort, Resource, reqparse # pip install flask-restful

import mysql.connector # pip install mysql-connector-python

from QA.key import Key
from QA.encrypt import Hash

class Login(Resource):
    def __init__(self):
        """Get API key"""
        host = ["localhost", "192.168.1.165"]
        user = ["root", "testuser123"]
        database = ["testing", "testing"]

        out = 1 

        PATH = "D:\\python\\Web API\\src\\Files\\sql.txt"
        with open(PATH) as f:
            password = f.readline()

        self.tap = mysql.connector.connect( # Connecting to tsc_office.tap
            host=host[out], 
            user=user[out],
            password=password,
            database=database[out]
        )
        self.tapCursor = self.tap.cursor()

        self.args = reqparse.RequestParser()
        self.args.add_argument("user", type=str)
        self.args.add_argument("password", type=str)

        args = self.args.parse_args()
        self.user, self.password = args["user"], args["password"]

    def post(self):
        H = Hash(self.password)
        encrypted = H.encrypt()

        sqlString = f"SELECT * FROM tsc_office.tap WHERE fuser = '{self.user}' AND fpassword = '{encrypted}'"
        self.tapCursor.execute(sqlString)
        res = self.tapCursor.fetchall()

        if len(res) == 0:
            abort(406, message="Incorrect username or password.")

        fid = res[0][4] # level of access
        key = Key().verify(self.user, self.password)

        return [{200: {"fid": fid, "key": key}}]