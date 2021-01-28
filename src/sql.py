# Fixed connection issue
from flask_restful import Api, Resource, reqparse # pip install flask-restful

from QA.encrypt import Hash
from QA.key import Key
from QA.database import Database

import decimal # local

class SQL(Resource):
    def __init__(self):
        o = 0
        """Setting up database connection"""
        host = ["localhost", "192.168.1.165"]
        user = ["root", "testuser123"]
        database = ["testing", "testing"]
        
        with open("D:\python\Web API\src\Files\sql.txt") as f:
            password = f.readlines()

        print("connection returned")
        self.mydb, self.cursor = Database().connect(host[o], user[o], password[o].strip("\n"), database[o])

        args = reqparse.RequestParser()
        args.add_argument("no", type=str)

        args = args.parse_args()
        self.no = args["no"]

    def get(self, name, hash, key, dep):
        """
        GET request works perfectly well. GET requests are done via the url. Take a look at the adding resources
        section for more information
        """
        print("Department: " + dep)
        Key().verifyKey(key)
        H = Hash(str(hash))
        hashed = H.encrypt()

        tableColumns = "fid, fuser, fpassword, flocation, finvoice, fcomplaint, ffinance, fpersonnel, femail, fcc, ffunction, fleave, fhr, froadtax, ftr, forder, fsalesman, ftele, fwarehouse, fpotato, fcsr, fconnect, fdriver, fdo, fcollection, femp, fic, DATE_FORMAT(findate, \"%Y-%m-%d\") AS findate, DATE_FORMAT(findate, \"%Y-%m-%d\") AS fconfirmdate, fpic, fplace, fname, fwarehouselog, fdsr, fvvip"
        sqlQuery = f"SELECT {tableColumns} FROM tsc_office.tap WHERE fuser=\'{name}\' AND fpassword=\'{hashed}\'"
        self.cursor.execute(sqlQuery)
        res = self.cursor.fetchall() # Formatted to give the text output, a tuple of data. Previous a list of a tuple.

        if self.no == "" or self.no == None and key:
            sqlQuery = "SELECT * FROM tsc_office.tap"
            self.cursor.execute(sqlQuery)
            res = self.cursor.fetchall()
            formattedRes = self.__toList(res)
            for con in formattedRes:
                for n, v in enumerate(con):
                    if type(v) == decimal.Decimal:
                        con[n] = self.json_default(v)
                    elif v == None:
                        con[n] = ""

            return {200: {"success": formattedRes}}

        if res == None:
            return {404: {"error": "Nothing was returned"}}

        elif len(res) == 0:
            tableColumns = "fid, fuser, fpassword, flocation, finvoice, fcomplaint, ffinance, fpersonnel, femail, fcc, ffunction, fleave, fhr, froadtax, ftr, forder, fsalesman, ftele, fwarehouse, fpotato, fcsr, fconnect, fdriver, fdo, fcollection, femp, fic, DATE_FORMAT(findate, \"%Y-%m-%d\") AS findate, DATE_FORMAT(findate, \"%Y-%m-%d\") AS fconfirmdate, fpic, fplace, fname, fwarehouselog, fdsr, fvvip"
            sqlQuery = f"SELECT fuser FROM tsc_office.tap"
            self.cursor.execute(sqlQuery)
            res = self.cursor.fetchall() # Formatted to give the text output, a tuple of data. Previous a list of a tuple.
            print(res)
            # return {404: {"error": "Either the username, or password is incorrect."}}

        description = self.cursor.description # Gets all the column names
        desc = [description[c][0] for c, _ in enumerate(description)] # Storing all the column names into a list, previously = (fid, 0, 0, 0) after formatting = fid
        headersAndValues = {k: v for k, v in zip(desc, res[0])} # Dictionary comprehension, with column names (desc) as a key, and the values (res) as its vaue.
        for k in headersAndValues:
            if headersAndValues[k] == None:
                headersAndValues[k] = ""

        return [{200: {"success": headersAndValues}}]

    def json_default(self, value): 
        if isinstance(value, decimal.Decimal):
            return str(float(value)) + "0"
            # return float(value)
        raise TypeError('not JSON serializable') #you may choose not to raise the Error though 

    def __toList(self, data):
        data = [list(c) for c in data]

        return data