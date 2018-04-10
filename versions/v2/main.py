from hashlib import sha256
from time import time
from random import randint

# setup variables
targetDifficulty = 4

# definition of a block
# (block headers included)
class Block:
    # extra arguments because in the future we may use this as
    # a data class
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
            timestamp = time()
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
        # add it to the chain
        self.chain.append(b)