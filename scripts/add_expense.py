import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

DB_PATH = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

# 支出记录 - 微信零钱转账
amount = 7.00
account_name = "微信零钱"
merchant = "晴空万里"
category = "other"
transaction_date = "2026-05-01"
note = '二维码转账给晴空万里，交易单号：10001073012026050100957833715154'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT id FROM accounts WHERE name = ?", (account_name,))
result = cursor.fetchone()
account_id = result[0] if result else None

if account_id is None:
    cursor.execute("""
        INSERT INTO accounts (name, account_type, initial_balance, credit_limit, created_at, updated_at)
        VALUES (?, 'wechat_wallet', 0, 0, datetime('now'), datetime('now'))
    """, (account_name,))
    account_id = cursor.lastrowid
    print(f"✅ 已创建账户：{account_name}（ID: {account_id}）")
else:
    print(f"📁 账户已存在：{account_name}（ID: {account_id}）")

cursor.execute("""
    INSERT INTO transactions (amount, transaction_type, account_id, merchant, category, transaction_date, note, created_at)
    VALUES (?, 'expense', ?, ?, ?, ?, ?, datetime('now'))
""", (amount, account_id, merchant, category, transaction_date, note))

transaction_id = cursor.lastrowid
conn.commit()
conn.close()

print(f"✅ 已记录支出：-{amount}元")
print(f"   收款方：{merchant}")
print(f"   账户：{account_name}")
print(f"   分类：{category}")
print(f"   日期：{transaction_date}")
print(f"   记录ID：{transaction_id}")
