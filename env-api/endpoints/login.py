from flask_restful import Resource 

from QA.database import Database
from QA.key import Key

from werkzeug.exceptions import NotFound

class Login(Resource):
    """The login endpoint, provides a user with the api key and his fid

    ---
    # Functions
    - __init__
    - get
    
    """
    def __init__(self):
        """Connects to the MySQL database"""
        try:
            self.tap, self.cursor = Database.connect("localhost", "root", "8811967", "tsc_office")
        except NotFound:
            self.tap, self.cursor = Database.connect("localhost", "root", "YJH030412yjh_g", "tsc_office")

    def get(self, user, password):
        """Processes the GET request
        
        ---
        # Parameters
        ### user
        The name of the user
        
        ### password
        The user's passowrd
        """
        enc, k = Key().getKey(user, password)

        sqlString = f"SELECT * FROM tsc_office.tap WHERE fuser = '{user}' AND fpassword = '{enc}'"
        self.cursor.execute(sqlString)

        fid = self.cursor.fetchall()[0][4]

        return {"fid": fid, "key": k}
