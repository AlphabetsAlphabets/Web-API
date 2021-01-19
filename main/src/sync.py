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
        """
        This metohd will initialise the connection to the mySql database, and the SQLite database. If the SQLite database does not exist when attempting to 
        connect to it - it will be created. Before it can be accessed.
        """
        self.mySql = mysql.connector.connect(
            host="localhost", 
            user="root",
            password="YJH030412yjh_g",
            database="testing"
            )
        """The host, user, password, and database variables will need to be changed accordingly to the host ip of the server, etc."""
        self.sqlCursor = self.mySql.cursor()
    
        self.liteCon = sqlite3.connect("main\src\SQLiteTutorialsDB.db")
        self.liteCursor = self.liteCon.cursor()

    def get(self):
        # TODO: Make the request dynamic, and change it to a PUT/POST request
        self.sqlCursor.execute("SELECT * FROM departments WHERE Salesperson = '2'") 
        resSql = self.sqlCursor.fetchall()
        self.liteCursor.execute("SELECT * FROM Departments WHERE Salesperson = '2'")
        resLite = self.liteCursor.fetchall()


        valid = [lite for lite in resLite if lite not in resSql]
        if len(valid) == 0:
            return {"message": "No changes made, as no new entries are made."}

        commits = [f"INSERT INTO `testing`.`departments` (`DepartmentId`, `DepartmentName`, `Salesperson`) VALUES ('{id}', '{depName}', '{salesperson}')" for id, depName, salesperson in valid]

        for commit in commits:
            self.sqlCursor.execute(commit)
        self.mySql.commit()

        return {200: "synced"}


