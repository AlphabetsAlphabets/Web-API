from QA import Database

from mysql.connector.cursor import MySQLCursor as TYPE_CURSOR
from mysql.connector.connection import MySQLConnection as TYPE_SQL_CONN

class Statement:
    def formatEntries(self, result: list) -> list:
        """Converts any MySQL database types to native python types that are also serializable.

        ---
        # Parameters
        ### result 
        The list of results from successfull execution of a mysql query \
        from `self.cursor.fetchall()`.
        """
        formattedRes = self.toSerialisable(result)
        for con in formattedRes:
            for n, v in enumerate(con):
                returnValue = self.json_default(v)
                if returnValue is not None:
                    con[n] = returnValue

                elif v == None:
                    con[n] = ""

        return formattedRes

    def getColumnNames(names: list) -> str:
        """
        Takes in a list of column names, and stiches them together to form a string of all the column names.

        ---
        # Parameters
        ### names
        A list of column names.

        ---
        # Example
        ```python3
        names = ["monthly income", "name", "position"]
        result = Database.getColumnNames(names)
        print(result) # monthly income, name, position
        ```
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

        ---
        # Example
        ```python3
        names = ["Monday", "Tuesday", "Wednesday"]
        result = Database.columnNamesForInsert(cursor, names)
        print(result) # "`columnOne` = Monday, `columnTwo` = "Tuesday", `columnThree` = "Wednesday"
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

