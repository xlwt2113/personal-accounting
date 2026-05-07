import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

account_id = 6
amount = 3.29
merchant = "兴全基金管理有限公司"
category = "investment"
transaction_date = "2026-04-28"
created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cursor.execute(
    """INSERT INTO transactions (amount, transaction_type, account_id, merchant, category, transaction_date, created_at)
       VALUES (?, ?, ?, ?, ?, ?, ?)""",
    (amount, "income", account_id, merchant, category, transaction_date, created_at)
)
conn.commit()
print(f"Income recorded: +{amount} from {merchant} on {transaction_date}")

conn.close()
