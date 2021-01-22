from flask import Flask # pip install flask
from flask_restful import Resource # pip install flask-restful

class Key(Resource):
	def __init__(self):
		with open("pass.txt") as f:
			self.correct = f.readline()

	def get(self):
		return self.correct

	def grabber(self):
		with open("pass.txt") as f:
			data = f.readline()

		return data


