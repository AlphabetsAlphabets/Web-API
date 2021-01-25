"""
Full list of external libraries will be found in requirements.txt in the same directory level. Unless Suffixed with local then it comes with
the default installation
"""
from flask import Flask # pip install flask
from flask_restful import abort, Api, Resource, reqparse # pip install flask-restful

import mysql.connector # pip install mysql-connector-python

import QA
from sync import Sync # To sync.py
from update import Update # to update.py
from key import Key # To key.py


app = Flask(__name__) # Initialisation of a flask app
api = Api(app) # Initilisation of a RESTful API

class SQL(Resource):
    def __init__(self):
        """Setting up database connection"""
        host = ["localhost", "192.168.1.165"]
        user = ["root", "testuser123"]
        database = ["testing", "testing"]
        out = 0
        
        with open("sql.txt") as f:
            password = f.readline()

        self.mydb = mysql.connector.connect(
            host=host[out], 
            user=user[out],
            password=password,
            database=database[out]
            )

        self.cursor = self.mydb.cursor()

    def get(self, dep, name, hash):
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

# Adding resources
"""
This is for any request, but, is most significant for a GET request. In the second parameter you can see the following:
/<string:debtorCode>
Which means that after the domain name of the website. Add a slash followed by a valid debtor code. And the result, will be returned.
In the form of JSON.
"""
api.add_resource(SQL, "/get/<string:dep>/<string:name>/<string:hash>") 
api.add_resource(Sync, "/sync/post")
api.add_resource(Update, "/update/<string:key>")
api.add_resource(Key, "/key")

@app.route("/") # Default page
def hello():
    return "If you are on this screen. Make sure you know what you're doing. If not, leave the site."

@app.route("/password")
def password():
    return "Password here: 123"

currentHost = QA.host()
app.run(debug=True, host=currentHost)
