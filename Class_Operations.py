from datetime import datetime
from Class_Sessions import Sessions

class Operations:
    def account_creation(self, cursor, mydb):
        #TODO create a button for it (in 'action?')
        creation_date = datetime.today()
        cursor.execute(f"INSERT INTO accounts (balance, user_id, creation_date) VALUES (0, {self.user_id}, '{creation_date}');")
        mydb.commit()

    def account_deletion(self, cursor, mydb):
        pass
        # TODO
        # cursor.execute(f";")
        # mydb.commit()

    def operation(app, operation): #amount: float, description: str, category: str
        # TEST
        amount = 10
        description = 'test'
        category = 'test'
        #-----
        try:
            balance = app.user.get_balance(app.cursor)
        except Exception:
            return "You need an account first!" 
        current_date = datetime.today()
        if operation == "withdraw":
            app.cursor.execute(f"UPDATE accounts SET balance = {balance - amount} WHERE user_id = {app.user.user_id};")
            string = f"{app.user.username}, you successfully withdrew {amount} from your account at {current_date}."
        elif operation == "deposit":
            app.cursor.execute(f"UPDATE accounts SET balance = {balance + amount} WHERE user_id = {app.user.user_id};")
            string = f"{app.user.username}, you successfully deposited {amount} into your account at {current_date}."
        elif operation == "transfert":
            pass
            # TODO account selected or from, destination account
            # TODO update both accounts using previous functions
            # app.cursor.execute(f"UPDATE accounts SET balance = {balance - amount} WHERE user_id = {app.user.user_id};")
            # string = f"{app.user.username}, you successfully withdrew {amount} from your account at {current_date}."
        
        app.cursor.execute(f"INSERT INTO transactions (user_id, amount, description, date, type, category) VALUES ({app.user.user_id}, {amount}, '{description}', '{current_date}', {operation}, '{category}');")

        app.mydb.commit()
        return string

    def withdraw(cursor, mydb, user: Sessions, amount: float, description, category):
        """Called by the button "withdraw" """
        pass
        #TODO add verif to check if balance is enough
        
    def deposit(cursor, mydb, user: Sessions, amount: float, description: str, category: str):
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