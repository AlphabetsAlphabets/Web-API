import datetime
import decimal
from typing import Union

import mysql.connector
from flask_restful import abort

"""All types from third party modules will be prefixed with TYPE and will all be uppercase."""
from mysql.connector.cursor import MySQLCursor as TYPE_CURSOR
from mysql.connector.connection import MySQLConnection as TYPE_SQL_CONN
from mysql.connector.errors import ProgrammingError as E_PROGRAMMING_ERROR

class Database:
    """
    This class provides functions for connecting to MySQL databases. As well as functions
    for formatting, and conversion of non-serializable JSON to serilizable JSON.

    ---

    # Functions
    - connect
    - __json_default (private)
    - toSerialisable
    - keyValuePairing
    - formatEntries
    - getColumnNames
    - columnNamesForInsert
    - forUpdate

    """
    def connect(host: str, user: str, password: str, schema_name: str) -> Union[TYPE_SQL_CONN, TYPE_CURSOR]:
        """Connects to a MySQL database assuming all entered information is valid.

        ---
        
        # Parameters
        ### host
        The ip address of the host for the MySQL server, \
        if the server is hosted on your local machine simply set host to 'localhost'

        ### user
        The username of the mysql database. 

        ### password
        The password needed to login into the mysql database.

        ### schema_name
        The name of the schema you are trying to connect to.\ 
        For example in `tsc_office.tinvoicehistory` tsc_office is the schema name, \
        and `tinvoicehistory` is the table name.

        ---

        # Exceptions
        - ProgrammingError: This error occurs when one of the four fields are incorrect,
        whether it be password, or host, etc.

        """
        try:
            connection = mysql.connector.connect(
                host = host, user = user, password = password,
                database = schema_name, auth_plugin="mysql_native_password"
            )
            cursor = connection.cursor()

        except E_PROGRAMMING_ERROR as e:
            errno = e.errno
            if errno != 1049:
                abort(404, message=f"Database '{schema_name}' does not exist.")

        return connection, cursor

    def __json_default(self, value: Union[decimal.Decimal, datetime.date, datetime.datetime, datetime.timedelta]) -> str: 
        """Formats datatype outputs from non-serializable to serializable

        ---
        
        # Parameters
        ### value
        The value to be converted to be a JSON serializable object
        """
        if isinstance(value, decimal.Decimal):
            return str(float(value)) + "0"
            
        elif isinstance(value, datetime.date):
            return str(value.strftime("%Y-%m-%d"))

        elif isinstance(value, datetime.datetime):
            return str(value.strftime("%Y-%m-%d %H:%M:%S"))

        elif isinstance(value, datetime.timedelta):
            return str(value)

    def toSerialisable(self, data: tuple) -> list:
        """Converts non-serializable JSON objects to serilizable JSON objects

        ---
        
        # Parameters
        ### data
        The data that will be converted to a JSON serializable object
        """
        data = [list(c) for c in data]

        return data

    def keyValuePairing(self, cursor: TYPE_CURSOR, res: list) -> dict:
        """
        Transforms a list of unserialisable objects, to a dictionary. Which is serialisable. 

        Parameters
        ==========
        cursor
        ------
        The mysql cursor that was returned from the `connect` function.

        res
        ---
        The list of results from successfull execution of a mysql query \
        from `self.cursor.fetchall()`.
        """
        description = cursor.description # Gets all the column names
        desc = [description[c][0] for c, _ in enumerate(description)] # Storing all the column names into a list, previously = (fid, 0, 0, 0) after formatting = fid

        keyValuePairs = {k: v for k, v in zip(desc, res[0])} # Dictionary comprehension, with column names (desc) as a key, and the values (res) as its vaue.
        for k in keyValuePairs:
            returnValue = self.__json_default(k)
            if returnValue is not None:
                keyValuePairs[k] = returnValue

        return keyValuePairs


    def formatEntries(self, result: list) -> list:
        """Converts any MySQL database types to native python types.

        ---
        
        # Parameters
        ### result 
        The list of results from successfull execution of a mysql query \
        from `self.cursor.fetchall()`.
        """
        formattedRes = self.toSerialisable(result)
        for con in formattedRes:
            for n, v in enumerate(con):
                returnValue = self.__json_default(v)
                if returnValue is not None:
                    con[n] = returnValue

                elif v == None:
                    con[n] = ""

        return formattedRes
        
    def getColumnNames(cursor: TYPE_CURSOR, names: list) -> str:
        """
        Takes in a list of column names, and stiches them together to form a string of all the column names.

        ---

        # Parameters
        ### cursor
        The MySQLCursor returned when connecting to a MySQL database.

        ### names
        A list of column names.
        """
        baseString = ""
        for name in names:
            if name == names[0]:
                baseString += name
            elif name == names[-1]:
                baseString += ", " + name
            else:
                baseString += ", " + name

        return baseString

    def columnNamesForInsert(cursor: TYPE_CURSOR, names: list = None) -> str:
        """Prepares an insert statement.
        
        # Parameters
        ### cursor
        The MySQLCursor returned when connecting to a MySQL database.

        ### name
        The list of column names     
        """
        if names == None:
            description = cursor.description # Gets all the column names
            formattedName = [description[c][0] for c, _ in enumerate(description)] # Storing all the column names into a list, previously = (fid, 0, 0, 0) after formatting = fid

        elif names != None:
            names = names.split(", ")
            formattedName  = [f"`{name}`" for name in names]

        baseString = ""
        for name in formattedName:
            if name == formattedName[0]:
                baseString += name
            elif name == formattedName[-1]:
                baseString += ", " + name
            else:
                baseString += ", " + name
                
        return baseString

    def forUpdate(columnNames: str, values: list) -> str:
        """Prepares an update statement.

        ---
        
        # Parameters
        ### columnNames
        The columNames that will be needed for the update statement.

        ### values
        The values to update the columns to. 
        """
        valid = [f"{column} = {value}" for column, value in zip(columnNames.split(", "), values.split(", ")) if len(value.strip()) != 0]

        return (", ").join(valid)

