import QA

H = QA.Hash("ABC123")
out = H.encrypt()
print(out)

dec = H.decrypt(out)
print(dec)
