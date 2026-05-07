import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

account_id = 1
amount = 183.00
merchant = "东北人家"
category = "food"
transaction_date = datetime.now().strftime("%Y-%m-%d")
created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cursor.execute(
    """INSERT INTO transactions (amount, transaction_type, account_id, merchant, category, transaction_date, created_at)
       VALUES (?, ?, ?, ?, ?, ?, ?)""",
    (amount, "expense", account_id, merchant, category, transaction_date, created_at)
)
conn.commit()
print(f"Record added: 183.00 spent at {merchant} on {transaction_date}")

conn.close()
