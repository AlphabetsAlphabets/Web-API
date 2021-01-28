import mysql.connector
import decimal, datetime
from typing import Iterable, Union 
from mysql.connector.cursor import MySQLCursor as CURSOR

class Database:
    def getColumnNames(names):
        blank = ""
        for name in names:
            if name == names[0]:
                blank += name
            elif name == names[-1]:
                blank += ", " + name
            else:
                blank += ", " + name
                    
    def connect(self, host, user, password, database):
        connection = mysql.connector.connect(
            host = host, user = user, password = password,
            database=  database
        )
        print(type(connection))

        cursor = connection.cursor()
        return connection, cursor

    def json_default(self, value: Union[decimal.Decimal, datetime.date]) -> str: 
        if isinstance(value, decimal.Decimal):
            return str(float(value)) + "0"
            
        elif isinstance(value, datetime.date):
            return value.strftime("%Y-%m-%d")

        raise TypeError('not JSON serializable') #you may choose not to raise the Error though 

    def toSerialisable(self, data: Union[list, tuple]) -> list:
        data = [list(c) for c in data]

        return data

    def keyValueParing(self, cursor: CURSOR, res: list) -> dict:
        description = cursor.description # Gets all the column names
        desc = [description[c][0] for c, _ in enumerate(description)] # Storing all the column names into a list, previously = (fid, 0, 0, 0) after formatting = fid
        keyValuePairs = {k: v for k, v in zip(desc, res[0])} # Dictionary comprehension, with column names (desc) as a key, and the values (res) as its vaue.
        for k in keyValuePairs:
            if keyValuePairs[k] == None:
                keyValuePairs[k] = ""

        return keyValuePairs