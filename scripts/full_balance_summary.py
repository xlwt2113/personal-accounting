import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Overall totals
cursor.execute("""
    SELECT 
        SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as total_income,
        SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as total_expense
    FROM transactions
""")
row = cursor.fetchone()
total_income = row[0] or 0
total_expense = row[1] or 0
net = total_income - total_expense

print(f"Total Income:  {total_income:.2f}")
print(f"Total Expense: {total_expense:.2f}")
print(f"Net:           {net:.2f}")
print()

# Account balances
cursor.execute("""
    SELECT id, name, account_type, initial_balance, credit_limit
    FROM accounts
""")
accounts = cursor.fetchall()

total_asset = 0
total_liability = 0

print(f"{'Account':<25} {'Type':<15} {'Balance/Liability'}")
print("-" * 60)
for acc in accounts:
    acc_id, name, acc_type, init_bal, credit_limit = acc
    if acc_type == 'credit_card':
        owed = init_bal
        print(f"{name:<25} {acc_type:<15} Owed: {owed:.2f}")
        total_liability += owed
    else:
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as income,
                SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as expense
            FROM transactions WHERE account_id = ?
        """, (acc_id,))
        tx = cursor.fetchone()
        income = tx[0] or 0
        expense = tx[1] or 0
        balance = init_bal + income - expense
        print(f"{name:<25} {acc_type:<15} {balance:.2f}")
        total_asset += balance

print("-" * 60)
print(f"Total Assets:      {total_asset:.2f}")
print(f"Total Liabilities: {total_liability:.2f}")
print(f"Net Worth:         {total_asset - total_liability:.2f}")

conn.close()
