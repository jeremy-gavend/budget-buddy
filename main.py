import mysql.connector, pygame
from Class_Accounts import Accounts
from Class_Operations import Operations
from hashlib import sha256

#----- Local connection stuffs
mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "root",
  database = "budget_buddy"
)

cursor = mydb.cursor()
#-----

# TODO Some login page
# TODO some resister page that create an user
username_input = 'test'
password_input = 'test'

# --- Test ---
username = username_input
password = sha256(password_input.encode()).hexdigest()
# --- ---- ---

try:
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}';")
except Exception:
    print("Error in login")

user_data = cursor.fetchall()

# Put the id of the user here for the session (should be overwritten when new session is created)
# This is for select requests
user = Accounts(user_data[0][0], user_data[0][1])

try:
  user.account_creation(cursor, mydb)
except Exception:
  print("Error in account creation")

# print in textbox
# balance = user.get_balance(cursor)

#button deposit that display deposit interface
# message_dep = Operations.deposit(cursor, mydb, user, 100, "Test_deposit", "None")
# print(message_dep)

#button withdraw that display withdraw interface
# message_withd = Operations.withdraw(cursor, mydb, user, 50, "Test_withdraw", "None")
# print(message_withd)


#button history that display history interface
# historic = Operations.history(cursor, user)
# print(historic)

# lots of button that call this but with different labels
# sorted = user.sort_by(cursor, "date", True)
# print(sorted)

# for specific dates button
sorted_dates = user.sort_dates(cursor, "2021-01-01", "2021-12-31")
print(sorted_dates)

sorted_dates = user.sort_dates(cursor, "2021-01-01")
print(sorted_dates)