"""
Full list of external libraries will be found in requirements.txt in the same directory level. Unless Suffixed with local then it comes with
the default installation
"""
import codecs  # local

from flask import Flask, session  # pip install flask
from flask_restful import Api  # pip install flask-restful

import QA

from endpoints.invoice import Invoice
from endpoints.login import Login
from endpoints.lookup import Lookup
from endpoints.sql import SQL  # to sql.py
from endpoints.sync import Sync  # To sync.py
from endpoints.update import Update  # to update.py
from endpoints.spec import Spec
from endpoints.image import Image

app = Flask(__name__) # Initialisation of a flask app
api = Api(app) # Initilisation of a RESTful API

# Adding resources
"""
This is for any request, but, is most significant for a GET request. In the second parameter you can see the following:
/<string:debtorCode>
Which means that after the domain name of the website. Add a slash followed by a valid debtor code. And the result, will be returned.
In the form of JSON.
"""

api.add_resource(Invoice, "/get/<string:key>/<string:user>/<string:api>/<string:identifier>")
api.add_resource(Login, "/get/login/<string:user>/<string:password>")
api.add_resource(Spec, "/get/spec/<string:table>/<string:o1>/<string:o2>/<string:o3>/<string:o4>/<string:o5>") # For external use, no API needed.
api.add_resource(SQL, "/get/<string:key>/<string:user>/<string:hash>/<string:api>/<string:dep>") 
api.add_resource(Sync, "/sync/post")
api.add_resource(Image, "/put/image")

with codecs.open("..\\src\\html\\index.html") as f:
    lines = f.read()

@app.route("/") # Default page
def hello():
    return lines

@app.route("/password")
def password():
    return "Password here: 123"

currentHost = QA.host()
app.run(debug=True, host=currentHost)
