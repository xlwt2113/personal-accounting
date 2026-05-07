import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
from datetime import datetime

db_path = r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db'

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# 获取所有账户
cursor.execute("SELECT * FROM accounts ORDER BY account_type, name")
accounts = cursor.fetchall()

print(f"共 {len(accounts)} 个账户")

# 计算每个账户的余额
def calc_balance(account_id, initial_balance, account_type):
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN transaction_type='income' THEN amount ELSE 0 END) as income,
            SUM(CASE WHEN transaction_type='expense' THEN amount ELSE 0 END) as expense
        FROM transactions WHERE account_id = ?
    """, (account_id,))
    row = cursor.fetchone()
    income = row['income'] or 0
    expense = row['expense'] or 0
    print(f"    calc: id={account_id}, initial={initial_balance}, income={income}, expense={expense}")
    if account_type == 'credit_card':
        balance = abs(initial_balance + expense - income)
    else:
        balance = initial_balance + income - expense
    return balance, income, expense

# 分离资产账户和信用卡
asset_accounts = []
credit_accounts = []
total_assets = 0
total_debt = 0

for acc in accounts:
    balance, income, expense = calc_balance(acc['id'], acc['initial_balance'], acc['account_type'])
    print(f"  {acc['name']} | type={acc['account_type']} | balance={balance}")

conn.close()