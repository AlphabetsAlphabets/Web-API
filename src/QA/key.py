from flask import Flask # pip install flask
from flask_restful import Resource, abort # pip install flask-restful
import mysql.connector

from QA.encrypt import Hash

"""A request to this is made when a new user is created."""
class Key(Resource):
	def __init__(self):
		host = ["localhost", "192.168.1.165"]
		user = ["root", "testuser123"]
		database = ["testing", "testing"]

		out = 0

		PATH = "D:\\python\\Web API\\src\\Files\\sql.txt"
		with open(PATH) as f:
			password = f.readline()

		self.keyTable = mysql.connector.connect(
			host=host[out], 
			user=user[out],
			password=password,
			database=database[out]
		)

		self.keyCursor = self.keyTable.cursor()

	def verify(self, id, key):
		H = Hash(key)
		encrypted = H.encrypt()
		if type(encrypted) == dict:
			return None

		sqlQuery = f"SELECT * FROM testing.creds WHERE id = '{id}' AND keyid = '{encrypted}'"
		self.keyCursor.execute(sqlQuery)
		key = self.keyCursor.fetchall()

		if key is None or len(key) == 0:
			abort(406, message="Incorrect credentials")

		return key[0][0]
