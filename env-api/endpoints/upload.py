"""
This endpoint is used for the mobile app, to upload pictures to the server. 
"""
from flask_restful import Resource, abort, reqparse
from werkzeug.datastructures import FileStorage

from PIL import Image
from QA.database import Database

import os
import datetime


"""
Either an additional column (or dedicated) table is needed to store the path to the images.
VARCHAR(250) recommended.
"""

class Upload(Resource):
    """Handles uploading images to the server. This endpoint is used by the mobile app specifically.

    ---
    # Functions
    ### public
    - __init__
    - put

    ### private
    - __info
    - __startup
    """
    def __init__(self):
        """Handles initialization, and connects to the database"""

        password = Database.getPassword()
        try:
            self.conn, self.cursor = Database.connect("localhost", "root", password[0], "testing")
            self.schema = "testing" 
            self.table = "images"
        except Exception:
            self.conn, self.cursor = Database.connect("localhost", "root", password[1], "tsc_office")
            self.schema = "tsc_office"
            self.table = "timages"

        parser = reqparse.RequestParser()
        parser.add_argument("image", type=FileStorage, location="files")

        self.parsed = parser.parse_args()

        try:
            path = "../src/images/"
            os.chdir(path)
            print("CHANGED PATH")
        except Exception:
            pass

    def __info(self, image: Image):
        """This just outputs information regarding the image itself. Useful during debugging.

        ---
        # Parameters
        ### image
        An instance of the Image class from the PIL library 
        """
        print(f"content_length: {image.content_length}")
        print(f"content_type: {image.content_type}")
        print(f"filename: {image.filename}")
        print(f"headers: {image.headers}")
        print(f"mimetype: {image.mimetype}")
        print(f"mimetype_params: {image.mimetype_params}")
        print(f"name: {image.name}")
        print(f"stream: {image.stream}")


    def __resize(self, dim: tuple) -> tuple:
        """Resizes the image according to a threshold
        
        ---
        # Parameters
        ### dim
        A tuple with the width and height of an image. In that exact order."""
        width, height = dim

        value = max(width, height)
        if (value > 2000):
            ratio = 2000 / value
            newWidth = width * ratio
            newHeight = height * ratio

            return (int(newWidth), int(newHeight))

        return dim

    def __startup(self, saveName: str):
        """Shows startup information, including what type of request, and which endpoint it is from to save time searching through
        each endpoint individually.
        
        ---
        # Parameters
        ### saveName
        The name of the image.
        """
        print("\n")
        banner = "=="*20 + " NEW PUT REQUEST " + "=="*20

        print(banner)
        print("- API: Upload")
        print(f"Current date and time: {datetime.datetime.now()}")
        print("\n" + f"saveName: {saveName}")
        print("=" * len(banner))

    def put(self, saveName):
        """Processes the PUT request.
        
        ---
        # Parameteres
        ### saveName
        The image's name"""
        # imageSave = os.getcwd() + f"\\{saveName}.jpg"
        imageSave = os.getcwd() + f"\\src\\images\\{saveName}.jpg"
        print(imageSave)
        print("PUT")
        self.__startup(saveName)

        saveName = saveName.strip(".jpg").strip(".jpeg")

        image = self.parsed["image"]
        if image is None:
            abort(406, message="You have not uploaded an image.", code=406)
        # self.__info(image)


        rawImage = Image.open(image.stream)

        dim = (int(rawImage.width), int(rawImage.height))

        newDim = self.__resize(dim)

        try:
            resized = rawImage.resize(newDim, Image.ANTIALIAS)
            resized.save(imageSave)
            imageSave = ""
        except (OSError, FileNotFoundError):
            resized.convert("RGB").save(imageSave)

        # add path to my sql
        pathToImage = (os.getcwd() + f"\\src\\images\\{saveName}.jpg").split("\\")
        sqlCompliantPath = ("/").join(pathToImage)

        sqlQuery = f"INSERT INTO {self.schema}.{self.table} (`image name`, `image path`) VALUES ('{saveName}', '{sqlCompliantPath}')"
        self.cursor.execute(sqlQuery)
        self.conn.commit()

        return {"success": "image succesfully uploaded"}

