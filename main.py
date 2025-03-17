import mysql.connector, pygame
from Class_Accounts import Accounts
from Class_Operations import Operations

#----- Local connection stuffs
mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "root",
  database = "budget_buddy"
)

cursor = mydb.cursor()
#-----

# Some login page
# some resister page that create an user

# --- Test ---
username = 'test'
password = 'test' #will be a hash
# --- ---- ---

try:
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}';")
except Exception:
    print("Error in login")

user_data = cursor.fetchall()

# Put the id of the user here for the session (should be overwritten when new session is created)
# This is for select requests
user = Accounts(user_data[0][0], user_data[0][1])

# user.account_creation(cursor, mydb)
# balance = user.get_balance(cursor)

# Operations.deposit(cursor, mydb, user, 100, "Test_deposit", "None")
historic = Operations.history(cursor, user)
print(historic)