from datetime import datetime

class Operations:
    def withdraw(self, cursor, user, amount, description):
        """Called by the button "withdraw" """
        balance = user.get_balance(cursor)
        date = datetime.date()
 
        cursor.execute(f"UPDATE accounts SET balance = {balance - amount} WHERE user_id = {user.user.id}")
        cursor.execute(f"INSERT INTO transactions (user_id, amount, description, date, type) VALUES ({user.username}, {amount}, {description}, {date}, 'withdraw')")

        # ! Display this in a informative textbox
        return f"{user.username}, you successfully withdrew {amount} from your account at {date}."

    def deposit(self, cursor, user, amount, description):
        """ Called by the button "deposit" """
        
        balance = user.get_balance(cursor)
        date = datetime.date()

        cursor.execute(f"UPDATE accounts SET balance = {balance + amount} WHERE user_id = {user.user_id}")
        cursor.execute(f"INSERT INTO transactions (user_id, amount, description, date, type) VALUES ({user.username}, {amount}, {description}, {date}, 'withdraw')")

        # ! Display this in a informative textbox
        return f"{user.username}, you successfully withdrew {amount} from your account at {date}."

    def transfert(self):
        # something for the display here
        return 

    def history(self, cursor, user):
        cursor.execute(f"SELECT * FROM transactions WHERE user_id = {user.user_id}")
        return cursor.fetchall()