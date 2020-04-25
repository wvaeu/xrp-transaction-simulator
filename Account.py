# Eva Wu, evawu@usc.edu
# Description:this contains the class for updating XRP accounts

class Account(object):
    def __init__(self, public_key, private_key, balance):
        self.__public_key = public_key
        self.__private_key = private_key
        self.__balance = balance

    def get_private_key(self):
        return self.__private_key

    def get_public_key(self):
        return self.__public_key

    def get_balance(self):
        return self.__balance

    def set_balance(self, new_balance):
        self.__balance = new_balance
