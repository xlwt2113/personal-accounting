import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

from_account_id = 1
to_account_id = 2
amount = 3100.00
transfer_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
created_at = transfer_time
note = "还款"

# 创建转账记录
cursor.execute(
    """INSERT INTO transfers (from_account_id, to_account_id, amount, transfer_time, note, created_at)
       VALUES (?, ?, ?, ?, ?, ?)""",
    (from_account_id, to_account_id, amount, transfer_time, note, created_at)
)
transfer_id = cursor.lastrowid

# 支出记录 (from savings card)
cursor.execute(
    """INSERT INTO transactions (amount, transaction_type, account_id, merchant, category, transaction_date, transfer_id, created_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
    (amount, "expense", from_account_id, "招商银行信用卡", "bills", transfer_time[:10], transfer_id, created_at)
)

# 收入记录 (to credit card - means repayment reduces balance/owed)
cursor.execute(
    """INSERT INTO transactions (amount, transaction_type, account_id, merchant, category, transaction_date, transfer_id, created_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
    (amount, "income", to_account_id, "招商银行储蓄卡", "refund", transfer_time[:10], transfer_id, created_at)
)

conn.commit()
print(f"Transfer completed: 3100.00 from savings(5678) to credit(7685)")

conn.close()
