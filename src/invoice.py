from flask_restful import abort, Resource, reqparse

from QA.key import Key
from QA.database import Database

import datetime
import decimal

class Invoice(Resource):
    def __init__(self):
        host = ["localhost", "192.168.1.165", "localhost"]
        user = ["root", "testuser123", "root"]
        database = ["testing", "testing", "tsc_office"]

        o = 0

        with open("D:\python\Web API\src\Files\sql.txt") as f:
            password = f.readlines()

        self.KeyTable, self.keyCursor = Database().connect(host[o], user[o], password[o], database[0])

        args = reqparse.RequestParser()
        args.add_argument("no", type=str)

        args = args.parse_args()
        self.no = args["no"]

    def get(self, key):
        Key().verifyKey(key)

        if len(self.no) == 0 or self.no == None:
            sqlQuery = f"SELECT * FROM tsc_office.tinvoicehistory WHERE finvoiceno"
            self.keyCursor.execute(sqlQuery)
            res = self.keyCursor.fetchall()
            if res  == None or len(res) == 0:
                abort(404, message="Not found.")

            formattedRes = Database().toSerialisable(res)
            for con in formattedRes:
                for n, v in enumerate(con):
                    if type(v) == decimal.Decimal:
                        con[n] = Database().json_default(v)
                    elif v == None:
                        con[n] = ""

            return {200: formattedRes}

        columnOne = "fno, finvoiceno, DATE_FORMAT(fdate, \"%Y-%m-%d\") AS fdate, fdesc, frefno, fterm, DATE_FORMAT(fduedate, \"%Y-%m-%d\") AS fduedate, fnettotal, fpaymentamt, foutstanding, fcancelled, DATE_FORMAT(ftimestamp, \"%Y-%m-%d %H:%i:%s\") AS ftimestamp, fuserid"
        columnTwo = f"{columnOne}, fusername, fdebtorcode, fcompanyname, ftype, fsalesagent, fsalesagentdesc, fcreditlimit"
        columnThree = f"{columnTwo}, fpendingdelivery, DATE_FORMAT(fdeliverydate, \"%Y-%m-%d\") AS fdeliverydate, florryno, fdriver, fhelper1, fhelper2, fhelper3, froute, fpod"
        columnFour = f"{columnThree}, fcomment, fstatus, fextraattempt, fverified, DATE_FORMAT(fverifiedtimestamp, \"%Y-%m-%d %H:%i:%s\") AS fverifiedtimestamp, fverifiedby, tinvoicehistorycol, fcrates, ftimeout, ftimein, fcycletime, fcollection"
        columnName = columnFour

        sqlQuery = f"SELECT {columnName} FROM tsc_office.tinvoicehistory WHERE tinvoicehistory = '{self.no}'"
        self.keyCursor.execute(sqlQuery)
        res = self.keyCursor.fetchall()
        formattedRes = self.__toList(res)
        for con in formattedRes:
            for n, v in enumerate(con):
                if type(v) == decimal.Decimal or type(v) == datetime.date:
                    con[n] = self.json_default(v)
                elif v == None:
                    con[n] = ""

        return {200: formattedRes}
