import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

account_name = "微信零钱"
created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cursor.execute(
    """INSERT INTO accounts (name, account_type, initial_balance, created_at, updated_at)
       VALUES (?, ?, ?, ?, ?)""",
    (account_name, "wechat_wallet", 1430.67, created_at, created_at)
)
conn.commit()
print(f"Account created: {account_name}, initial balance: 1430.67")

conn.close()
