import sqlite3 # local

from flask import Flask # pip install flask
from flask_restful import Api, Resource, reqparse # pip install flask-restful

import mysql.connector # pip install mysql-connector-python

class Update(Resource):
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="192.168.1.165",
            user="testuser123",
            password="YJH030412yjh_g",
            database="testing"
            )
        
        self.cursor = self.mydb.cursor()
        
        self.updateArgs = reqparse.RequestParser()
        self.updateArgs.add_argument("data", type=str)

    def post(self):
        print("POST: in update")
        print("---"*20)

        data = self.updateArgs.parse_args()
        name = data["data"]

        sqlQuery = f"INSERT INTO `testing`.`apitest` (`names`) VALUES ('{name}')"

        self.cursor.execute(sqlQuery)
        self.mydb.commit()

        return {200: {"success": "New Entry Added"}}