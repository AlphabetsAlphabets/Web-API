from flask import Flask
from flask_restful import Resource, reqparse, abort

from QA.key import Key
from QA.database import Database

# Errors
from mysql.connector.errors import ProgrammingError as TYPE_PROGRAMMING_ERROR
from mysql.connector.errors import DataError as TYPE_DATA_ERROR

class Update(Resource):
    """
    # Important
    This endpoint has not been used or maintained in a long time due to lack of use.

    Updates the MySQL database to reflect changes

    # Functions
    - __init__
    - post
    """
    def __init__(self):
        """Handles initialization, connects to database"""
        password = Database().getPassword()
        self.schema = "testing"

        parser = reqparse.RequestParser() 
        parser.add_argument("user", type=str, location="headers")
        parser.add_argument("key", type=str, location="headers")
        parser.add_argument("change", type=str)
        parser.add_argument("previous", type=str)

        self.parsed = parser.parse_args()

        user, key = self.parsed["user"], self.parsed["key"]

        """Verify user"""
        K = Key()
        K.verifyKey(user, key)

        try:
            self.conn, self.cursor = Database().connect("localhost", "root", password[0], self.schema)
        except Exception:
            self.conn, self.cursor = Database().connect("localhost", "root", password[1], self.schema)

    def post(self, salesperson):
        """Handles the POST request

        ---
        # Parameters
        ### salesperson
        The id of the salesperson 
        """
        self.cursor.execute(f"SELECT * FROM {self.schema}.trans WHERE salesperson = {salesperson}")
        res = self.cursor.fetchall()
        if len(res) == 0:
            abort(404, message = f"The entry with the id of {salesperson} doesnt not exist. Check if you had a typo.")

        self.change, self.prev = self.parsed["change"], self.parsed["previous"]
        try:
            sqlQuery = f"UPDATE {self.schema}.trans SET fbydate = '{self.change}' WHERE fbydate = '{self.prev}'"
            self.cursor.execute(sqlQuery)
            self.conn.commit()
        except (TYPE_DATA_ERROR, TYPE_PROGRAMMING_ERROR):
            abort(400, message = "Make sure your date format is in YYYY-MM-DD. i.e. 2021-01-01 not 2021-1-1")

        return {200: "New Entry Added"}