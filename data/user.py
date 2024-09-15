import sqlite3



class UserX:
    def __init__(self, db_file='db_users.sql'):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS telegram_bot_users (
                                tg_id INT PRIMARY KEY,
                                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                premium BOOLEAN DEFAULT FALSE,
                                requests_count INT DEFAULT 0,
                                balance INT DEFAULT 0
                            )''')
        self.conn.commit()

    def create_user(self, tg_id, premium=False):
        self.cursor.execute("INSERT INTO telegram_bot_users (tg_id, premium) VALUES (?, ?)", (tg_id, premium))
        self.conn.commit()

    def get_user(self, tg_id):
        self.cursor.execute("SELECT * FROM telegram_bot_users WHERE tg_id = ?", (tg_id,))
        return self.cursor.fetchone()

    def delete_user(self, tg_id):
        self.cursor.execute("DELETE FROM telegram_bot_users WHERE tg_id = ?", (tg_id,))
        self.conn.commit()

    def edit_user(self, tg_id, **kwargs):
        for key, value in kwargs.items():
            if key in ['premium', 'balance', 'requests_count']:
                self.cursor.execute(f"UPDATE telegram_bot_users SET {key} = ? WHERE tg_id = ?", (value, tg_id))
                self.conn.commit()

    def increment_requests_count(self, tg_id):
        self.cursor.execute("UPDATE telegram_bot_users SET requests_count = requests_count + 1 WHERE tg_id = ?", (tg_id,))
        self.conn.commit()

    def update_balance(self, tg_id, amount):
        self.cursor.execute("UPDATE telegram_bot_users SET balance = ? WHERE tg_id = ?", (amount, tg_id))
        self.conn.commit()

    def close(self):
        self.conn.close()
