import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

account_name = "支付宝"

# 检查账户是否已存在
cursor.execute("SELECT id FROM accounts WHERE name = ?", (account_name,))
row = cursor.fetchone()
if row:
    account_id = row[0]
    print(f"Account found: {account_name} (ID: {account_id})")
else:
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        """INSERT INTO accounts (name, account_type, initial_balance, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?)""",
        (account_name, "alipay", 0.00, created_at, created_at)
    )
    conn.commit()
    account_id = cursor.lastrowid
    print(f"Account created: {account_name} (ID: {account_id})")

conn.close()
