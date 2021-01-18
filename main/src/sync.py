import json # local
import requests
import numpy as np

from flask import Flask # pip install flask
from flask_restful import Api, Resource, reqparse # pip install flask-restful

import mysql.connector # pip install mysql-connector-python
import sqlite3

"""
Sync class to use. Refer to api.py and at the line api.add_resource() will be it's trigger. Which will respond to 
a GET or a POST request.
"""

class Sync(Resource):
    def __init__(self):
        self.mySql = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YJH030412yjh_g",
            database="testing"
            )
        self.sqlCursor = self.mySql.cursor()
    
        self.liteCon = sqlite3.connect("main\src\SQLiteTutorialsDB.db")
        self.liteCursor = self.liteCon.cursor()

    def get(self):
        self.sqlCursor.execute("SELECT * FROM departments WHERE salesperson = '1'")
        resSql = self.sqlCursor.fetchall()
        self.liteCursor.execute("SELECT * FROM Departments")
        resLite = self.liteCursor.fetchall()

        if len(resSql) == len(resLite):
            return {"message": "No changes."}

        resSql.sort(), resLite.sort()
        lenResSql = len(resSql)
        id, depName = resLite[lenResSql]

        sqlQuery = f"INSERT INTO `testing`.`departments` (`DepartmentId`, `DepartmentName`) VALUES ('{id}', '{depName}')"

        self.sqlCursor.execute(sqlQuery)
        self.mySql.commit()

        return {200: "synced"}


