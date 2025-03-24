from datetime import datetime, date

class Sessions:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.selected_account_id = 1
        
    def create_session(user_data):
        # Put the id of the user here for the session (should be overwritten when new session is created)
        # This is for select requests
        user = Sessions(user_data[0], user_data[1])
        return user
    
    def get_balance(self, cursor):
        cursor.execute(f"SELECT balance FROM accounts WHERE user_id = {self.user_id} AND id = {self.selected_account_id};")
        data = cursor.fetchall()
        if data:
            return data[0][0]
        else:
            return ''
        
    def sort_by(self, app, table, sorting: str, ascending: bool):
        if ascending:
            order = "ASC"
        else:
            order = "DESC"
        app.cursor.execute(f"SELECT * FROM {table} WHERE user_id = {self.user_id} ORDER BY '{sorting}' {order};")
        return app.cursor.fetchall()
    
    def sort_dates(self, app, sorting, text):
        if sorting == "date2":
            app.cursor.execute(f"SELECT * FROM transactions WHERE user_id = {self.user_id} AND date BETWEEN {self.main_filter_transactions_textboxes["date"].text} AND {text};")
        else:
            app.cursor.execute(f"SELECT * FROM transactions WHERE user_id = {self.user_id} AND {sorting} = {text};")
        
        return app.cursor.fetchall()