import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"
conn = sqlite3.connect(db_path, isolation_level=None)
cursor = conn.cursor()

# 创建支付宝账户（如果不存在）
cursor.execute("SELECT id FROM accounts WHERE name = '支付宝'")
existing = cursor.fetchone()

if not existing:
    cursor.execute("""
        INSERT INTO accounts (name, account_type, initial_balance, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    """, ("支付宝", "alipay", 0.00, datetime.now().isoformat(), datetime.now().isoformat()))
    alipay_id = cursor.lastrowid
    print(f"支付宝账户创建成功, ID: {alipay_id}")
else:
    alipay_id = existing[0]
    print(f"支付宝账户已存在, ID: {alipay_id}")

# 获取招行储蓄卡账户
cursor.execute("SELECT id FROM accounts WHERE name LIKE '%招商银行储蓄卡%' LIMIT 1")
row = cursor.fetchone()
if not row:
    print("Error: 招商银行储蓄卡 not found")
    exit(1)

from_account_id = row[0]
print(f"招行储蓄卡 ID: {from_account_id}")

# 开始转账事务
transfer_time = datetime.now()
transfer_time_str = transfer_time.isoformat()

cursor.execute("BEGIN")

# 创建转账记录
cursor.execute("""
    INSERT INTO transfers (from_account_id, to_account_id, amount, transfer_time, created_at)
    VALUES (?, ?, ?, ?, ?)
""", (from_account_id, alipay_id, 200.00, transfer_time_str, transfer_time_str))
transfer_id = cursor.lastrowid

# 支出记录（从储蓄卡转出）
cursor.execute("""
    INSERT INTO transactions (amount, transaction_type, account_id, merchant, category, transaction_date, transfer_id, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (200.00, "expense", from_account_id, "转账", "transfer", transfer_time.strftime("%Y-%m-%d"), transfer_id, transfer_time_str))

# 收入记录（转入支付宝/花呗）
cursor.execute("""
    INSERT INTO transactions (amount, transaction_type, account_id, merchant, category, transaction_date, transfer_id, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (200.00, "income", alipay_id, "花呗收款", "transfer", transfer_time.strftime("%Y-%m-%d"), transfer_id, transfer_time_str))

cursor.execute("COMMIT")

print(f"\nTransfer completed!")
print(f"From: 招商银行储蓄卡 -> To: 支付宝(花呗), Amount: 200")

conn.close()
