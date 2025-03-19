from datetime import datetime, date

class Sessions:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    def account_creation(self, cursor, mydb):
        creation_date = datetime.today()
        cursor.execute(f"INSERT INTO accounts (balance, user_id, creation_date) VALUES (0, {self.user_id}, '{creation_date}');")
        mydb.commit()

    def get_balance(self, cursor):
        cursor.execute(f"SELECT balance FROM accounts WHERE user_id = {self.user_id};")
        return cursor.fetchall()[0][0]
    
    def sort_by(self, cursor, sorting: str,  ascending: bool):
        if ascending:
            order = "ASC"
        else:
            order = "DESC"
        cursor.execute(f"SELECT * FROM transactions WHERE user_id = {self.user_id} ORDER BY {sorting} {order};")
        return cursor.fetchall()
    
    def sort_dates(self, cursor, start: datetime, end: datetime = ''):
        if end:
            cursor.execute(f"SELECT * FROM transactions WHERE user_id = {self.user_id} AND date BETWEEN {start} AND {end};")
        else:
            cursor.execute(f"SELECT * FROM transactions WHERE user_id = {self.user_id} AND date = {start};")
        
        return cursor.fetchall()