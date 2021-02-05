import requests
import base64
import time

startTime = time.time()
with open(".\\Files\\imgur.txt") as f:
    clientId, clientSecret= f.readlines()

with open(".\\Files\\img.jpg", "rb") as file:
    url = "https://api.imgur.com/3/image"

    payload = {
        'image': base64.b64encode(file.read()),
        "title": "first post",
        "name": "animal",
        "in_gallery" : True
        }

    ID = clientId.strip("\n")

    headers = {
        "Authorization": f"Client-ID {ID}",
    }

    files = {
        "name": file
    }

    r = requests.request("POST", url, headers=headers, data=payload, files=files)

data = r.json()
link = data["data"]["link"]
r = requests.get(link)
with open(".\\Files\\copy.png", "wb") as f:
    f.write(r.content)

print("Download complete, it took {0}".format(time.time() - startTime))
