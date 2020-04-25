# Eva Wu, evawu@usc.edu
# Description: this python file stores the transaction class which writes to the ledger

import hashlib
import datetime

class Transaction(object):
    def __init__(self, data, prev_hash):
        self.__date = datetime.datetime.now()  # timestamp
        self.__data = data  # transaction notes
        self.__prev_hash = prev_hash  # hash of previous block
        self.__hash = self.hash()  # creates a unique cryptographic hash
        self.write_ledger()  # calls the write_ledger function

    # create a unique encrypted hash for a block object
    def hash(self):
        # use sha256() algorithm to create a SHA-256 hash object
        hash_object = hashlib.sha256()
        # use update() method to feed block data into SHA-256 hash object
        # unicode-objects must be encoded before hashing using .encode()
        hash_object.update(str(self.__date).encode('utf-8') +
                           str(self.__data).encode('utf-8') +
                           str(self.__prev_hash).encode('utf-8'))
        # use hexdigest() to encrypt data passed in through update() as a hex-encoded string
        return hash_object.hexdigest()

    # use class method to manually create the first dummy transaction in ledger
    @classmethod
    def create_genesis(cls):
        return cls("First entry to initialize ledger", "N/A")

    # write transaction details to txt file
    def write_ledger(self):
        fileOut = open("XRP-Ledger.txt", "a")  # open Ledger file for appending
        print(str(self.__date) + "\n" + str(self.__data) + "\n\nHash: " +
              str(self.__hash) + "\nPrevious Hash: " + str(self.__prev_hash) +
              "\n==========================================================================================", file=fileOut)
        fileOut.close()

    def get_data(self):
        return self.__data

    def get_date(self):
        return self.__date

    def get_hash(self):
        return self.__hash

    def get_prev_hash(self):
        return self.__prev_hash
