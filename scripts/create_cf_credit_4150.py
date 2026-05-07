import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

account_name = "广发银行信用卡（4150）"
credit_limit = 115000.00
available = 111205.47
owed = credit_limit - available  # 3794.53
created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cursor.execute(
    """INSERT INTO accounts (name, account_type, initial_balance, credit_limit, created_at, updated_at)
       VALUES (?, ?, ?, ?, ?, ?)""",
    (account_name, "credit_card", owed, credit_limit, created_at, created_at)
)
conn.commit()
print(f"Account created: {account_name}, owed: {owed}, credit limit: {credit_limit}")

conn.close()
