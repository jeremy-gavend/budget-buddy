class Accounts:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    def get_balance(self, cursor):
        cursor.execute(f"SELECT balance FROM accounts WHERE user_id = {self.id_user}")
        return cursor.fetchall()[0]