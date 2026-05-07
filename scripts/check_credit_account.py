import sqlite3

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check credit card account
cursor.execute("SELECT id, name, account_type, initial_balance, credit_limit FROM accounts WHERE name LIKE '%招商银行信用卡%'")
row = cursor.fetchone()
if row:
    print(f"Account: {row}")
else:
    print("Credit card account not found")

conn.close()
