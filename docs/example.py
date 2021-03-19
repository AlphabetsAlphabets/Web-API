from flask_restful import Resource
from QA import Database

class Example(Resource):
    def __init__(self):
        """Connects to the MySQL database, provided all information is correct."""
        self.conn, self.cursor = Database.connect("localhost", "username", "password", "schema")

    def get(self, arg1, arg2):
        """accepts two arguments arg1, and arg2"""
        arg3 = arg1 + arg2 # Does processing with arg1 and arg2

        """
        In order to create a MySQL query and execute it, you must create create a `sqlString`
        then you must call `execute()` and pass the sqlString into the function.
        """

        sqlString = "SELECT * FROM schema.table"
        self.cursor.execute(sqlString)

        """In order to get the results from the sql query you must called `fetchall()` 
        which returns a list."""
        results = self.cursor.fetchall()[0]

        """returns must be JSON serializable, or it will throw an error. Functions in env-api/QA/database.py
        has functions that can convert non-serializable JSON objects to serializable JSON objects."""
        return {200: arg3, "results": results} 
