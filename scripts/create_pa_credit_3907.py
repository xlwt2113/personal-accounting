import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

account_name = "平安银行信用卡（3907）"
credit_limit = 38000.00
available = 37206.53
owed = credit_limit - available  # 793.47
created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cursor.execute(
    """INSERT INTO accounts (name, account_type, initial_balance, credit_limit, created_at, updated_at)
       VALUES (?, ?, ?, ?, ?, ?)""",
    (account_name, "credit_card", owed, credit_limit, created_at, created_at)
)
conn.commit()
print(f"Account created: {account_name}, owed: {owed}, credit limit: {credit_limit}")

conn.close()
