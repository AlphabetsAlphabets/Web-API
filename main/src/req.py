import requests
import json

host = "http://192.168.1.134:5000/update"
data = {"data": "axe"}

r = requests.post(host, data)
print(r.json())