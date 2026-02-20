import argparse

from user_store import add_user, list_users

parser = argparse.ArgumentParser(description="Add a user to the user store")
parser.add_argument("username")
parser.add_argument("password")
args = parser.parse_args()

add_user(args.username, args.password)
print("Added user:", args.username)
print("Current users:", list_users())
