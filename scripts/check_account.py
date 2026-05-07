import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if CMB savings card exists
cursor.execute("SELECT id, name, account_type, initial_balance FROM accounts WHERE name LIKE '%招商银行储蓄卡%'")
rows = cursor.fetchall()
print("=== 招商银行储蓄卡账户 ===")
for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Type: {row[2]}, Initial: {row[3]}")

# Also check all accounts
cursor.execute("SELECT id, name, account_type, initial_balance FROM accounts")
all_rows = cursor.fetchall()
print("\n=== 所有账户 ===")
for row in all_rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Type: {row[2]}, Initial: {row[3]}")

conn.close()
