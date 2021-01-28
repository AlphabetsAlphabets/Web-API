from flask import Flask # pip install flask
from flask_restful import Api, Resource, reqparse # pip install flask-restful

import mysql.connector # pip install mysql-connector-python

from QA.key import Key

class Update(Resource):
    def __init__(self, key):
        """
        The following code is PUT/POST request specific, and this is a guideline for creating future PUT/POST request functions.

        While constructing the url, and adding it as a resource. The parameters passed in during url construction.
        Will need to be added as a parameter in the respective function. Or there will be an error - indicating that the parameter is passed in, but not expected. 
        Which will crash the API. Once you add it as an accepted argument in the PUT function. You can just leave it, you dont actually need to do anything with it.
        """

        self.updateArgs = reqparse.RequestParser() 
        self.updateArgs.add_argument("data", type=str)
        self.updateArgs.add_argument("password", type=str)
        self.updateArgs.add_argument("id", type=str)

        data = self.updateArgs.parse_args()
        self.name, self.password, self.id = data["data"], data["password"], data["id"]

        """
        The actual argument parsing is done in the two lines as shown above. In this case when a post request is made, JSON data with the key of "data" is expected, and must be present.
        If for example you pass in two keys one "data", and another "data2". There will not be an error, however, when trying to access to value the "data2" is pointing to will result in and error,
        as that parameter is not expected.
        """
        self.key = key

    def startupAndVerify(id, password):
        """Verify user"""
        K = Key()
        key = K.verify(id, password)

        host = ["localhost", "192.168.1.165"]
        user = ["root", "testuser123"]
        database = ["testing", "testing"]
        out = 0
        
        with open("sql.txt") as f:
            password = f.readline()

        mydb = mysql.connector.connect(
            host=host[out], 
            user=user[out],
            password=password,
            database=database[out]
            )
        
        cursor = mydb.cursor()

        return mydb, cursor 
    def post(self):

        self.mydb, self.cursor = self.startupAndVerify(id, self.password)
        print("POST: in update")
        print("---"*20)

        sqlQuery = f"INSERT INTO `testing`.`apitest` (`names`) VALUES ('{self.name}')"

        self.cursor.execute(sqlQuery)
        self.mydb.commit()

        return {200: {"success": "New Entry Added"}}