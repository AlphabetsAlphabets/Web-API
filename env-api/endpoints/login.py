from flask_restful import Resource 

from QA.database import Database
from QA.key import Key

from werkzeug.exceptions import NotFound

class Login(Resource):
    """The login endpoint, provides access to the api key and fid level of a specific user. Provided they have the correct username, and password of course.
    
    Inherits from Resource from flask restful"""
    def __init__(self):
        """Connects to the MySQL database"""
        try:
            self.tap, self.tapCursor = Database.connect("localhost", "root", "8811967", "tsc_office")
        except NotFound:
            self.tap, self.tapCursor = Database.connect("localhost", "root", "YJH030412yjh_g", "tsc_office")

    def get(self, user, password):
        enc, k = Key().getKey(user, password)

        sqlString = f"SELECT * FROM tsc_office.tap WHERE fuser = '{user}' AND fpassword = '{enc}'"
        self.tapCursor.execute(sqlString)

        fid = self.tapCursor.fetchall()[0][4]

        return {"fid": fid, "key": k}
