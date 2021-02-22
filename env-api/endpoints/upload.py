from flask_restful import Resource, abort, reqparse
from werkzeug.datastructures import FileStorage
from PIL import Image
from QA.database import Database
import os
import shutil

# Types
from PIL.JpegImagePlugin import JpegImageFile as TYPE_JPEG_IMAGE
from PIL.Image import Image as TYPE_IMAGE

"""
Either an additional column (or dedicated) table is needed to store the path to the images.
VARCHAR(250) recommended.
"""

class Upload(Resource):
    def __init__(self):
        self.schema = "testing"
        self.table = "images"

        self.conn, self.cursor = Database.connect("localhost", "root", "YJH030412yjh_g", self.schema)

        parser = reqparse.RequestParser()
        parser.add_argument("image", type=FileStorage, location='files')
        parser.add_argument("width", type=str, location="headers")
        parser.add_argument("height", type=str, location="headers")

        self.parsed = parser.parse_args()

    def put(self, name):
        path = f"../src/images/"
        imageName = path + f"{name}.jpg" # New image name.

        image = self.parsed["image"]
        width = self.parsed["width"]
        height = self.parsed["height"]

        if width is None or height is None:
            abort(406, message="Please provide a valid width or height. It cannot be empty.")

        dim = (int(width), int(height))

        rawImage = Image.open(image)

        # Decompress
        resized = rawImage.resize(dim, Image.ANTIALIAS)
        resized.save(imageName)

        # add path to my sql
        os.chdir(path)
        pathToImage = (os.getcwd() + f"\\{name}.jpg").split("\\")
        sqlCompliantPath = ("\\\\").join(pathToImage)

        sqlQuery = f"INSERT INTO {self.schema}.{self.table} (`image name`, `image path`) VALUES ('{name}', '{sqlCompliantPath}')"
        self.cursor.execute(sqlQuery)
        self.conn.commit()

        return {"200": "image succesfully uploaded"}

