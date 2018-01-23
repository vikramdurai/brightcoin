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
        # the hash is finally a valid proof!
        # so update the cache
        self._cachedHash = ""
        # also update the artifacts
        self.nonce = nonce
        self.timestamp = timestamp
        # return the hash
        return h.hexdigest()
