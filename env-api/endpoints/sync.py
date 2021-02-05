import datetime
import sqlite3  # local
import time
from typing import Union

import mysql.connector  # pip install mysql-connector-python
from flask_restful import (Resource, abort,  # pip install flask-restful
                           reqparse)

from QA.database import Database
from QA.key import Key

table = {"sqlite": "`testing`.`transaction`", "mysql": "`testing`.`trans`"}

class Sync(Resource):
    def __init__(self):
        """
        This method will initialise the connection to the mySql database, and the SQLite database. If the SQLite database does not exist when attempting to 
        connect to it - it will be created. Before it can be accessed. If the MySQL database does not exist. It will produce a mySqlDatabaseErrorNotFound Exception.
        But the api will continue to work, without crashing.

        Makes the POST request accept two arguments: salesperson, and key.
        """

        try:
            # self.mySql, self.sqlCursor = Database().connect("localhost", "root", "YJH030412yjh_g", "testing")
            self.mySql, self.sqlCursor = Database().connect("localhost", "root", "8811967", "testing")
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

        Key().verifyKey(self.user, key)

        try:
            sqliteDb = "Files\\testingDB.db" # Path to the local SQLite database stored in the device.
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
        list(map(self.insertStatement, valid))
        self.updateCounter()

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

        valid = [lite for lite in resLite if lite not in resSql]
        
        return valid

    def updateCounter(self) -> None:
        liteQuery = f"UPDATE `transaction` SET counter = '1' WHERE counter = '0' AND salesperson = '{self.salesperson}' AND fbydate >= date('now', '-3 day')"
        self.liteCursor.execute(liteQuery)
        self.liteCon.commit()

        sqlQuery = f"UPDATE `testing`.`trans` SET counter = '1' WHERE counter = '0' AND salesperson = '{self.salesperson}' AND fbydate >= CURDATE() - INTERVAL 3 day"
        self.sqlCursor.execute(sqlQuery)
        self.mySql.commit()

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
    