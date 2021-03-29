"""
Check requirements.txt for library details.
"""
# TODO: error handing during execute of sql queries, whether it be sqLITE or MySQL

from flask import Flask, session
from flask_restful import Api 

import socket

"""It's worth noting that the order of important is according the which api was made first.
First import being the first endpoint that was made."""
from endpoints.tap import Tap
from endpoints.tinvoicehistory import TInvoiceHistory
from endpoints.sync import Sync
from endpoints.spec import Spec
from endpoints.insertGeneric import InsertGeneric
from endpoints.login import Login
from endpoints.upload import Upload
from endpoints.location import Location
from endpoints.firstTimeSetup import FirstTimeSetup

app = Flask(__name__) 
api = Api(app) 

# Add key, and user params to all url's except spec, and login for key validation.
api.add_resource(Tap, "/tap/<string:user>/<string:hash>")
api.add_resource(TInvoiceHistory, "/get/tinvoicehistory/<string:invoiceNumber>")
api.add_resource(Sync, "/sync/<string:salesperson>")
api.add_resource(Spec, "/get/spec/<string:table>/<string:o1>/<string:o2>/<string:o3>/<string:o4>/<string:o5>")
api.add_resource(InsertGeneric, "/redirect/<string:table>/<string:invoiceno>")
api.add_resource(Login, "/<string:user>/<string:password>")
api.add_resource(Upload, "/upload/<string:saveName>")
api.add_resource(Location, "/locations")
api.add_resource(FirstTimeSetup, "/fts")

@app.route("/") # Default page
def hello():
    return "API of TSC"

@app.route("/password")
def password():
    return "Password here: 123"

if __name__ == "__main__":
    current_host = socket.gethostbyname(socket.gethostname())
    app.run(debug = True, host=current_host)
