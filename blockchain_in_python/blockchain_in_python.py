import hashlib
import random
import Crypto.PublicKey.RSA
import Crypto.Signature.pkcs1_15
import Crypto.Hash.SHA384

class Block:
    def __init__(self,prev_hash,transactions):
        self.transactions=transactions
        self.prev_hash=prev_hash
        self.data=str(transactions)+prev_hash
        self.hash=hashlib.sha256(self.data.encode()).hexdigest()


class User:
    private_key: int
    public_key: int
    def __init__(self, name, private_key, public_key, credit):
         self.name = name
         self.private_key = private_key
         self.public_key = public_key
         self.credit = credit

users: list[User]=[]
blocks=[]
transactions=[]

with open('names.txt','r') as names:
    names=names.readlines()
    for user in range(20):
        users.append(User(random.choice(names), Crypto.PublicKey.RSA.generate(1024), Crypto.PublicKey.RSA.generate(1024), 1000))

for i in range(10):
    for j in range(5):
        user=users[random.randint(0,19)]
        number=random.randint(1,100)
        if user.credit-number>=0:
            message=f"{user.name} gives {number} GHOUL to {users[random.randint(0,19)]}"
            message=Crypto.Hash.SHA384.new(message.encode())
            transactions.append(Crypto.Signature.pkcs1_15.new(user.private_key).sign(message))
    if len(blocks)>0:
        blocks.append(Block(blocks[i-1].hash,transactions))
    else:
        blocks.append(Block("",transactions))
for block in blocks:
    print(block.hash,block.prev_hash)