import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

account_name = "招商银行信用卡（7685）"

# 检查账户是否已存在
cursor.execute("SELECT id FROM accounts WHERE name = ?", (account_name,))
if cursor.fetchone():
    print(f"Account already exists: {account_name}")
else:
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        """INSERT INTO accounts (name, account_type, initial_balance, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?)""",
        (account_name, "credit_card", 0.00, created_at, created_at)
    )
    conn.commit()
    print(f"Account created: {account_name}")

conn.close()
