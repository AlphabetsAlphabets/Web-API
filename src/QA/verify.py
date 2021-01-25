import mysql.connector
from QA.encrypt import Hash
from flask_restful import abort

class ApiKey:
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

    def getKey(self):
        sqlQuery = "SELECT * FROM `testing`.`key`"
        self.keyCursor.execute(sqlQuery)
        resKey = self.keyCursor.fetchall()
        encryptedKey = resKey[0][0]
        key = Hash(encryptedKey).decrypt() 
        
        return key

    def verifyKey(self, hash):
        value = Hash(hash).encrypt()

        sqlQuery = "SELECT * FROM `testing`.`key`"
        self.keyCursor.execute(sqlQuery)
        resKey = self.keyCursor.fetchall()
        key = resKey[0][0]

        if key != value:
            abort(406, message = "Incorrect API key.")
        
        return True