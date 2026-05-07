import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"
conn = sqlite3.connect(db_path, isolation_level=None)
cursor = conn.cursor()

# 查询招行储蓄卡和支付宝账户ID
cursor.execute("SELECT id, name, account_type FROM accounts WHERE name LIKE '%招商银行储蓄卡%' OR name LIKE '%支付宝%'")
accounts = cursor.fetchall()
print("Found accounts:")
for a in accounts:
    print(f"  ID: {a[0]}, Name: {a[1]}, Type: {a[2]}")

# 找到对应账户
from_account_id = None
to_account_id = None
for a in accounts:
    if "招商银行储蓄卡" in a[1]:
        from_account_id = a[0]
    if "支付宝" in a[1]:
        to_account_id = a[0]

if not from_account_id:
    print("Error: 招商银行储蓄卡 account not found")
    exit(1)
if not to_account_id:
    print("Error: 支付宝 account not found")
    exit(1)

print(f"\nTransfer: {from_account_id} -> {to_account_id}, Amount: 200")

# 开始事务
cursor.execute("BEGIN")

# 创建转账记录
transfer_time = datetime.now().isoformat()
cursor.execute("""
    INSERT INTO transfers (from_account_id, to_account_id, amount, transfer_time, created_at)
    VALUES (?, ?, ?, ?, ?)
""", (from_account_id, to_account_id, 200.00, transfer_time, transfer_time))
transfer_id = cursor.lastrowid
print(f"Transfer record created, ID: {transfer_id}")

# 创建支出记录（从储蓄卡转出）
cursor.execute("""
    INSERT INTO transactions (amount, transaction_type, account_id, merchant, category, transaction_date, transfer_id, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (200.00, "expense", from_account_id, "转账", "transfer", datetime.now().strftime("%Y-%m-%d"), transfer_id, transfer_time))

# 创建收入记录（转入支付宝）
cursor.execute("""
    INSERT INTO transactions (amount, transaction_type, account_id, merchant, category, transaction_date, transfer_id, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (200.00, "income", to_account_id, "转账", "transfer", datetime.now().strftime("%Y-%m-%d"), transfer_id, transfer_time))

cursor.execute("COMMIT")

print("\nTransfer completed successfully!")
print(f"From: 招商银行储蓄卡 -> To: 支付宝, Amount: 200")

conn.close()
