from flask_restful import Resource, abort, reqparse

from QA.database import Database
from QA.key import Key

class TInvoiceHistory(Resource):
    """This is endpoint is meant to view a specific invoice, or to view all invoices"""
    def __init__(self):
        password = Database.getPassword()
        self.schema = "tsc_office"

        try:
            self.conn, self.cursor = Database.connect("localhost", "root", password[0], self.schema)
        except Exception:
            self.conn, self.cursor = Database.connect("localhost", "root", password[1], self.schema)


        parser = reqparse.RequestParser()
        parser.add_argument("key", type=str, location='headers')
        parser.add_argument("user", type=str, location='headers')

        parsed = parser.parse_args()
        key, user = parsed["key"], parsed["user"]

        Key().verifyKey(user, key)

    def get(self, invoiceNumber: str):
        """Processes the GET request. Gets all information of a specific invoice by referencing via invoice number.

        ---
        # Parameteres
        ### invoiceNumber
        Invoice number of an invoice.
        """
        if invoiceNumber.lower() == "all":
            sqlQuery = f"SELECT * FROM {self.schema}.tinvoicehistory LIMIT 10"
            self.cursor.execute(sqlQuery)
            res = self.cursor.fetchall()

            formattedRes = Database().formatEntries(res)

            return {200: {"success": formattedRes}}

        columnOne = "fno, finvoiceno, DATE_FORMAT(fdate, \"%Y-%m-%d\") AS fdate, fdesc, frefno, fterm, DATE_FORMAT(fduedate, \"%Y-%m-%d\") AS fduedate, fnettotal, fpaymentamt, foutstanding, fcancelled, DATE_FORMAT(ftimestamp, \"%Y-%m-%d %H:%i:%s\") AS ftimestamp, fuserid"
        columnTwo = f"{columnOne}, fusername, fdebtorcode, fcompanyname, ftype, fsalesagent, fsalesagentdesc, fcreditlimit"
        columnThree = f"{columnTwo}, fpendingdelivery, DATE_FORMAT(fdeliverydate, \"%Y-%m-%d\") AS fdeliverydate, florryno, fdriver, fhelper1, fhelper2, fhelper3, froute, fpod"
        columnFour = f"{columnThree}, fcomment, fstatus, fextraattempt, fverified, DATE_FORMAT(fverifiedtimestamp, \"%Y-%m-%d %H:%i:%s\") AS fverifiedtimestamp, fverifiedby, tinvoicehistorycol, fcrates, ftimeout, ftimein, fcycletime, fcollection"
        columnName = columnFour

        sqlQuery = f"SELECT {columnName} FROM {self.schema}.tinvoicehistory WHERE finvoiceno = '{invoiceNumber}'"
        self.cursor.execute(sqlQuery)
        res = self.cursor.fetchall()

        if len(res) == 0:
            abort(404, message=f"Entry with invoice number: '{invoiceNumber}' not found")

        elif len(res) > 1:
            formattedRes = Database().toSerialisable(res)
            return {200: formattedRes}

        formattedRes = Database().formatEntries(res)
        keyValuePairOfFormattedRes = Database().keyValuePairing(self.cursor, formattedRes)

        return {200: keyValuePairOfFormattedRes}
