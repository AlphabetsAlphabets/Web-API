from flask_restful import Resource, abort
from QA.database import Database

class Lookup(Resource):
    def __init__(self):
        o = 0
        """Setting up database connection"""
        host = ["localhost", "192.168.1.165"]
        user = ["root", "testuser123"]
        database = ["testing", "testing"]
        
        with open("D:\python\Web API\src\Files\sql.txt") as f:
            password = f.readlines()

        self.conn, self.cursor = Database().connect(host[o], user[o], password[o].strip("\n"), database[o])

    def get(self, table: str) -> dict:
        "/lookup/tablename"
        redirect = self.search(table)
        self.cursor.execute(redirect)
        res = self.cursor.fetchall()

        formatted = Database().keyValueParing(self.cursor, res)
        formatted = Database().keyValueParing()

        return {200: formatted}

    def search(self, table: str) -> str:
        sqlQuery = f"SELECT * FROM redirect WHERE table_name = '{table}'"
        self.cursor.execute(sqlQuery)
        res = self.cursor.fetchall()
        if len(res) == 0:
            abort(404, message="Table not found. Check if you have typed the table name correctly.")

        return res[0][1]
