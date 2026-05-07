import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

account_name = "中信银行信用卡（7379）"
credit_limit = 75000.00
available = 74312.03
owed = credit_limit - available  # 687.97
created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cursor.execute(
    """INSERT INTO accounts (name, account_type, initial_balance, credit_limit, created_at, updated_at)
       VALUES (?, ?, ?, ?, ?, ?)""",
    (account_name, "credit_card", owed, credit_limit, created_at, created_at)
)
conn.commit()
print(f"Account created: {account_name}, owed: {owed}, credit limit: {credit_limit}")

conn.close()
