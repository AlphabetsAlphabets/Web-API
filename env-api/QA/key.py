from typing import NoReturn, Union

from flask_restful import Resource, abort  # pip install flask-restful
from mysql.connector.errors import ProgrammingError

from QA.database import Database
from QA.encrypt import Hash

from werkzeug.exceptions import ServiceUnavailable as TYPE_SERVICE_UNAVAILABLE

"""A request to this is made when a new user is created."""
class Key(Resource):
	def __init__(self):
		try:
			self.keyTable, self.keyCursor = Database().connect("localhost", "root", "YJH030412yjh_g", "testing")
		except TYPE_SERVICE_UNAVAILABLE:
			abort(503, message="Unable to connect to database. Due to incorrect credentials.")

	def getKey(self, user: str, password: Union[str, int]) -> str:
		"""Checks to see if the password matches the one in the database. If it does then it returns
		a key and an auth level. If not, throws an error."""

		H = Hash(password)
		encrypted = H.encrypt()
		if type(encrypted) == dict:
			return None

		sqlQuery = f"SELECT * FROM testing.creds WHERE user = '{user}' AND password = '{encrypted}'"
		print(sqlQuery)
		self.keyCursor.execute(sqlQuery)
		key = self.keyCursor.fetchall()

		if key is None or len(key) == 0:
			abort(406, message="Incorrect credentials")

		return encrypted, key[0][0]

	def verifyKey(self, user: str, key: str) -> NoReturn:
		"""
		Goes through the database, with user, and key as conditionals. To verify if this unique key belongds
		to this particular user.	
		"""
		sqlQuery = f"SELECT * FROM testing.creds WHERE apikey = '{key}' AND user = '{user}'"
		print("==="*20)
		print(f"sqlQuery: {sqlQuery}")
		self.keyCursor.execute(sqlQuery)

		key = self.keyCursor.fetchall()

		if key is None or len(key) == 0:
			abort(406, message = f"Invalid API key for user: {user}")
