from flask_restful import Resource, abort
from typing import Union, Iterable
from QA.database import Database as Db
from mysql.connector.errors import ProgrammingError

"""
This is only relevant if you're using an IDE such as Visual Studio Code(VSC), Visual Studio(VS), PyCharm(PC), etc. Or
a very powerful text editor like sublime text (sub).

If you don't understand how a function works. Click on the function name then press
alt + F12(VSC)/F12(sub) to view the function definition to look at the logic. (I do not use PyCharm, and do not know it's associated shortcut.)
Within the definition there will be doc strings documenting what each function is supposed to do.

"""

class Spec(Resource):
    def __init__(self):
        self.conn, self.cursor = Db().connect("localhost", "root", "YJH030412yjh_g", "testing")

        self.BASE_QUERY = "SELECT * FROM testing.spec"

    def get(self, table: str, o1: Union[str, int], o2: Union[str, int], o3: Union[str, int], o4: Union[str, int], o5: Union[str, int]) -> str:
        """Collects all the parameters into a list. Then filters out unwanted values."""
        initialParams = [o1, o2, o3, o4, o5] 
        filteredParams = list(filter(self.removeNone, initialParams)) # removes all empty values ("n")
        noneIndices = [i for i, v in enumerate(initialParams) if v == "n"]
        noneIndices.sort(reverse=True) # Reverse it so that when deleting values from lists, via indices the program won't throw an IndexError exception
        
        """Makes a request to the SQL database which returns None intentionally, as this is required in order to get the column names"""
        silent = f"{self.BASE_QUERY} WHERE table_name = 'silent'"  
        self.cursor.execute(silent)
        _ = self.cursor.fetchall()

        """The actual query to be made, to get the associated SQL query to get data for that specific table."""
        sqlQuery = f"{self.BASE_QUERY} WHERE table_name = '{table}'"
        self.cursor.execute(sqlQuery)
        res = self.cursor.fetchall()

        desc = self.cursor.description
        """Starts from the 2nd index, because the first two column names are: table_name and sql. Which is not needed."""
        names = [des[0] for des in desc][2:]
        parameters = {k: v for k, v in zip(names, filteredParams)}

        if len(res) == 0:
            abort(404, message = f"{table} does not exist.")

        formattedRes = Db().toSerialisable(res)
        conditionals = list(filter(self.removeNone, formattedRes[0]))[2:]
        """Deletes unneeded parameters from the list so it won't be added into a SQL query."""
        for i in noneIndices:
            del conditionals[i]

        keyValuePairs = {k: v for k, v in zip(filteredParams, conditionals)}

        whereQuerySnippets = []
        for value, k in zip(filteredParams, parameters):
            con, v = keyValuePairs[value], parameters[k]
            whereQuerySnippets.append(f"{con} = '{v}'")
        
        stitchedWhereQuery= (" AND ").join(whereQuerySnippets)
        stitchedQuery = f"SELECT * FROM testing.{table} WHERE {stitchedWhereQuery}"

        """The part where the api makes another SQL query on your behalf"""
        _ , redirCursor = Db().connect("localhost", "root", "YJH030412yjh_g", "testing")
        redirCursor.execute(stitchedQuery)

        redirRes = redirCursor.fetchall()
        lengthOfRedirRes = len(redirRes)

        """Handles the part with more than one result"""
        if lengthOfRedirRes > 1:
            tempConn, tempCursor = Db().connect("localhost", "root", "YJH030412yjh_g", "testing")
            silent = tempCursor.execute("SELECT * FROM testing.trans")
            _ = tempCursor.fetchall()
            

            serialisedRedirRes = Db().formatEntries(redirRes)

            return serialisedRedirRes

        elif lengthOfRedirRes == 0:
            abort(404, message = "No entries with the specified information found.")

        serialisedRedirRes = Db().formatEntries(redirRes)

        """Makes a key value pair to the appriroiate value. For it to be clearer."""
        keyValuePairOfSerialisedRedirRes = Db().keyValuePairing(redirCursor, serialisedRedirRes)

        return keyValuePairOfSerialisedRedirRes

    def removeNone(self, value: Union[str, int]) -> Union[str, int]:
        """Meant to use with the filter function, to remove all None values"""
        if value != "n" and value != None:
            return value 