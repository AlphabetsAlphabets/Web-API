from typing import Union

from flask_restful import Resource, abort  # pip install flask-restful
from mysql.connector.errors import ProgrammingError

from QA.database import Database
from QA.encrypt import Hash

"""
Add a new column to the table tsc_office.tap, called api key or something similar. So there is no need to create a new table when verifying a user's
api key
"""

class Key(Resource):
	"""
	This class is used to retrieve, and verify a user's unique api key.

	---
	# Functions
	- __init__
	- getKey
	- verifyKey

	"""
	def __init__(self):
		self.schema = "testing"
		self.table = "creds"
		try:
			self.keyTable, self.keyCursor = Database.connect("localhost", "root", "-", self.schema)
		except ProgrammingError as err:
			abort(503, message="Unable to connect to database. Check your credentials.")

	def getKey(self, user: str, password: Union[str, int]) -> str:
		"""
		Retrieve the user's unique api key 

		---
		# Parameters
		### user
		The username

		### password
		The password of the user

		"""
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

		---
		# Parameters
		### user
		The user's name

		### key
		The user's unique api key
		"""
		sqlQuery = f"SELECT apikey FROM {self.schema}.{self.table} WHERE user = '{user}'"
		self.keyCursor.execute(sqlQuery)

		realKey = self.keyCursor.fetchall()
		if len(realKey) == 0:
			abort(406, message = f"Invalid API key for user: {user}", inside="key.py")

		elif key == realKey[0][0]:
			return True

		else:
			return False
