import mysql.connector, pygame
from Class_Account import Accounts

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

try:
    cursor.execute("SELECT * FROM users WHERE username = 'username' AND password = 'password'")
except Exception:
    print("Error in login")

user_data = cursor.fetchall()

# Put the id of the user here for the session (should be overwritten when new session is created)
# This is for select requests
user = Accounts(user_data[0], user_data[1])