from flask import Flask # pip install flask
from flask_restful import Api, Resource, reqparse # pip install flask-restful

import mysql.connector # pip install mysql-connector-python
import sqlite3 # local

import asyncio

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

        sqlString = f"SELECT *, DATE_FORMAT(fbydate, \"%Y-%m-%d\") FROM `testing`.`trans` WHERE salesperson = '{salesPerson}'"
        self.sqlCursor.execute(sqlString) 
        resSql = self.sqlCursor.fetchall()

        liteString = f"SELECT * FROM `transaction` WHERE salesperson = '{salesPerson}'"
        self.liteCursor.execute(liteString)
        resLite = self.liteCursor.fetchall()

        resSql = list(resSql[0])

        del resSql[-2]
        print(resSql)
        print(resLite)

        valid = [lite for lite in resLite]
        
        print(valid)

        if len(valid) == 0:
            print("204: No changes")
            return [{204: "No changes made, as there are no new entries."}]

        liteQuery = f"UPDATE `transaction` SET counter = '1' WHERE counter = '0' AND salesperson = '{salesPerson}' AND fbydate >= date('now', '-1 day')"
        self.liteCursor.execute(liteQuery)
        self.liteCon.commit()

        columns = "`debtorcode`, `outstanding`, `amount`, `salesperson`, `counter`, `fbydate`"
        commits = [f"INSERT INTO `testing`.`trans` ({columns}) VALUES ('{debtorCode}', '{outstanding}', '{amount}', '{salesPerson}', '{counter}', '{fbydate}')" for debtorCode, outstanding, amount, _, counter, fbydate in valid]
        print(commits[0])
        print(len(commits))
        # INSERT INTO `testing`.`trans` (`debtorcode`, `outstanding`, `amount`, `salesperson`) VALUES ('3000-C020', '50', '900', '25');
        for commit in commits:
            self.sqlCursor.execute(commit)
        self.mySql.commit()

        self.rowCount(salesperson=salesPerson)        
        self.schedule(salesperson=salesPerson)

        print("successfully synced")
        return [{200: "Successfully synced."}]

    def schedule(self, salesperson):
        print(f"Scheduled task for salesperson {salesperson}")
        liteQuery = f"UPDATE `transaction` SET counter = '2' WHERE counter = '1' AND salesperson = '{salesperson}' AND fbydate >= date('now', '-1 day')"
        sqlQuery = f"UPDATE `testing`.`trans` SET counter = '2' WHERE counter = '1' AND salesperson = '{salesperson}' AND fbydate >= CURDATE()"

        self.liteCursor.execute(liteQuery)
        self.liteCon.commit()

        self.sqlCursor.execute(sqlQuery)
        self.mySql.commit()

        print("Task executed, and completed.")

    def rowCount(self, salesperson):
        sqlQuery = f"SELECT * FROM `testing`.`trans` WHERE salesperson = {salesperson} AND fbydate = CURDATE() AND counter = 1"
        liteQuery = f"SELECT * FROM `transaction` WHERE salesperson = {salesperson} and fbydate = date('now') AND counter = 1"

        self.sqlCursor.execute(sqlQuery)
        self.liteCursor.execute(liteQuery)

        resSql, resLite = self.sqlCursor.fetchall(), self.liteCursor.fetchall()
        if len(resSql) != len(resLite):
            return [{400: "Rejected"}]
        print("same length")




