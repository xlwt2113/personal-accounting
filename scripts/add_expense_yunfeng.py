import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

DB_PATH = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

amount = 9.30
account_name = "中信银行信用卡（7379）"
account_type = "credit_card"
merchant = "云峰糕点(东明路店)"
category = "food"
transaction_date = "2026-05-01"
note = "交易单号：4200003097202605019608353410"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT id FROM accounts WHERE name = ?", (account_name,))
result = cursor.fetchone()

if result is None:
    cursor.execute("""
        INSERT INTO accounts (name, account_type, initial_balance, credit_limit, created_at, updated_at)
        VALUES (?, ?, 0, 0, datetime('now'), datetime('now'))
    """, (account_name, account_type))
    account_id = cursor.lastrowid
    print(f"✅ 已创建账户：{account_name}（ID: {account_id}）")
else:
    account_id = result[0]
    print(f"📁 账户已存在：{account_name}（ID: {account_id}）")

cursor.execute("""
    INSERT INTO transactions (amount, transaction_type, account_id, merchant, category, transaction_date, note, created_at)
    VALUES (?, 'expense', ?, ?, ?, ?, ?, datetime('now'))
""", (amount, account_id, merchant, category, transaction_date, note))

transaction_id = cursor.lastrowid
conn.commit()
conn.close()

print(f"✅ 已记录支出：{amount}元")
print(f"   商户：{merchant}")
print(f"   账户：{account_name}")
print(f"   分类：{category}")
print(f"   日期：{transaction_date}")
print(f"   记录ID：{transaction_id}")