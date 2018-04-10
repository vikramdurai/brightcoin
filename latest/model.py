from hashlib import sha256
from urllib import request
from time import time
from random import randint
from json import loads
import sqlite3

# setup variables
targetDifficulty = 4

# initialize the database
conn = sqlite3.connect("db.sqlite3")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS addresses (balance INT, name STRING)")
c.execute("CREATE TABLE IF NOT EXISTS blockchain (parent STRING, msg STRING, hash STRING, nonce INT, _timestamp INT)")
c.execute("CREATE TABLE IF NOT EXISTS transactions (sender STRING, receiver STRING, amount INT)")
conn.commit()
conn.close()

# definition of a block
# (block headers included)
class Block:
    def __init__(self, parent, msg, cachedHash="", timestamp=0, nonce=0):
        # link to the previous block
        self.parent = parent
        # optional message
        self.msg = msg
        # cache
        self._cachedHash = ""
        # unique artifacts
        self.nonce = 0
        self.timestamp = 0
        # transactions list
        self.tx = []
    # the proof-of-work method
    @property
    def hash(self):
        # load the cache
        if self._cachedHash: return self._cachedHash
        # create a 32-bit cryptographically
        # random number to ensure a random hash
        nonce = randint(0, 2**16)
        timestamp = 0
        # create an empty hash
        h = sha256()
        # while the hash is not a valid proof
        while not h.hexdigest()[:targetDifficulty] == ("0" * targetDifficulty):
            # regenerate the hash...
            h = sha256()
            # ...and populate it with random stuff
            h.update(bytes(self.msg
                    + str(nonce)
                    + str(timestamp)
                    + str(self.parent)
                    + str(randint(0, 2**32)), "utf8"))
            # change the nonce
            nonce += 1
            # change the timestamp
            timestamp = int(time())
            ##debug
            print("%s" % h.hexdigest(), end="\r")
        # the hash is finally a valid proof
        # so update the cache
        self._cachedHash = h.hexdigest()
        # also update the artifacts
        self.nonce = nonce
        self.timestamp = timestamp
        # return the hash
        return h.hexdigest()

# create the Genesis Block and hash it
# the genesis block is the only block in the
# system to have no block before it
genesisBlock = Block(None, "Genesis Block!")
if genesisBlock.hash: pass

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending = []
        self.chain.append(genesisBlock)
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute("INSERT INTO blockchain VALUES (?, ?, ?, ?, ?)", (
                    str(self.chain[-1].parent),
                    self.chain[-1].msg,
                    str(self.chain[-1].hash),
                    str(self.chain[-1].nonce),
                    str(self.chain[-1].timestamp)))
        conn.commit()
        conn.close()

    # create a new transaction
    # by adding it to the waiting list of
    # transactions to be verified
    def tx(self, sender, receiver, amount):
        self.pending.append({
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        })
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute("INSERT INTO transactions VALUES (?, ?, ?)", (sender, receiver, amount))
        conn.commit()
        conn.close()

# bc is the one and only Blockchain
bc = Blockchain()

class Address:
    def __init__(self, name, balance=0):
        # the amount of money in this account
        self.balance = balance
        # unique address id
        # used when paying
        self.name = name
        # list of available peers
        # to make transactions with
        self.peers = []

    def add_peer(self, p, op):
        if p in self.peers:
            return
        x = loads(request.urlopen("http://localhost:"+p+"/self").read().decode())
        a = Address(x["name"], x["balance"])
        a.peers = x["peers"]
        a.save()
        a.add_peer(op)
        
        

    # adds the new address to the list
    def save(self):
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute("INSERT INTO addresses VALUES (?, ?)", (self.balance, self.name))
        conn.commit()
        conn.close()

    # update its counterpart in the database
    def update(self):
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute("UPDATE addresses SET balance = ?, name = ? WHERE name == ?", (self.balance, self.name, self.name))
        conn.commit()
        conn.close()

    # registers a transaction in the blockchain
    def pay(self, other_address, amount):
        # you must have enough coins in your account
        # first
        assert self.balance >= amount, "you don't have enough coins"
        # also, the other address must be valid
        assert findAddress(other_address.name), "receiving address doesn't exist"
        # then register the transaction
        bc.tx(self.name, other_address.name, amount)

    # mining generates new blocks
    # and validates transactions
    def mine(self, msg=""):
        # create a block and hash it
        b = Block(bc.chain[len(bc.chain)-1].hash, msg)
        if b.hash: pass
        # empty the transaction list
        # into the freshly created block
        b.tx = bc.pending
        # validate the transactions
        for i in b.tx:
            # make sure they're both valid addresses
            assert findAddress(i["sender"]), "sending address does not exist"
            assert findAddress(i["receiver"]), "receiving address does not exist"
            # get the addresses
            s = findAddress(i["sender"])
            r = findAddress(i["receiver"])
            # perform the transaction
            s.balance -= i["amount"]
            r.balance += i["amount"]
            # and refresh their counterparts in the database
            s.update()
            r.update()
            # update the transaction history
            conn = sqlite3.connect("db.sqlite3")
            c = conn.cursor()
            c.execute("INSERT INTO transactions VALUES (?, ?, ?)", (i["sender"], i["receiver"], i["amount"]))
            conn.commit()
            conn.close()

        # add it to the chain
        bc.chain.append(b)

        # update the database
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute("INSERT INTO blockchain VALUES (?, ?, ?, ?, ?)", (
                    str(bc.chain[-1].parent),
                    bc.chain[-1].msg,
                    str(bc.chain[-1].hash),
                    str(bc.chain[-1].nonce),
                    str(bc.chain[-1].timestamp)))
        conn.commit()
        conn.close()
        # clear the waiting list
        bc.pending = []
        # and reward the miner
        self.balance += 100
        self.update()

# factory function to make it easier to create addresses
def newAddress():
    h = sha256()
    h.update(bytes(str([randint(0, 2**16), randint(0, 2**32), int(time())]), "utf8"))
    a = Address("BRIGHT"+h.hexdigest())
    a.save()
    return a

# simple function to get addresses
# from the database
def findAddress(n):
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT * FROM addresses WHERE name == \"%s\"" % n)
    r = c.fetchone()
    conn.commit()
    conn.close()
    if r:
        return Address(r[1], r[0])
    else:
        return None

# simple function to get
# the transaction history
def txHistory():
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT * FROM transactions")
    r = c.fetchall()
    conn.commit()
    conn.close()
    return [{"sender": i[0], "receiver": i[1], "amount": i[2]} for i in r]