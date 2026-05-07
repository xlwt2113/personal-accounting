import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

account_name = "交通银行信用卡（8114）"

# Check if exists
cursor.execute("SELECT id FROM accounts WHERE name = ?", (account_name,))
if cursor.fetchone():
    print(f"Account already exists: {account_name}")
else:
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        """INSERT INTO accounts (name, account_type, initial_balance, credit_limit, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (account_name, "credit_card", 0.00, 70000.00, created_at, created_at)
    )
    conn.commit()
    print(f"Account created: {account_name}, credit limit: 70000.00")

conn.close()
