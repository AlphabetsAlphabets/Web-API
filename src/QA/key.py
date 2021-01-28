from typing import Union
from flask import Flask # pip install flask
from flask_restful import Resource, abort # pip install flask-restful

from QA.encrypt import Hash
from QA.database import Database

"""A request to this is made when a new user is created."""
class Key(Resource):
	def __init__(self):
		host = ["localhost", "192.168.1.165"]
		user = ["root", "testuser123"]
		database = ["testing", "testing"]

		o = 0

		PATH = "D:\\python\\Web API\\src\\Files\\sql.txt"
		with open(PATH) as f:
			password = f.readlines()
		
		self.keyTable, self.keyCursor = Database().connect(host[o], user[o], password[o], database[o])

	def verify(self, user: str, password: Union[str, int]) -> str:
		print(password)
		H = Hash(password)
		encrypted = H.encrypt()
		if type(encrypted) == dict:
			return None

		sqlQuery = f"SELECT * FROM testing.creds WHERE user = '{user}' AND apikey = '{encrypted}'"
		print(sqlQuery)
		self.keyCursor.execute(sqlQuery)
		key = self.keyCursor.fetchall()

		if key is None or len(key) == 0:
			abort(406, message="Incorrect credentials")

		return key[0][0]

	def verifyKey(self, key: str) -> None:
		sqlQuery = f"SELECT * FROM testing.creds WHERE apikey = '{key}'"
		self.keyCursor.execute(sqlQuery)
		key = self.keyCursor.fetchall()

		if key is None or len(key) == 0:
			return False
