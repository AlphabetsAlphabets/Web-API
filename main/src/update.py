import sqlite3 # local

from flask import Flask # pip install flask
from flask_restful import Api, Resource, reqparse # pip install flask-restful

import mysql.connector # pip install mysql-connector-python

class Update(Resource):
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="192.168.1.165", # These fields must be changed accordingly
            user="testuser123",
            password="YJH030412yjh_g",
            database="testing"
            )
        
        self.cursor = self.mydb.cursor()
        
        """
        The following code is PUT/POST request specific, until indicated by "ends here". And this is a guideline for creating future PUT request functions.

        While constructing the url, and adding it as a resource. The parameters passed in during url construction.
        Will need to be added as a parameter in the respective function. Or there will be an error - indicating that the parameter is passed in, but not expected. 
        Which will crash the API. Once you add it as an accepted argument in the PUT function. You can just leave it, you dont actually need to do anything with it.
        """

        self.updateArgs = reqparse.RequestParser() 
        self.updateArgs.add_argument("data", type=str)

        """
        The actual argument parsing is done in the two lines as shown above. In this case when a post request is made, JSON data with the key of "data" is expected, and must be present.
        If for example you pass in two keys one "data", and another "data2". There will not be an error, however, when trying to access to value the "data2" is pointing to will result in and error,
        as that parameter is not expected.
        """

    def post(self):
        print("POST: in update")
        print("---"*20)

        data = self.updateArgs.parse_args()
        name = data["data"]

        sqlQuery = f"INSERT INTO `testing`.`apitest` (`names`) VALUES ('{name}')"

        self.cursor.execute(sqlQuery)
        self.mydb.commit()

        return {200: {"success": "New Entry Added"}}