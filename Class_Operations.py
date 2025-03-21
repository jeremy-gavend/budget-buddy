from datetime import datetime
from Class_Sessions import Sessions

class Operations:       
    def manage_account(app, action):
        creation_date = datetime.today()
        if action == "create":
            app.cursor.execute(f"INSERT INTO accounts (balance, user_id, creation_date) VALUES (0, {app.user.user_id}, '{creation_date}');")
        if action == "delete":
            app.cursor.execute(f"DELETE FROM accounts WHERE user_id = {app.user.user_id};")
        app.mydb.commit()
 # TODO add a condition to delete transactions if both id_user (from and to) doesn't exist

    def operation(app, operation): #amount: float, description: str, category: str
        # TODO add from_user, from_account, to_user, to_account
        # TEST
        amount = 10
        description = 'test'
        category = 'test'
        #-----
        try:
            balance = app.user.get_balance(app.cursor)
            current_date = datetime.today()
            if operation == "withdraw":
                #TODO add verif to check if balance is enough
                app.cursor.execute(f"UPDATE accounts SET balance = {balance - amount} WHERE user_id = {app.user.user_id};")
                app.info_message.text = [f"{app.user.username}, you successfully withdrew {amount} from your account at {current_date}."]
            elif operation == "deposit":
                app.cursor.execute(f"UPDATE accounts SET balance = {balance + amount} WHERE user_id = {app.user.user_id};")
                app.info_message.text = [f"{app.user.username}, you successfully deposited {amount} into your account at {current_date}."]
            elif operation == "transfert":
                pass
                # TODO account selected or from, destination account
                # TODO update both accounts using previous functions
                # app.cursor.execute(f"UPDATE accounts SET balance = {balance - amount} WHERE user_id = {app.user.user_id};")
                # string = f"{app.user.username}, you successfully withdrew {amount} from your account at {current_date}."
        except Exception:
            app.info_message.text = ["You need an account first!"]
            return 
        app.mydb.commit()
        
        app.cursor.execute(f"INSERT INTO transactions (user_id, amount, description, date, type, category) VALUES ({app.user.user_id}, {amount}, '{description}', '{current_date}', '{operation}', '{category}');")
        app.mydb.commit()