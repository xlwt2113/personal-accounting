import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
    SELECT a.id, a.name, a.account_type, a.initial_balance,
           COALESCE(SUM(CASE WHEN t.transaction_type = 'income' THEN t.amount ELSE 0 END), 0) as income_total,
           COALESCE(SUM(CASE WHEN t.transaction_type = 'expense' THEN t.amount ELSE 0 END), 0) as expense_total
    FROM accounts a
    LEFT JOIN transactions t ON a.id = t.account_id
    GROUP BY a.id
    ORDER BY a.id
""")

print("=== All Accounts ===\n")
for row in cursor.fetchall():
    balance = row[3] + row[4] - row[5]
    print(f"ID: {row[0]}")
    print(f"  Name: {row[1]}")
    print(f"  Type: {row[2]}")
    print(f"  Balance: {balance}")
    print()

conn.close()
