import sqlite3

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get 招商银行储蓄卡 balance
cursor.execute("""
    SELECT a.id, a.name, a.initial_balance,
           COALESCE(SUM(CASE WHEN t.transaction_type = 'income' THEN t.amount ELSE 0 END), 0) as income_total,
           COALESCE(SUM(CASE WHEN t.transaction_type = 'expense' THEN t.amount ELSE 0 END), 0) as expense_total
    FROM accounts a
    LEFT JOIN transactions t ON a.id = t.account_id
    WHERE a.name LIKE '%招商银行储蓄卡%'
    GROUP BY a.id
""")
card = cursor.fetchone()

# Get 支付宝/花呗 balance
cursor.execute("""
    SELECT a.id, a.name, a.initial_balance,
           COALESCE(SUM(CASE WHEN t.transaction_type = 'income' THEN t.amount ELSE 0 END), 0) as income_total,
           COALESCE(SUM(CASE WHEN t.transaction_type = 'expense' THEN t.amount ELSE 0 END), 0) as expense_total
    FROM accounts a
    LEFT JOIN transactions t ON a.id = t.account_id
    WHERE a.name = '支付宝'
    GROUP BY a.id
""")
alipay = cursor.fetchone()

print("=== 招商银行储蓄卡 ===")
if card:
    balance = card[2] + card[3] - card[4]
    print(f"  Account ID: {card[0]}")
    print(f"  Initial: {card[2]}")
    print(f"  Income: +{card[3]}")
    print(f"  Expense: -{card[4]}")
    print(f"  Balance: {balance}")
else:
    print("  Not found")

print("\n=== 支付宝(花呗) ===")
if alipay:
    balance = alipay[2] + alipay[3] - alipay[4]
    print(f"  Account ID: {alipay[0]}")
    print(f"  Initial: {alipay[2]}")
    print(f"  Income: +{alipay[3]}")
    print(f"  Expense: -{alipay[4]}")
    print(f"  Balance: {balance}")
else:
    print("  Not found")

conn.close()
