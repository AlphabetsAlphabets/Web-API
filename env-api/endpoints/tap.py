# Fixed connection issue
from flask_restful import abort, Resource, reqparse # pip install flask-restful

from QA.key import Key
from QA.encrypt import Hash
from QA.database import Database

from mysql.connector.errors import ProgrammingError

class Tap(Resource):
    """Gets information about a specific user. Requires login.
    
    ---
    # Functions
    ### public
    - __init__
    - get
    """
    def __init__(self):
        """Handles initilization, and connects to a MySQL database."""
        self.schema = "tsc_office"
        try:
            self.mydb, self.cursor = Database().connect("localhost", "root", "-", self.schema)

        except ProgrammingError:
            self.mydb, self.cursor = Database().connect("localhost", "root", "8811967", self.schema)
            # abort(503, message="Unable to connect to database.")

        parser = reqparse.RequestParser()
        parser.add_argument("key", type=str, location='headers')
        parser.add_argument("user", type=str, location='headers')

        parsed = parser.parse_args()
        key, user = parsed["key"], parsed["user"]

        verified = Key().verifyKey(user, key)
        abort(404, message="Invalid credentials.") if verified == False else ""

    def get(self, user, hash):
        """
        GET request works perfectly well. GET requests are done via the url. Take a look at the adding resources
        section for more information

        ---
        # Parameters
        ### user
        The user's name

        ### hash
        The string of characters to-be encrypted.
        """
        hashed = Hash.encrypt(hash)
        
        tableColumns = "fid, fuser, fpassword, flocation, finvoice, fcomplaint, ffinance, fpersonnel, femail, fcc, ffunction, fleave, fhr, froadtax, ftr, forder, fsalesman, ftele, fwarehouse, fpotato, fcsr, fconnect, fdriver, fdo, fcollection, femp, fic, DATE_FORMAT(findate, \"%Y-%m-%d\") AS findate, DATE_FORMAT(findate, \"%Y-%m-%d\") AS fconfirmdate, fpic, fplace, fname, fwarehouselog, fdsr, fvvip"
        sqlQuery = f"SELECT {tableColumns} FROM {self.schema}.tap WHERE fuser=\'{user}\' AND fpassword=\'{hashed}\'"

        self.cursor.execute(sqlQuery)
        res = self.cursor.fetchall() # Formatted to give the text output, a tuple of data. Previous a list of a tuple.

        if len(res) == 0:
            return {404: {"error": "Either the username, or password is incorrect."}}

        keyValuePairs = Database().keyValuePairing(self.cursor, res)
        return [{"success": keyValuePairs}]
