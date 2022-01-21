# Schema: testing
from flask_restful import Resource, abort, reqparse
from QA.database import Database
from QA.key import Key

from typing import NoReturn, Union

from mysql.connector.cursor import MySQLCursor as TYPE_CURSOR

"""The reason as to why you should scrap this endpoint below"""
"""
    My personal opinion is that this endpoint should not exist at all. The best practice is one endpoint for one data base table.
    Not one generic one for a few of them. Because it's how api endpoint's work. They don't serve as a general purpose tool, but instead
    they serve a set of specific related tasks. 

    If the argument is that you will need to write a lot of endpoints if someone from high up the hierarchy demands a new feature 
    then you'll need to create a lot of endpoints. Which is why a generic one is best.

    But conventions must be followed to increase maintainability. The challenge of writing an endpoint with a general purpose is not
    only difficult, but hard to maintain.
"""

class InsertGeneric(Resource):
    """Makes an insert statement to the sql database, the statement is constructed through the url. Login required.

    ---
    # Functions
    ### public
    - __init__
    - put

    ### private
    - __validateDatabase
    - __join
    """
    def __init__(self):
        """Adds arguements to the request. Verify a user's key, and connects to the database."""
        password = Database.getPassword()

        parser = reqparse.RequestParser()
        parser.add_argument("con1", type=str)
        parser.add_argument("key", type=str, location="headers")
        parser.add_argument("user", type=str, location="headers")

        self.parsed = parser.parse_args()
        key, user = self.parsed["key"], self.parsed["user"]

        if key == None or user == None:
            abort(406, message = "Either the key, or user field is left blank.")

        Key().verifyKey(user, key)

        """A redirect table of some sort is needed. Refer to testing.redirect for a guide."""
        try:
            self.conn, self.cursor = Database.connect("localhost", "root", password[0], "testing")
            self.schema = "testing"
        except Exception:
            self.conn, self.cursor = Database.connect("localhost", "root", password[1], "tsc_office")
            self.schema = "tsc_office"

    def __validateDatabase(self, cursor: TYPE_CURSOR, table: str) -> str:
        """
        Checks whether the table you are trying to add a new entry to exists, if not throws a 404 not found
        exception.
        """
        sqlQuery = f"SELECT `sql_query` FROM testing.redirect WHERE table_name = '{table}'"
        self.cursor.execute(sqlQuery)
        res = cursor.fetchall()

        if len(res) == 0:
            abort(404, message = f"Table with the name of {table} does not exist, check your spelling, and try again.")

        return res[0][0]
 
    def __join(self, *values: list) -> Union[str, int]:
        """
        Strips all whitespace in front, and after the conditions. To make it cleaner, spaces between words will not be stripped.
        Add quotes to all values, then joins them all with ", " between each word.

        ---
        # Parameters
        ### *values
        A list of objects, such as strings, ints, floats, etc. You wish to join together to form a string.

        ---
        # Example
        ```python3
        objects = ["Monday", "Tuesday", "Wednesay"]
        result = Database().__join(objects)
        print(result) # "Monday, Tuesday, Wednesay
        ```
        """
        strippedValues = [value.strip() for value in values if len(value.strip()) != 0]
        quotedValues = [f"'{value}'" for value in strippedValues]
        joinedValues = (", ").join(quotedValues)

        return len(quotedValues), joinedValues

    def put(self, table: str, invoiceno: str) -> dict:
        """Takes your role into account. If your role is not within the dictionary, a forbidden error is thrown.

        ---
        # Parameters
        ### table
        The name of the table you wish to make edits to

        ### Invoiceno (temporary)
        The invoice number to reference whcih invoice you wish to edit.

        ---
        # Exceptions
        - ProgrammingError: Occurs when trying to connect to a database with invalid credentials
        """
        wheres = {"tinvoicehistory": "`finvoiceno`", "tdebtordetail": "`debtorcode`"}
        if table not in wheres:
            abort(404, message=f"table with the name of {table} not found.")

        con1 = self.parsed["con1"]

        conditionals = con1.split("|")
        values = self.__validateDatabase(self.cursor, table)
        columnNames = values.split("(")[1].split(",")
        numberOfColumns = len(columnNames)

        formattedColumnNames = [columnName.strip(")").strip() for columnName in columnNames]
        joinedColumnNames = (", ").join(formattedColumnNames)

        try:
            redirConn, redirCursor = Database.connect("localhost", "root", "-", self.schema)# Change database
        except Exception:
            redirConn, redirCursor = Database.connect("localhost", "root", "8811967", self.schema)

        silentQuery = f"SELECT * FROM testing.{table} LIMIT 1"
        redirCursor.execute(silentQuery)
        res = redirCursor.fetchall()
        if len(res) == 0:
            abort(404, message = f"The table {table} does not exist, check your spelling, and try again.")

        lengthOfGivenValues, quotedValues = self.__join(*conditionals)
        if numberOfColumns > lengthOfGivenValues:
            abort(406, message = f"You are required to fill a total of {numberOfColumns} but you have only entered in {lengthOfGivenValues}. Please fill up all the fields and then try again.")

        if invoiceno != "n":
            formattedColumnNamesForUpdate = Database.forUpdate(joinedColumnNames, quotedValues)
            sqlQuery = f"UPDATE {self.schema}.{table} SET {formattedColumnNamesForUpdate} WHERE {wheres[table]} = '{invoiceno}'"
        else:
            sqlQuery = f"INSERT INTO {self.schema}.{table} ({joinedColumnNames}) VALUES ({quotedValues})"

        """Uncomment (remove the hashtags from) the next two lines when the prerequisites have been setup."""
        redirCursor.execute(sqlQuery)
        redirConn.commit()

        return {201: "successfully added a new entry.", "query" : sqlQuery}

