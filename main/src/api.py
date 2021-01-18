"""
Full list of external libraries will be found in requirements.txt in the same directory level. Unless Suffixed with local then it comes with
the default installation
"""
import json # local
import requests # pip install requests

from flask import Flask # pip install flask
from flask_restful import Api, Resource, reqparse # pip install flask-restful

import mysql.connector # pip install mysql-connector-python

from encrypt import Hash
from ip import host
from sync import Sync # To sync.py
from update import Update # to update.py


app = Flask(__name__) # Initialisation of a flask app
api = Api(app) # Initilisation of a RESTful API

"""
The following code is PUT request specific, until indicated by "ends here". And this is a guideline for creating future PUT request functions.

While constructing the url, and adding it as a resource. The parameters passed in during url construction.
Will need to be added as a parameter in the PUT function. Or there will be an error - indicating that the parameter is passed in, but not expected. 
Which will crash the API. Once you add it as an accepted argument in the PUT function. You can just leave it, you dont actually need to do anything with it.
"""

sqlRequests = reqparse.RequestParser()
sqlRequests.add_argument("debtorCode", type=str, help="You need to enter a unique debtor code.")
sqlRequests.add_argument("companyName", type=str, help="You need to enter a unique debtor code.")

"""ends here"""

class SQL(Resource):
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="192.168.1.165",
            user="testuser123",
            password="YJH030412yjh_g",
            database="tsc_office"
            )

        self.cursor = self.mydb.cursor()

    def get(self, name, hash):
        """
        GET request works perfectly well. GET requests are done via the url. Take a look at the adding resources
        section for more information
        """

        H = Hash(str(hash))
        hashed = H.encrypt()

        sqlQuery = f"SELECT fid, fuser, fpassword, flocation, finvoice, fcomplaint, ffinance, fpersonnel, femail, fcc, ffunction, fleave, fhr, froadtax, ftr, forder, fsalesman, ftele, fwarehouse, fpotato, fcsr, fconnect, fdriver, fdo, fcollection, femp, fic, DATE_FORMAT(findate, \"%Y-%m-%d\") AS findate, DATE_FORMAT(findate, \"%Y-%m-%d\") AS fconfirmdate, fpic, fplace, fname, fwarehouselog, fdsr, fvvip FROM tsc_office.tap WHERE fuser=\'{name}\' AND fpassword=\'{hashed}\'"
        self.cursor.execute(sqlQuery)
        res = self.cursor.fetchall() # Formatted to give the text output, a tuple of data. Previous a list of a tuple.
        if res == None:
            return {404: {"error": "Nothing was returned"}}

        elif len(res) == 0:
            return {404: {"error": "Either the username, or password is incorrect."}}

        description = self.cursor.description # Gets all the column names
        desc = [description[c][0] for c, _ in enumerate(description)] # Storing all the column names into a list, previously = (fid, 0, 0, 0) after formatting = fid
        headersAndValues = {k: v for k, v in zip(desc, res[0])} # Dictionary comprehension, with column names (desc) as a key, and the values (res) as its vaue.


        return {200: {"success": headersAndValues}}

    # def put(self, name, hash):
    #     """Current error is SQL database related and not the fault of the api. As of Tuesday, 12/1/2021"""

    #     print("PUT request")

    #     args = sqlRequests.parse_args()
    #     debtorCode, companyName = args["debtorCode"], args["companyName"] 
    #     print("POST request made")

    #     query = f"INSERT INTO `tsc_office`.`tinvoicehistory` (`fdebtorcode`, `fcompanyname`) VALUES ({name}, {hash})"
    #     print()
    #     return {200: {"success": "Successfully added a new entry."}}


# Adding resources
"""
This is for any request, but, is most significant for a GET request. In the second parameter you can see the following:
/<string:debtorCode>
Which means that after the domain name of the website. Add a slash followed by a valid debtor code. And the result, will be returned.
In the form of JSON.
"""
api.add_resource(SQL, "/<string:name>/<string:hash>") 
api.add_resource(Sync, "/sync")
api.add_resource(Update, "/update")

@app.route("/") # Default page
def hello():
    return "If you are on this screen. Make sure you know what youre doing. If not, leave the site."

@app.route("/password")
def password():
    return "Password here: 123"

currentHost = host()
app.run(debug=True, host=currentHost)
