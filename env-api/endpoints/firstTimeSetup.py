"""This endpoint is used by the mobile to configure a first time setup."""

from flask_restful import Resource
from PIL import Image

# Documentation needed
class FirstTimeSetup(Resource):
    def get(self):
        image = Image.open("env-api/endpoints/images/logo.png")
        imageByteArray = list(image.tobytes())
        return {"image": imageByteArray}