# Fixed connection issue
from flask_restful import abort, Resource # pip install flask-restful

from QA.encrypt import Hash
from QA.key import Key
from QA.database import Database

import decimal # local
from mysql.connector.errors import ProgrammingError

class SQL(Resource):
    def __init__(self):
        try:
            self.mydb, self.cursor = Database().connect("localhost", "root", "8811967", "tsc_office")
            # self.mydb, self.cursor = Database().connect("192.168.1.165", "testuser123", "YJH030412yjh_g", "tsc_office")

        except ProgrammingError as err:
            abort(503, message="Unable to connecct to database.")

    def get(self, key: str, user: str, hash: str, api: str, dep: str) -> dict:
        """
        GET request works perfectly well. GET requests are done via the url. Take a look at the adding resources
        section for more information
        """
        print(api)
        print("Department: " + dep)
        Key().verifyKey(user, key)
        H = Hash(str(hash))
        hashed = H.encrypt()

        tableColumns = "fid, fuser, fpassword, flocation, finvoice, fcomplaint, ffinance, fpersonnel, femail, fcc, ffunction, fleave, fhr, froadtax, ftr, forder, fsalesman, ftele, fwarehouse, fpotato, fcsr, fconnect, fdriver, fdo, fcollection, femp, fic, DATE_FORMAT(findate, \"%Y-%m-%d\") AS findate, DATE_FORMAT(findate, \"%Y-%m-%d\") AS fconfirmdate, fpic, fplace, fname, fwarehouselog, fdsr, fvvip"
        sqlQuery = f"SELECT {tableColumns} FROM tsc_office.tap WHERE fuser=\'{user}\' AND fpassword=\'{hashed}\'"

        self.cursor.execute(sqlQuery)
        res = self.cursor.fetchall() # Formatted to give the text output, a tuple of data. Previous a list of a tuple.

        if res == None:
            return {404: {"error": "Nothing was returned"}}

        elif len(res) == 0:
            tableColumns = "fid, fuser, fpassword, flocation, finvoice, fcomplaint, ffinance, fpersonnel, femail, fcc, ffunction, fleave, fhr, froadtax, ftr, forder, fsalesman, ftele, fwarehouse, fpotato, fcsr, fconnect, fdriver, fdo, fcollection, femp, fic, DATE_FORMAT(findate, \"%Y-%m-%d\") AS findate, DATE_FORMAT(findate, \"%Y-%m-%d\") AS fconfirmdate, fpic, fplace, fname, fwarehouselog, fdsr, fvvip"
            sqlQuery = f"SELECT fuser FROM tsc_office.tap"
            self.cursor.execute(sqlQuery)
            res = self.cursor.fetchall() # Formatted to give the text output, a tuple of data. Previous a list of a tuple.
            print(res)
            # return {404: {"error": "Either the username, or password is incorrect."}}

        keyValuePairs = Database().keyValuePairing(self.cursor, res)
        return [{200: {"success": keyValuePairs}}]