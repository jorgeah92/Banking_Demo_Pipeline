# test for making a banking balance sheet

import csv
import os

def new_user(username):
    user = str(username)
    balance = 1000
    userfile = user + ".csv"
    check = os.path.exists(userfile)
    if check is True:
        return "Account already exists"
    else:
        with open(userfile, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([balance])

        return "Account created: " + user

def balance_check(user):
    userfile = str(user) + ".csv"
    check = os.path.exists(userfile)
    if check is False:
        return "The account " + str(username) + " doesn't exist."
    else:
        with open(userfile) as file:
            reader = csv.reader(file, delimiter=',')
            balance = []
            for row in reader:
                balance.append(row)

            return "Current balance: $" + str(balance[-1][0])

def delete_account(username):
    userfile = str(username) + ".csv"
    check = os.path.exists(userfile)
    if check is True:
        print("Are you sure you want to remove " + username + "?")
        answer = input("Enter Y or N: ")
        if answer.upper() == "Y":
            os.remove(userfile)
            print()
            print(username, "deleted")
        else:
            print()
            print("Delete canceled")
    else:
        print()
        print("The account " + str(username) + " doesn't exist.")

    return None

if __name__ == "__main__":
    print("Welcome to banking app!")
    exit = False
    while exit == False:
        print()
        print("Please choose an option:")
        print("1 - Create Account")
        print("2 - Check balance")
        print("3 - Delete Account")
        print("0 - Exit")
        x = input()

        if x == "0":
            exit = True
        elif x == "1":
            username = input("Please enter username: ")
            message = new_user(username)
            print()
            print(message)
        elif x == "2":
            username = input("Please enter username: ")
            message = balance_check(username)
            print()
            print(message)
        elif x == "3":
            username = input("Please enter username: ")
            delete_account(username)
        else:
            print()
            print("Invalid option, try again.")
