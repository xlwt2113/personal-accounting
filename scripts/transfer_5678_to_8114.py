import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

from_account_id = 4  # 招行储蓄卡5678
to_account_id = 5    # 交通银行信用卡8114
amount = 1000.00
transfer_time = "2026-04-29 10:14:23"
created_at = transfer_time

# Create transfer record
cursor.execute(
    """INSERT INTO transfers (from_account_id, to_account_id, amount, transfer_time, note, created_at)
       VALUES (?, ?, ?, ?, ?, ?)""",
    (from_account_id, to_account_id, amount, transfer_time, "还款", created_at)
)
transfer_id = cursor.lastrowid

# Expense from savings card
cursor.execute(
    """INSERT INTO transactions (amount, transaction_type, account_id, merchant, category, transaction_date, transfer_id, created_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
    (amount, "expense", from_account_id, "交通银行信用卡", "bills", transfer_time[:10], transfer_id, created_at)
)

# Income to credit card (repayment reduces balance owed)
cursor.execute(
    """INSERT INTO transactions (amount, transaction_type, account_id, merchant, category, transaction_date, transfer_id, created_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
    (amount, "income", to_account_id, "招商银行储蓄卡", "refund", transfer_time[:10], transfer_id, created_at)
)

conn.commit()
print(f"Transfer completed: 1000 from savings(5678) to credit(8114) at {transfer_time}")

conn.close()
