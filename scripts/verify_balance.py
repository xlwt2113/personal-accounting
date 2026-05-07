import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

db_path = r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# 原始数据
print("=" * 60)
print("账户 initial_balance 原始值:")
cursor.execute("SELECT id, name, account_type, initial_balance FROM accounts ORDER BY account_type, name")
for r in cursor.fetchall():
    print(f"  {r['name']} | type={r['account_type']} | initial={r['initial_balance']}")

print("\n" + "=" * 60)
print("各账户全部交易汇总:")
cursor.execute("""
    SELECT 
        t.account_id,
        a.name,
        a.account_type,
        a.initial_balance,
        SUM(CASE WHEN t.transaction_type='income' THEN t.amount ELSE 0 END) as total_income,
        SUM(CASE WHEN t.transaction_type='expense' THEN t.amount ELSE 0 END) as total_expense
    FROM transactions t
    JOIN accounts a ON t.account_id = a.id
    GROUP BY t.account_id
    ORDER BY a.account_type, a.name
""")
for r in cursor.fetchall():
    if r['account_type'] == 'credit_card':
        balance = abs(r['initial_balance'] + r['total_expense'] - r['total_income'])
    else:
        balance = r['initial_balance'] + r['total_income'] - r['total_expense']
    print(f"  {r['name']} | 初始={r['initial_balance']} | 收入={r['total_income']:.2f} | 支出={r['total_expense']:.2f} | 计算余额={balance:.2f}")

conn.close()