# Eva Wu, evawu@usc.edu
# Description: this program runs the XRP transaction simulation

from Account import Account
from Transaction import Transaction
from bs4 import BeautifulSoup
import requests

# web scrape to find XRP price
def get_price():
    # sends request using get function in request library using a url, returns data object of search results
    data = requests.get("https://www.google.com/search?q=xrp+price")
    # pass html of data object into BeautifulSoup object, while specifying to parse as html
    soup = BeautifulSoup(data.text, 'html.parser')
    # find div (tag type in html) on page containing xrp price
    ans = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")[3].text  # get it as text
    # return answer excluding $ sign and as float
    return float(ans[1:])

# check if private key exists
def get_public(private_key):
    fileIn = open("XRP-test-accounts.txt", "r")
    for line in fileIn:
        line = line.strip()  # removes trailing and leading whitespace
        account = line.split(",")  # separate address from secret to put in list
        if private_key == account[1]:
            fileIn.close()
            return True
    fileIn.close()
    return False

# didn't need to be a function but idk it's kinda ugly
def view_menu():
    print("\n          ●▬▬▬▬▬๑۩۩๑▬▬▬▬▬●"
          "\n       1) View account details"
          "\n       2) Buy XRP"
          "\n       3) Send XRP"
          "\n       4) Receive XRP"
          "\n       5) View transaction history"
          "\n       6) Logout"
          "\n          ●▬▬▬▬▬๑۩۩๑▬▬▬▬▬●\n")

def main():
    # create an account object for every line in file and add to dictionary
    accounts = {}
    fileIn = open("XRP-test-accounts.txt", "r")
    fileIn.readline()
    for line in fileIn:
        line = line.strip()  # removes trailing and leading whitespace
        acc = line.split(",")  # separate address from secret to put in list
        accounts[acc[0]] = Account(acc[0], acc[1], float(acc[2]))
    fileIn.close()

    # create a list to keep track of transaction hashes made during this program session
    fileIn = open("XRP-Ledger.txt", "r")
    # create genesis block if none exists in ledger
    if not fileIn.readline().strip():  # check if first line of the file is empty
        prev_hash = Transaction.create_genesis().get_hash()  # make genesis hash prev hash
    else:
        # loop through hashes and overwrite last_hash until end of file, ending up with most recent hash
        last_hash = ""
        for line in fileIn:
            if line[:4] == "Hash":
                last_hash = line[6:].strip()
        prev_hash = last_hash
    fileIn.close()

    print("°º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸\n       Welcome to your XRP Wallet\n°º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸")
    # get XRP rate from cached google result (last close price from previous day)
    XRP_rate = get_price()
    private_key = input("\nTo begin, please enter your Private Key (see XRP-test-accounts): ").strip()
    # check private key exists in error check
    user_public_key = ""
    # loop while private key is not found (i.e. if public key was not set)
    while not user_public_key:
        for key in accounts:
            if accounts[key].get_private_key() == private_key:  # (account object).getter()
                user_public_key = key
        if not user_public_key:
            private_key = input("\nInvalid Private Key, please try again: ").strip()
    print("       ʕ·͡ᴥ·ʔ Successful login! ʕ·͡ᴥ·ʔ\nServices available to you:")
    choice = 0
    while choice != 6:
        view_menu()  # display menu items
        choice = input("What would you like to do today (1-6)?: ").strip()
        while not choice or not choice.isnumeric() or int(choice) < 0 or int(choice) > 6:  # check valid input
            choice = input("Invalid choice, must be a number between 1-6: ")
        choice = int(choice)
        if choice == 1:  # display account details
            print("\n💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰" +
                  "\nYour private key is: " + str(private_key) +
                  "\nYour public key is: " + str(user_public_key) +
                  "\nYour account balance is: " + str(accounts[user_public_key].get_balance()) +
                  "\n💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰")
        elif choice == 2:  # buy XRP
            print("1 XRP = " + str(XRP_rate) + " USD")
            USD_amount = input("How much would you like to buy? (USD): ").strip()
            # error check input
            while not USD_amount or not USD_amount.isnumeric() or float(USD_amount) <= 0 or float(USD_amount) > 1000000:
                USD_amount = input("Invalid input, enter an amount between 0-1mil(USD): ").strip()
            XRP_amount = (float(USD_amount)/XRP_rate).__round__(6)
            print("You have purchased "+ str(XRP_amount) + " XRP for\n" + str(USD_amount) + " USD")
            # update and return new acc balance in account.py
            accounts[user_public_key].set_balance((accounts[user_public_key].get_balance() + XRP_amount).__round__(6))
            print("Your new balance is: " + str(accounts[user_public_key].get_balance()))
            # write to ledger through self.data in transaction.py
            data = "Eva Bank transferred " + str(XRP_amount) + " XRP to " + str(user_public_key) + \
                   "\nRate = " + str(XRP_rate)
            prev_hash = Transaction(data, prev_hash).get_hash()
        elif choice == 3: # send XRP
            receiver = input("Enter receiver public key: ")
            # search user keys to see if it exists and that user did not input own public key
            while receiver not in accounts or receiver == user_public_key:
                receiver = input("Invalid public key. Please try again: ")
            # get send amount and ensure sender has enough to execute transaction
            print("1 XRP = " + str(XRP_rate) + " USD")
            USD_amount = input("How much would you like to send? (USD): ")
            while not USD_amount or not USD_amount.isnumeric() or float(USD_amount) <= 0 or \
                    float(USD_amount)/XRP_rate > accounts[user_public_key].get_balance():
                USD_amount = input("Invalid input, enter a USD amount between 0 and your current balance (" +
                                   str((accounts[user_public_key].get_balance()).__round__(6)) + " XRP): ")
            XRP_amount = (float(USD_amount) / XRP_rate).__round__(6)
            print("You just successfully sent " + str(XRP_amount) + " XRP.")
            # update sender account balance
            accounts[user_public_key].set_balance((accounts[user_public_key].get_balance() - XRP_amount).__round__(6))
            # update receiver account balance
            accounts[receiver].set_balance((accounts[receiver].get_balance() + XRP_amount).__round__(6))
            # write transaction to ledger
            data = str(user_public_key) + " sent " + str(XRP_amount) + " XRP to " + str(receiver) + \
                   "\nRate = " + str(XRP_rate)
            prev_hash = Transaction(data, prev_hash).get_hash()
        elif choice == 4: # receive XRP
            print("To receive XRP, give the sender your public key:" + str(user_public_key))
        elif choice == 5: # view transaction history
            # view transaction ledger
            fileIn = open("XRP-Ledger.txt", "r")
            # loop through hashes and overwrite prev_line (date), ending up with correct date for the transaction
            prev_line = ""
            for line in fileIn:
                if user_public_key in line:  # if user public key in line, print the transaction with prev_line (date)
                    print(prev_line + "\n" + line +
                          "===========================================================================================")
                else:  # if hash not in line, update previous line (date) to current line
                    prev_line = line
            fileIn.close()
    # write changes in balance to XRP-test-accounts.txt
    fileOut = open("XRP-test-accounts.txt", "w")
    print("Public Address,Secret Keys,Balance", file=fileOut)
    for key in accounts:
        print(key + "," + accounts[key].get_private_key() + "," + str(accounts[key].get_balance()), file=fileOut)
    print("Thanks for testing out this crypto simulation! Check out XRP-Ledger.txt to see the transactions"
          "\nwritten to the ledger. You can also see updated account balances in XRP-test-accounts.")
main()