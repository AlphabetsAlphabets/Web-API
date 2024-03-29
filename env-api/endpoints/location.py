from flask_restful import Resource, abort
from QA.database import Database

class Location(Resource):
    """
    This is used by the mobile app to get the location information of our clients. Api key validation is needed.  

    ---
    # Functions
    ### public
    - __init__
    - get

    ### private
    - __info

    """
    def __init__(self):
        """TODO: Add a method for api key validation"""
        pass

    def __info(self):
        """Displays information on every request"""
        banner = "==="*10 + " NEW GET REQUEST " + "==="*10
        print(banner)
        print("Endpoint: location (for mobile app)")
        print("=" * len(banner))

    def get(self):
        """Processes the GET request"""
        self.__info()

        try:
            self.conn, self.cursor = Database.connect("localhost", "root", "-", "tsc_office")
        except Exception:
            self.conn, self.cursor = Database.connect("localhost", "root", "8811967", "tsc_office")
        except Exception:
            abort(404, "The table tlocations is not found. Please create it.")

        sql_query = f"SELECT * FROM tsc_office.tlocations"
        self.cursor.execute(sql_query)
        results = self.cursor.fetchall()
        if len(results) == 0:
            abort(404, message=f"Location does not exist", code="404")
        
        names = []
        lat_one = []
        lon_one = []

        lat_two = []
        lon_two =  []
        for result in results:
            names.append(result[0])
            lat_one.append(result[1])
            lon_one.append(result[2])

            lat_two.append(result[3])

            lon_two.append(result[4])


        response = {
            "name": names,
            "lat_one": lat_one,
            "lon_one": lon_one,
            "lat_two": lat_two,
            "lon_two": lon_two
            }

        return response


        
