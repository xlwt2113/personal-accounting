import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

account_id = 5
amount = 41.89
merchant = "京小盒生活超市"
category = "shopping"
transaction_date = "2026-04-25"
created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cursor.execute(
    """INSERT INTO transactions (amount, transaction_type, account_id, merchant, category, transaction_date, created_at)
       VALUES (?, ?, ?, ?, ?, ?, ?)""",
    (amount, "expense", account_id, merchant, category, transaction_date, created_at)
)
conn.commit()
print(f"Expense recorded: -{amount} at {merchant} on {transaction_date}")

conn.close()
