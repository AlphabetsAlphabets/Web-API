from typing import Union
from flask import Flask # pip install flask
from flask_restful import Api, Resource, reqparse, abort # pip install flask-restful

import mysql.connector # pip install mysql-connector-python
import sqlite3 # local

import datetime, time

from QA.key import Key
from QA.database import Database

table = {"sqlite": "`testing`.`transaction`", "mysql": "`testing`.`trans`"}

class Sync(Resource):
    def __init__(self):
        """
        This method will initialise the connection to the mySql database, and the SQLite database. If the SQLite database does not exist when attempting to 
        connect to it - it will be created. Before it can be accessed. If the MySQL database does not exist. It will produce a mySqlDatabaseErrorNotFound Exception.
        But the api will continue to work, without crashing.

        Makes the POST request accept two arguments: salesperson, and key.
        """

        o = 0
        """Setting up database connection"""
        host = ["localhost", "192.168.1.165"]
        user = ["root", "testuser123"]
        database = ["testing", "testing"]
        with open("D:\python\Web API\src\Files\sql.txt") as f:
            password = f.readlines()

        try:
            self.mySql, self.sqlCursor = Database().connect(host[o], user[o], database[o], password[o])
        except mysql.connector.errors.InterfaceError:
            abort(400, message="MySQL table not found.")
        
        self.args = reqparse.RequestParser()
        self.args.add_argument("key", type=str)
        self.args.add_argument("salesperson", type=str)
        self.args.add_argument("user", type=str)
        self.args.add_argument("password", type=str)
        self.args.add_argument("department", type=str)

        args = self.args.parse_args()
        key, self.salesperson, self.user, self.password, self.department = args["key"], args["salesperson"], args["user"], args["password"], args["department"]

        Key().verifyKey(key)

        try:
            sqliteDb = "D:\python\Web API\src\\files\\testingDB.db" # Path to the local SQLite database stored in the device.
            self.liteCon = sqlite3.connect(sqliteDb) 
            self.liteCursor = self.liteCon.cursor()

        except sqlite3.OperationalError:
            abort(400, message="local SQLITE table not found. Try again, one should be created now.")

    def post(self):
        """An argument parser is needed, in order to process the data that was passed in."""

        startTime = time.time()

        """Stops the user from proceeding without the correct key, most likely subject to change."""
        valid = self.dataProcessing(self.salesperson)
        # Updating the databases starts here
        # columns = "`debtorcode`, `outstanding`, `amount`, `salesperson`, `counter`, `fbydate`"
        # """Unpacks all the data from each column then inserts them into an insert statement that will be processed in the commitData() function."""
        # commits = [f"INSERT INTO `testing`.`trans` ({columns}) VALUES ('{debtorCode}', '{outstanding}', '{amount}', '{self.salesperson}', '{counter}', '{fbydate}')" for debtorCode, outstanding, amount, _, counter, fbydate in valid]
        self.updateCounter
        list(map(self.insertStatement, valid))

        return [{201: f"Successfully synced. Time taken: {time.time() - startTime}"}]

    def dataProcessing(self, salesPerson: Union[str, int]) -> list:
        sqlString = f"SELECT * FROM `testing`.`trans` WHERE salesperson = '{salesPerson}' and fbydate >= CURDATE() - INTERVAL 3 day" # This causes an extra element in a tuple in a list
        self.sqlCursor.execute(sqlString) 
        resSql = self.sqlCursor.fetchall()

        liteString = f"SELECT * FROM `transaction` WHERE salesperson = '{salesPerson}' and fbydate >= date('now', '-3 days')" 
        self.liteCursor.execute(liteString)
        resLite = self.liteCursor.fetchall()

        resSql = [list(columnData) for columnData in resSql]
        resLite = [list(columnData) for columnData in resLite]
        
        for container in resSql:
            for c, columnData in enumerate(container):
                if type(columnData) == datetime.date:
                    container[c] = columnData.strftime("%Y-%m-%d")

        liteSet = set(tuple(data) for data in resLite)
        sqlSet = set(tuple(data) for data in resSql)

        out = liteSet == sqlSet

        if len(resLite) == 0 or out:
            abort(409, message="Conflict: no new entries made.")

        valid = [lite for lite in resLite if lite not in resSql]
        
        return valid

    def updateCounter(self) -> None:
        liteQuery = f"UPDATE `transaction` SET counter = '1' WHERE counter = '0' AND salesperson = '{self.salesperson}' AND fbydate >= date('now', '-3 day')"
        self.liteCursor.execute(liteQuery)
        self.liteCon.commit()

        sqlQuery = f"UPDATE `testing`.`trans` SET counter = '1' WHERE counter = '0' AND salesperson = '{self.salesperson}' AND fbydate >= CURDATE() - INTERVAL 3 day"
        self.sqlCursor.execute(sqlQuery)
        self.mySql.commit()
        """Updates all 1's to 2's signifying that the transactions are valid, and trustworthy."""
        liteQuery = f"UPDATE `transaction` SET counter = '2' WHERE counter = '1' AND salesperson = '{self.salesperson}' AND fbydate >= date('now', '-3 day')"

        self.liteCursor.execute(liteQuery)
        self.liteCon.commit()

        sqlQuery = f"UPDATE `testing`.`trans` SET counter = '2' WHERE counter = '1' AND salesperson = '{self.salesperson}' AND fbydate >= CURDATE() - INTERVAL 3 day"
        self.sqlCursor.execute(sqlQuery)
        self.mySql.commit()

    def insertStatement(self, values: list) -> None:
        columns = "`debtorcode`, `outstanding`, `amount`, `salesperson`, `counter`, `fbydate`"
        """Unpacks all the data from each column then inserts them into an insert statement that will be processed in the commitData() function."""
        debtorCode, outstanding, amount, _, counter, fbydate = values
        sqlQuery = f"INSERT INTO `testing`.`trans` ({columns}) VALUES ('{debtorCode}', '{outstanding}', '{amount}', '{self.salesperson}', '{counter}', '{fbydate}')"

        self.sqlCursor.execute(sqlQuery)
        self.mySql.commit()
    