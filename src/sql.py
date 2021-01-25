from flask import Flask # pip install flask
from flask_restful import abort, Resource, reqparse # pip install flask-restful

import mysql.connector # pip install mysql-connector-python
import QA

from QA.key import Key

class SQL(Resource):
    def __init__(self):
        pass

    def startupAndVerify(id, password):
        """Verify user"""
        K = Key()
        key = K.verify(id, password)

        """Setting up database connection"""
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

        return mydb, cursor, key

    def get(self, name, hash, id, key, dep):
        self.mydb, self.cursor, self.key = self.startup(id, key)
        """
        GET request works perfectly well. GET requests are done via the url. Take a look at the adding resources
        section for more information
        """

        print("Department: " + dep)

        H = QA.Hash(str(hash))
        hashed = H.encrypt()

        columnsPartOne = "fid, fuser, fpassword, flocation, finvoice, fcomplaint, ffinance, fpersonnel, femail, fcc, ffunction, fleave, fhr, froadtax, ftr, forder, fsalesman, ftele, fwarehouse"
        columnsPartTwo = "fpotato, fcsr, fconnect, fdriver, fdo, fcollection, femp, fic, DATE_FORMAT(findate, \"%Y-%m-%d\") AS findate, DATE_FORMAT(findate, \"%Y-%m-%d\")"
        tableColumns = f"{columnsPartOne}, {columnsPartTwo} AS fconfirmdate, fpic, fplace, fname, fwarehouselog, fdsr, fvvip"

        sqlQuery = f"SELECT {tableColumns} FROM tsc_office.tap WHERE fuser=\'{name}\' AND fpassword=\'{hashed}\'"
        self.cursor.execute(sqlQuery)

        res = self.cursor.fetchall() # Formatted to give the text output, a tuple of data. Previous a list of a tuple.
        if res == None:
            abort(404, message="")

        elif len(res) == 0:
            abort(404, message="")

        description = self.cursor.description # Gets all the column names
        desc = [description[c][0] for c, _ in enumerate(description)] # Storing all the column names into a list, previously = (fid, 0, 0, 0) after formatting = fid

        headersAndValues = {k: v for k, v in zip(desc, res[0])} # Dictionary comprehension, with column names (desc) as a key, and the values (res) as its vaue.
        for k in headersAndValues:
            if headersAndValues[k] == None:
                headersAndValues[k] = ""

        return {200: {"success": headersAndValues}}