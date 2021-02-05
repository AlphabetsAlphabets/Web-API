import datetime
import decimal
 
from flask_restful import Resource, abort, reqparse

from QA.database import Database
from QA.key import Key

class Invoice(Resource):
    def __init__(self):
        self.keyTable, self.keyCursor = Database().connect("localhost", "root", "8811967", "tsc_office")

        args = reqparse.RequestParser()
        args.add_argument("no", type=str)

        args = args.parse_args()
        self.no = args["no"]

    def get(self, key: str, user: str, api: str, identifier: str = None):
        print(api)
        Key().verifyKey(user, key)

        if identifier.lower() == "all":
            sqlQuery = f"SELECT * FROM tsc_office.tinvoicehistory LIMIT 10"
            self.keyCursor.execute(sqlQuery)
            res = self.keyCursor.fetchall()
            if res  == None or len(res) == 0:
                abort(404, message="Not found.")

            formattedRes = Database().formatEntries(res)

            return {200: {"success": formattedRes}}

        columnOne = "fno, finvoiceno, DATE_FORMAT(fdate, \"%Y-%m-%d\") AS fdate, fdesc, frefno, fterm, DATE_FORMAT(fduedate, \"%Y-%m-%d\") AS fduedate, fnettotal, fpaymentamt, foutstanding, fcancelled, DATE_FORMAT(ftimestamp, \"%Y-%m-%d %H:%i:%s\") AS ftimestamp, fuserid"
        columnTwo = f"{columnOne}, fusername, fdebtorcode, fcompanyname, ftype, fsalesagent, fsalesagentdesc, fcreditlimit"
        columnThree = f"{columnTwo}, fpendingdelivery, DATE_FORMAT(fdeliverydate, \"%Y-%m-%d\") AS fdeliverydate, florryno, fdriver, fhelper1, fhelper2, fhelper3, froute, fpod"
        columnFour = f"{columnThree}, fcomment, fstatus, fextraattempt, fverified, DATE_FORMAT(fverifiedtimestamp, \"%Y-%m-%d %H:%i:%s\") AS fverifiedtimestamp, fverifiedby, tinvoicehistorycol, fcrates, ftimeout, ftimein, fcycletime, fcollection"
        columnName = columnFour

        sqlQuery = f"SELECT {columnName} FROM tsc_office.tinvoicehistory WHERE finvoiceno = '{identifier}'"
        self.keyCursor.execute(sqlQuery)
        res = self.keyCursor.fetchall()

        if len(res) == 0:
            abort(404, message=f"Entry with invoice number: '{identifier}' not found")

        formattedRes = Database().getAllEntries(res)

        return {200: formattedRes}
