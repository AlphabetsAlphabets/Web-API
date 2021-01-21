from flask import Flask # pip install flask
from flask_restful import Api, Resource, reqparse # pip install flask-restful

import mysql.connector # pip install mysql-connector-python
import sqlite3 # local

"""
Sync class to use. Refer to api.py and at the line api.add_resource() will be it's trigger. Which will respond to 
a GET or a POST request.
"""

class Sync(Resource):
    def __init__(self):
        """
        This method will initialise the connection to the mySql database, and the SQLite database. If the SQLite database does not exist when attempting to 
        connect to it - it will be created. Before it can be accessed. If the MySQL database does not exist. It will produce a mySqlDatabaseErrorNotFound Exception.
        But the api will continue to work, without crashing.
        """
        self.mySql = mysql.connector.connect(
            host="localhost", 
            user="root",
            password="YJH030412yjh_g",
            database="testing"
            )
        """The host, user, password, and database variables will need to be changed accordingly to the host ip of the server, etc."""
        self.sqlCursor = self.mySql.cursor()
    
        sqliteDb = "D:\python\Web API\main\src\\testingDB.db" # Path to the local SQLite database stored in the device.
        self.liteCon = sqlite3.connect(sqliteDb) 
        self.liteCursor = self.liteCon.cursor()

        self.args = reqparse.RequestParser()
        self.args.add_argument("salesperson", type=str)

    def post(self):
        """An argument parser is needed, in order to process the data that was passed in."""
        data = self.args.parse_args()
        salesPerson = data["salesperson"]

        sqlString = f"SELECT * FROM `testing`.`trans` WHERE salesperson = '{salesPerson}'"
        self.sqlCursor.execute(sqlString) 
        resSql = self.sqlCursor.fetchall()

        liteString = f"SELECT * FROM `transaction` WHERE salesperson = '{salesPerson}'"
        self.liteCursor.execute(liteString)
        resLite = self.liteCursor.fetchall()

        if len(resSql) > 0:
            slice = len(resLite[0]) - len(resSql[0])
            valid = [lite[:-slice] for lite in resLite if lite[:-slice] not in resSql]

        else:
            """
            There is a possibility of the sql table to be empty and if that occurs it will by pass most checks and precautions made in place to make sure there are no
            duplicate sets or corrupted data. Before parsing.
            """
            slice = 2
            valid = [lite[:-2] for lite in resLite]
            commits = [f"INSERT INTO `testing`.`trans` (`debtorcode`, `outstanding`, `amount`, `salesperson`) VALUES ('{debtorCode}', '{outstanding}', '{amount}', '{salesPerson}')" for debtorCode, outstanding, amount, _ in valid]

        if len(valid) == 0:
            print("204: No changes")
            return {204: "No changes made, as there are no new entries."}

        liteQuery = f"UPDATE `transaction` SET counter = '1' WHERE counter = '0' AND salesperson = '{salesPerson}' AND fbydate >= date('now', '-1 day')"
        # SELECT * FROM `transaction` WHERE fbydate >= date('now') - date('now', '-1 day') 
        self.liteCursor.execute(liteQuery)
        self.liteCon.commit()
        
        commits = [f"INSERT INTO `testing`.`trans` (`debtorcode`, `outstanding`, `amount`, `salesperson`) VALUES ('{debtorCode}', '{outstanding}', '{amount}', '{salesPerson}')" for debtorCode, outstanding, amount, _ in valid]
        # INSERT INTO `testing`.`trans` (`debtorcode`, `outstanding`, `amount`, `salesperson`) VALUES ('3000-C020', '50', '900', '25');
        for commit in commits:
            self.sqlCursor.execute(commit)
        self.mySql.commit()

        print("successfully synced")
        return {200: "Successfully synced! Local database scheduled to be updated in 30 minutes."}

    def schedule(self, salesperson):
        print(f"Scheduled task for salesperson {salesperson}")
        liteQuery = f"UPDATE `transaction` SET counter = '2' WHERE counter = '1' AND salesperson = '{salesperson}' AND fbydate >= date('now', '-1 day')"

        self.liteCursor.execute(liteQuery)
        self.liteCon.commit()

        print("Task executed, and completed.")




