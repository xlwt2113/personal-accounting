import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 检查账户是否已存在
cursor.execute("SELECT id FROM accounts WHERE name = ?", ("招商银行储蓄卡（5689）",))
if cursor.fetchone():
    print("账户已存在：招商银行储蓄卡（5689）")
else:
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        """INSERT INTO accounts (name, account_type, initial_balance, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?)""",
        ("招商银行储蓄卡（5689）", "savings_card", 1000.00, created_at, created_at)
    )
    conn.commit()
    print("账户创建成功：招商银行储蓄卡（5689），初始余额 ¥1,000.00")

conn.close()
