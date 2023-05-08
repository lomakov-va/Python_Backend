import bcrypt
passssss = "123" #userInput--это коммент
hashAndSalt = bcrypt.hashpw(passssss.encode(), bcrypt.gensalt())
print('hashAndSalt')
print(hashAndSalt)