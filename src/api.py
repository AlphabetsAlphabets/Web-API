"""
Full list of external libraries will be found in requirements.txt in the same directory level. Unless Suffixed with local then it comes with
the default installation
"""
from flask import Flask # pip install flask
from flask_restful import Api # pip install flask-restful

import QA
from sync import Sync # To sync.py
from update import Update # to update.py
from sql import SQL # to sql.py

app = Flask(__name__) # Initialisation of a flask app
api = Api(app) # Initilisation of a RESTful API

# Adding resources
"""
This is for any request, but, is most significant for a GET request. In the second parameter you can see the following:
/<string:debtorCode>
Which means that after the domain name of the website. Add a slash followed by a valid debtor code. And the result, will be returned.
In the form of JSON.
"""
# api.add_resource(SQL, "/get/<string:dep>/<string:name>/<string:id>/<string:hash>/<string:key>") 
api.add_resource(SQL, "/get/<string:name>/<string:hash>/<string:id>/<string:key>/<string:dep>") 
api.add_resource(Sync, "/sync/post")
api.add_resource(Update, "/update")

@app.route("/") # Default page
def hello():
    return "If you are on this screen. Make sure you know what you're doing. If not, leave the site."

@app.route("/password")
def password():
    return "Password here: 123"

currentHost = QA.host()
app.run(debug=True, host=currentHost)
