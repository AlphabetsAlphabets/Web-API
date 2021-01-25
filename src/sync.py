from flask import Flask # pip install flask
from flask_restful import Api, Resource, reqparse, abort # pip install flask-restful

import mysql.connector # pip install mysql-connector-python
import sqlite3 # local

import datetime, time

table = {"sqlite": "`testing`.`transaction`", "mysql": "`testing`.`trans`"}

class Sync(Resource):
    def __init__(self):
        """
        This method will initialise the connection to the mySql database, and the SQLite database. If the SQLite database does not exist when attempting to 
        connect to it - it will be created. Before it can be accessed. If the MySQL database does not exist. It will produce a mySqlDatabaseErrorNotFound Exception.
        But the api will continue to work, without crashing.
        """
        self.connectToDatabase()
        """
        Makes the POST request accept two arguments: salesperson, and key.
        """
        self.args = reqparse.RequestParser()
        self.args.add_argument("salesperson", type=str)

    def connectToDatabase(self):
        host = ["localhost", "192.168.1.165"]
        user = ["root", "testuser123"]
        database = ["testing", "testing"]
        out = 0
        with open("D:\\python\\Web API\\src\\files\\sql.txt") as f:
            password = f.readline()

        try:
            self.mySql = mysql.connector.connect( # Connect to main table
                host=host[out], 
                user=user[out],
                password=password,
                database=database[out]
                )
            """The host, user, password, and database variables will need to be changed accordingly to the host ip of the server, etc."""
            self.sqlCursor = self.mySql.cursor()


        except mysql.connector.errors.InterfaceError:
            abort(400, message="MySQL table not found.")
       
        try:
            sqliteDb = "D:\python\Web API\src\\testingDB.db" # Path to the local SQLite database stored in the device.
            self.liteCon = sqlite3.connect(sqliteDb) 
            self.liteCursor = self.liteCon.cursor()

        except sqlite3.OperationalError:
            abort(400, message="local SQLITE table not found. Try again, one should be created now.")

    def post(self, salesPerson=None):
        startTime = time.time()
        if salesPerson is None:
            """An argument parser is needed, in order to process the data that was passed in."""
            data = self.args.parse_args()
            salesPerson= data["salesperson"]

        """Stops the user from proceeding without the correct key, most likely subject to change."""
        valid = self.dataProcessing(salesPerson)

        # Updating the databases starts here
        columns = "`debtorcode`, `outstanding`, `amount`, `salesperson`, `counter`, `fbydate`"
        """Unpacks all the data from each column then inserts them into an insert statement that will be processed in the commitData() function."""
        commits = [f"INSERT INTO `testing`.`trans` ({columns}) VALUES ('{debtorCode}', '{outstanding}', '{amount}', '{salesPerson}', '{counter}', '{fbydate}')" for debtorCode, outstanding, amount, _, counter, fbydate in valid]
        self.commitData(commits, salesPerson)

        return [{201: f"Successfully synced. Time taken: {time.time() - startTime}"}]

    def dataProcessing(self, salesPerson):
        sqlString = f"SELECT * FROM `testing`.`trans` WHERE salesperson = '{salesPerson}' and fbydate >= CURDATE() - INTERVAL 3 day" # This causes an extra element in a tuple in a list
        self.sqlCursor.execute(sqlString) 
        resSql = self.sqlCursor.fetchall()

        liteString = f"SELECT * FROM `transaction` WHERE salesperson = '{salesPerson}' and fbydate = date('now', '-3 days')" 
        self.liteCursor.execute(liteString)
        resLite = self.liteCursor.fetchall()

        resSql= [list(columnData) for columnData in resSql]
        for container in resSql:
            for c, columnData in enumerate(container):
                if type(columnData) == datetime.date:
                    container[c] = columnData.strftime("%Y-%m-%d")

        if len(resLite) == 0:
            abort(409, message="Conflict: no new entries made.")

        valid = [lite for lite in resLite if lite not in resSql]
        
        return valid

    def commitData(self, commits, salesPerson):
        # Possible place to check if there is an available connection here
        for commit in commits:
            self.sqlCursor.execute(commit)
        self.mySql.commit()


        liteQuery = f"UPDATE `transaction` SET counter = '1' WHERE counter = '0' AND salesperson = '{salesPerson}' AND fbydate >= date('now', '-3 day')"
        self.liteCursor.execute(liteQuery)
        self.liteCon.commit()

        sqlQuery = f"UPDATE `testing`.`trans` SET counter = '1' WHERE counter = '0' AND salesperson = '{salesPerson}' AND fbydate >= CURDATE() - INTERVAL 3 day"
        self.sqlCursor.execute(sqlQuery)
        self.mySql.commit()

        self.updateCounter(salesperson=salesPerson)

    def updateCounter(self, salesperson):
        # and here
        """Updates all 1's to 2's signifying that the transactions are valid, and trustworthy."""
        liteQuery = f"UPDATE `transaction` SET counter = '2' WHERE counter = '1' AND salesperson = '{salesperson}' AND fbydate >= date('now', '-3 day')"

        self.liteCursor.execute(liteQuery)
        self.liteCon.commit()

        sqlQuery = f"UPDATE `testing`.`trans` SET counter = '2' WHERE counter = '1' AND salesperson = '{salesperson}' AND fbydate >= CURDATE() - INTERVAL 3 day"
        self.sqlCursor.execute(sqlQuery)
        self.mySql.commit()