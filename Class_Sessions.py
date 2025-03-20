from datetime import datetime, date

class Sessions:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        
    def create_session(user_data):
        # Put the id of the user here for the session (should be overwritten when new session is created)
        # This is for select requests
        user = Sessions(user_data[0], user_data[1])
        return user
    
    def get_balance(self, cursor):
        cursor.execute(f"SELECT balance FROM accounts WHERE user_id = {self.user_id};")
        return cursor.fetchall()[0][0]
    
    def sort_by(self, cursor, table, sorting: str, ascending: bool):
        if ascending:
            order = "ASC"
        else:
            order = "DESC"
        cursor.execute(f"SELECT * FROM {table} WHERE user_id = {self.user_id} ORDER BY '{sorting}' {order};")
        return cursor.fetchall()
    
    def sort_dates(self, cursor, start: datetime, end: datetime = ''):
        if end:
            cursor.execute(f"SELECT * FROM transactions WHERE user_id = {self.user_id} AND date BETWEEN {start} AND {end};")
        else:
            cursor.execute(f"SELECT * FROM transactions WHERE user_id = {self.user_id} AND date = {start};")
        
        return cursor.fetchall()