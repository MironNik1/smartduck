import aiosqlite
import asyncio

class UserX:
    def __init__(self, db_file='db_users.sql'):
        self.db_file = db_file

    async def __aenter__(self):
        self.conn = await aiosqlite.connect(self.db_file)
        self.cursor = await self.conn.cursor()
        await self.create_table()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()

    async def create_table(self):
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS telegram_bot_users (
                                        tg_id INT PRIMARY KEY,
                                        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        premium BOOLEAN DEFAULT FALSE,
                                        requests_count INT DEFAULT 0,
                                        balance INT DEFAULT 0,
                                        age INT DEFAULT 0,
                                        gender TEXT DEFAULT None,
                                        name TEXT DEFAULT None,
                                        isRegistered BOOLEAN DEFAULT FALSE
                                    )''')
        await self.conn.commit()

    async def create_user(self, tg_id, premium=False):
        await self.cursor.execute("INSERT INTO telegram_bot_users (tg_id, premium) VALUES (?, ?)", (tg_id, premium))
        await self.conn.commit()

    async def get_user(self, tg_id):
        await self.cursor.execute("SELECT * FROM telegram_bot_users WHERE tg_id = ?", (tg_id,))
        return await self.cursor.fetchone()

    async def delete_user(self, tg_id):
        await self.cursor.execute("DELETE FROM telegram_bot_users WHERE tg_id = ?", (tg_id,))
        await self.conn.commit()

    async def edit_user(self, tg_id, **kwargs):
        for key, value in kwargs.items():
            if key in ['premium', 'balance', 'requests_count', 'age', 'gender', 'name', 'isRegistered']:
                await self.cursor.execute(f"UPDATE telegram_bot_users SET {key} = ? WHERE tg_id = ?", (value, tg_id))
                await self.conn.commit()

    async def increment_requests_count(self, tg_id):
        await self.cursor.execute("UPDATE telegram_bot_users SET requests_count = requests_count + 1 WHERE tg_id = ?", (tg_id,))
        await self.conn.commit()

    async def update_balance(self, tg_id, amount):
        await self.cursor.execute("UPDATE telegram_bot_users SET balance = ? WHERE tg_id = ?", (amount, tg_id))
        await self.conn.commit()