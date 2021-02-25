from typing import Union

from flask_restful import Resource, abort  # pip install flask-restful
from mysql.connector.errors import ProgrammingError

from QA.database import Database
from QA.encrypt import Hash

from werkzeug.exceptions import ServiceUnavailable as TYPE_SERVICE_UNAVAILABLE

"""A request to this is made when a new user is created."""
class Key(Resource):
	def __init__(self):
		self.schema = "testing"
		self.table = "creds"
		try:
<<<<<<< HEAD
			self.keyTable, self.keyCursor = Database().connect("localhost", "root", "YJH030412yjh_g", "testing")
		except TYPE_SERVICE_UNAVAILABLE:
			abort(503, message="Unable to connect to database. Due to incorrect credentials.")
=======
			self.keyTable, self.keyCursor = Database.connect("localhost", "root", "YJH030412yjh_g", self.schema)
		except ProgrammingError as err:
			abort(503, message="Unable to connect to database. Check your credentials.")
>>>>>>> b96324ce21cc65cc8aaec772c77625dd8f039be6

	def getKey(self, user: str, password: Union[str, int]) -> str:
		print(f"Params: user {user}, password {password}")
		"""Checks to see if the password matches the one in the database. If it does then it returns
		a key and an auth level. If not, throws an error."""

		encrypted = Hash.encrypt(password)
		print(f"Encrypted: {encrypted}")

		sqlQuery = f"SELECT * FROM {self.schema}.{self.table} WHERE user = '{user}' AND password = '{encrypted}'"
		print(f"SQL Query: {sqlQuery}")
		self.keyCursor.execute(sqlQuery)
		key = self.keyCursor.fetchall()

		if key is None or len(key) == 0:
			abort(406, message="Incorrect credentials")

		return encrypted, key[0][0]

	def verifyKey(self, user: str, key: str) -> bool:
		"""
		Goes through the database, with user, and key as conditionals. To verify if this unique key belongs
		to this particular user.	
		"""
<<<<<<< HEAD
		sqlQuery = f"SELECT * FROM testing.creds WHERE apikey = '{key}' AND user = '{user}'"
		print("==="*20)
		print(f"sqlQuery: {sqlQuery}")
=======
		sqlQuery = f"SELECT apikey FROM {self.schema}.{self.table} WHERE user = '{user}'"
>>>>>>> b96324ce21cc65cc8aaec772c77625dd8f039be6
		self.keyCursor.execute(sqlQuery)

		realKey = self.keyCursor.fetchall()
		if len(realKey) == 0:
			abort(406, message = f"Invalid API key for user: {user}")
		elif key == realKey[0][0]:
			return True
