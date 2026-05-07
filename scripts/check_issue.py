import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
conn = sqlite3.connect('C:/Users/wt/.openclaw/workspace/skills/personal-accounting/db/accounting.db')
cur = conn.cursor()

# 检查 account_type='savings' 的账户（这个类型不是标准类型）
cur.execute("SELECT id, name, account_type FROM accounts WHERE account_type = 'savings'")
rows = cur.fetchall()
print("account_type='savings' 的账户:")
for r in rows:
    print(f"  {r}")

# 检查是否有余额宝账户
cur.execute("SELECT id, name, account_type, initial_balance FROM accounts WHERE name LIKE '%余额宝%' OR name LIKE '%支付宝%'")
rows = cur.fetchall()
print("\n支付宝相关账户:")
for r in rows:
    print(f"  {r}")