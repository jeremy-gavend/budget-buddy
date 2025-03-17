from datetime import datetime
from Class_Accounts import Accounts

class Operations:
    def withdraw(cursor, mydb, user: Accounts, amount: float, description, category):
        """Called by the button "withdraw" """
        balance = user.get_balance(cursor)
        current_date = datetime.today()
 
        cursor.execute(f"UPDATE accounts SET balance = {balance - amount} WHERE user_id = {user.user_id};")
        cursor.execute(f"INSERT INTO transactions (user_id, amount, description, date, type, category) VALUES ({user.user_id}, {amount}, '{description}', '{current_date}', 'withdraw', '{category}');")

        mydb.commit()
        # ! Display this in a informative textbox
        return f"{user.username}, you successfully withdrew {amount} from your account at {current_date}."

    def deposit(cursor, mydb, user: Accounts, amount: float, description: str, category: str):
        """ Called by the button "deposit" """
        
        balance = user.get_balance(cursor)
        current_date = datetime.today()

        cursor.execute(f"UPDATE accounts SET balance = {balance + amount} WHERE user_id = {user.user_id};")
        cursor.execute(f"INSERT INTO transactions (user_id, amount, description, date, type, category) VALUES ({user.user_id}, {amount}, '{description}', '{current_date}', 'deposit', '{category}');")

        mydb.commit()
        # ! Display this in a informative textbox
        return f"{user.username}, you successfully withdrew {amount} from your account at {current_date}."

    def transfert():
        # something for the display here
        return 

    def history(cursor, user):
        cursor.execute(f"SELECT * FROM transactions WHERE user_id = {user.user_id};")
        return cursor.fetchall()