from hashlib import sha256
from time import time
from random import randint

# setup variables
targetDifficulty = 4

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

    # create a new transaction
    # by adding it to the waiting list of
    # transactions to be verified
    def tx(self, sender, receiver, amount):
        self.pending.append({
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        })

    # mining generates new blocks
    # and validates transactions
    def mine(self, msg=""):
        # create a block and hash it
        b = Block(self.chain[len(self.chain)-1].hash, msg)
        if b.hash: pass
        # empty the transaction list
        # into the freshly created block
        b.tx = self.pending
        self.pending = []
        # validate the transactions
        for i in b.tx:
            # make sure they're both valid addresses
            assert findAddress(i["sender"]), "sending address does not exist"
            assert findAddress(i["receiver"]), "receiving address does not exist"
            # find the addresses
            s = findAddress(i["sender"])
            r = findAddress(i["receiver"])
            # perform the transaction
            s.balance -= i["amount"]
            r.balance += i["amount"]
            # update the transaction history
            s.tx.append(i)
            r.tx.append(i)
            # and refresh their counterparts in the addresses
            # list
            s.update()
            r.update()

        # add it to the chain
        self.chain.append(b)

# bc is the one and only Blockchain
bc = Blockchain()
# list of addresses to keep track of
addresses = []

class Address:
    def __init__(self, name, balance=0, tx=[]):
        # stores the transaction history
        self.tx = tx
        # the amount of money in this account
        self.balance = balance
        # unique address id
        # used when paying
        self.name = name
        # id in the addresses list
        # not used when paying
        self._id = 0

    # adds the new address to the list
    def register(self):
        addresses.append(self)
        self._id = len(addresses)-1

    # update its counterpart in the array
    # Side note: I really wish Python had optional
    # pointers.
    def update(self):
        addresses.pop(self._id)
        addresses.insert(self._id, self)

    # registers a transaction in the blockchain
    def pay(self, other_address, amount):
        # you must have enough coins in your account
        # first
        assert self.balance >= amount, "you don't have enough coins"
        # also, the other address must be valid
        assert findAddress(other_address.name), "receiving address doesn't exist"
        # then register the transaction
        bc.tx(self.name, other_address.name, amount)

def newAddress():
    h = sha256()
    h.update(bytes(str([randint(0, 2**16), randint(0, 2**32), int(time())]), "utf8"))
    a = Address(h.hexdigest())
    a.register()
    return a

def findAddress(n):
    r = [i for i in addresses if i.name == n]
    if len(r):
        return r[0]
    else:
        return None