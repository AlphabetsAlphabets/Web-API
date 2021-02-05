import datetime
import decimal
from typing import Union

import mysql.connector

"""All types from third party modules will be prefixed with TYPE and will all be uppercase."""
from mysql.connector.cursor import MySQLCursor as TYPE_CURSOR
from mysql.connector.connection import MySQLConnection as TYPE_SQL_CONN


class Database:
    def getColumnNames(names: list) -> str:
        """Takes in a list of column names, and stiches them together to form a string of all the column names."""
        blank = ""
        for name in names:
            if name == names[0]:
                blank += name
            elif name == names[-1]:
                blank += ", " + name
            else:
                blank += ", " + name

        return blank
                    
    def connect(self, host, user, password, database) -> Union[TYPE_SQL_CONN, TYPE_CURSOR]:
        """Connects to a MySQL database assuming all entered information is valid."""
        connection = mysql.connector.connect(
            host = host, user = user, password = password,
            database=  database
        )

        cursor = connection.cursor()
        return connection, cursor

    def json_default(self, value: Union[decimal.Decimal, datetime.date]) -> str: 
        if isinstance(value, decimal.Decimal):
            return str(float(value)) + "0"
            
        elif isinstance(value, datetime.date):
            return str(value.strftime("%Y-%m-%d"))

        elif isinstance(value, datetime.datetime):
            return str(value.strftime("%Y-%m-%d %H:%M:%S"))
        
        else:
            pass

    def toSerialisable(self, data: Union[list, tuple]) -> list:
        data = [list(c) for c in data]

        return data

    def keyValuePairing(self, cursor: TYPE_CURSOR, res: list) -> dict:
        """
        Transforms a list of unserialisable objects, to a dictionary. Which is serialisable. 
        """
        description = cursor.description # Gets all the column names
        desc = [description[c][0] for c, _ in enumerate(description)] # Storing all the column names into a list, previously = (fid, 0, 0, 0) after formatting = fid
        keyValuePairs = {k: v for k, v in zip(desc, res[0])} # Dictionary comprehension, with column names (desc) as a key, and the values (res) as its vaue.
        for k in keyValuePairs:
            if type(keyValuePairs[k]) == datetime.date:
                keyValuePairs[k] = keyValuePairs[k].strftime("%Y-%m-%d")

            elif keyValuePairs[k] == None:
                keyValuePairs[k] = ""

        return keyValuePairs

    def formatEntries(self, result: list) -> list:
        """Converts any MySQL database types to native python types."""
        formattedRes = self.toSerialisable(result)
        for con in formattedRes:
            for n, v in enumerate(con):
                if type(v) == datetime.date or type(v) == decimal.Decimal or type(v) == datetime.datetime:
                    con[n] = self.json_default(v)

                elif v == None:
                    con[n] = ""

        return formattedRes
