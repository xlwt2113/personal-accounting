import sqlite3

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT id, name, account_type, initial_balance, credit_limit FROM accounts WHERE id = 5")
row = cursor.fetchone()
print(f"Credit card: {row}")

cursor.execute("""
    SELECT SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as paid,
           SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as spent
    FROM transactions WHERE account_id = 5
""")
row = cursor.fetchone()
print(f"Transactions - paid: {row[0]}, spent: {row[1]}")

conn.close()
