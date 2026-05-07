import sqlite3
from datetime import datetime

conn = sqlite3.connect(r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db')
cursor = conn.cursor()

# Check if 支付宝 account exists
cursor.execute("SELECT id FROM accounts WHERE name = '支付宝'")
alipay_result = cursor.fetchone()

if not alipay_result:
    cursor.execute("""
        INSERT INTO accounts (name, account_type, initial_balance, created_at, updated_at)
        VALUES ('支付宝', 'alipay', 0, datetime('now'), datetime('now'))
    """)
    alipay_id = cursor.lastrowid
else:
    alipay_id = alipay_result[0]

# Get 招商银行储蓄卡 ID
cursor.execute("SELECT id FROM accounts WHERE account_type = 'savings_card' LIMIT 1")
cmb_id = cursor.fetchone()[0]

# Record the transfer
amount = 641.02
transfer_time = '2026-04-28 23:01:19'

cursor.execute("""
    INSERT INTO transfers (from_account_id, to_account_id, amount, transfer_time, note, created_at)
    VALUES (?, ?, ?, ?, ?, datetime('now'))
""", (cmb_id, alipay_id, amount, transfer_time, '花呗还款-2026年05月账单'))

transfer_id = cursor.lastrowid

conn.commit()
conn.close()

print(f"SUCCESS: Transfer {transfer_id} recorded")
print(f"From: 招商银行储蓄卡 -> To: 支付宝/花呗")
print(f"Amount: {amount}")
print(f"Time: {transfer_time}")