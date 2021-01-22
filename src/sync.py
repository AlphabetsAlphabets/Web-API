from flask import Flask # pip install flask
from flask_restful import Api, Resource, reqparse # pip install flask-restful

import mysql.connector # pip install mysql-connector-python
import sqlite3 # local

import datetime, time
from key import Key # To key.py

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
        try:
            self.mySql = mysql.connector.connect(
                host="localhost", 
                user="root",
                password="YJH030412yjh_g",
                database="testing"
                )
            """The host, user, password, and database variables will need to be changed accordingly to the host ip of the server, etc."""
            self.sqlCursor = self.mySql.cursor()

        except mysql.connector.errors.InterfaceError:
            return [{400: {"message": "Connection to MySQL database failed."}}]
       
        try:
            sqliteDb = "D:\python\Web API\main\src\\testingDB.db" # Path to the local SQLite database stored in the device.
            self.liteCon = sqlite3.connect(sqliteDb) 
            self.liteCursor = self.liteCon.cursor()
        except sqlite3.OperationalError:
            return [{400: {"message": "The SQLite Table does not exist. A new one should be created, try again to confirm. If this error persists, contact the IT department."}}]

        """
        Makes the POST request accept two arguments: salesperson, and key.
        """
        self.args = reqparse.RequestParser()
        self.args.add_argument("salesperson", type=str)
        self.args.add_argument("key", type=str)


        self.again = True # This is for checking if the user needs to run another POST request.

    def post(self, salesPerson=None, key=None):
        startTime = time.time()
        if salesPerson is None:
            """An argument parser is needed, in order to process the data that was passed in."""
            data = self.args.parse_args()
            salesPerson, self.key = data["salesperson"], data["key"]

        print(self.key == "116111110103115971109910497110") 

        """Stops the user from proceeding without the correct key, most likely subject to change."""
        if self.key != Key().grabber():
            return [{400: {"message": "Incorrect key"}}]

        valid = self.dataProcessing(salesPerson)

        # Updating the databases starts here
        columns = "`debtorcode`, `outstanding`, `amount`, `salesperson`, `counter`, `fbydate`"
        """Unpacks all the data from each column then inserts them into an insert statement that will be processed in the commitData() function."""
        commits = [f"INSERT INTO `testing`.`trans` ({columns}) VALUES ('{debtorCode}', '{outstanding}', '{amount}', '{salesPerson}', '{counter}', '{fbydate}')" for debtorCode, outstanding, amount, _, counter, fbydate in valid]
        self.commitData(commits, salesPerson)

        return [{200: f"Successfully synced. Time taken: {time.time() - startTime}"}]

    def dataProcessing(self, salesPerson):
        sqlString = f"SELECT * FROM `testing`.`trans` WHERE salesperson = '{salesPerson}'" # This causes an extra element in a tuple in a list
        self.sqlCursor.execute(sqlString) 
        resSql = self.sqlCursor.fetchall()
        self.limit = len(resSql)

        liteString = f"SELECT * FROM `transaction` WHERE salesperson = '{salesPerson}'" 
        self.liteCursor.execute(liteString)
        resLite = self.liteCursor.fetchall()

        resSql= [list(columnData) for columnData in resSql]
        for container in resSql:
            for c, columnData in enumerate(container):
                if type(columnData) == datetime.date:
                    container[c] = columnData.strftime("%Y-%m-%d")

        valid = [lite for lite in resLite]
        
        if len(valid) == 0:
            return [{204: "No changes made, as there are no new entries."}]

        return valid

    def verify(self, salesperson):
        """SQL statements to filter out data, and then compare them against checks to verify their legitamacy."""
        sqlQuery = f"SELECT * FROM `testing`.`trans` WHERE salesperson = {salesperson} AND fbydate >= CURDATE() - INTERVAL 3 day AND counter = 1"
        liteQuery = f"SELECT * FROM `transaction` WHERE salesperson = {salesperson} AND fbydate >= date('now', '-3 day') AND counter = 1" 

        self.sqlCursor.execute(sqlQuery)
        self.liteCursor.execute(liteQuery)

        resSql, resLite = self.sqlCursor.fetchall(), self.liteCursor.fetchall()
        if len(resLite) != len(resSql):
            if self.again:
                self.again = False
                self.post(salesperson)

            elif not self.again:
               sqlQuery = f"UPDATE `testing`.`trans` SET counter = '1' WHERE counter = '1' AND salesperson = '{salesperson}' AND fbydate >= date('now', '-3 day')"

        elif len(resSql) == 0 or len(resLite) == 0:
            pass

        elif len(resSql) == 0 and len(resLite) == 0:
            return [{100: {"message": "there are no entries in your table. You recently made zero transactions."}}]

        elif not self.again:
            return [{200 :{"message": "You are currently locked out of the service."}}] # When you try to sync twice, but it fails; locks client out of service until further notice.

        else:
            return [{200: {"message": "An unexpected error has occured", "function": "Within function verify() in sync.py"}}] # Just incase something unexpected occurs


    def updateCounter(self, salesperson):
        """Updates all 1's to 2's signifying that the transactions are valid, and trustworthy."""
        liteQuery = f"UPDATE `transaction` SET counter = '2' WHERE counter = '1' AND salesperson = '{salesperson}' AND fbydate >= date('now', '-3 day')"
        sqlQuery = f"UPDATE `testing`.`trans` SET counter = '2' WHERE counter = '1' AND salesperson = '{salesperson}' AND fbydate >= CURDATE() - INTERVAL 3 day"

        self.liteCursor.execute(liteQuery)
        self.liteCon.commit()

        self.sqlCursor.execute(sqlQuery)
        self.mySql.commit()

    def commitData(self, commits, salesPerson):
        # Final check before updating the counter to a 2
        self.verify(salesperson=salesPerson)        

        liteQuery = f"UPDATE `transaction` SET counter = '1' WHERE counter = '0' AND salesperson = '{salesPerson}' AND fbydate >= date('now', '-3 day')"
        self.liteCursor.execute(liteQuery)
        self.liteCon.commit()

        for commit in commits:
            self.sqlCursor.execute(commit)
        self.mySql.commit()

        self.updateCounter(salesperson=salesPerson)



