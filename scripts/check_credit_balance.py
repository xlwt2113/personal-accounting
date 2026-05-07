import sqlite3

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check all transactions for credit card (ID 2)
cursor.execute("""
    SELECT id, amount, transaction_type, merchant, category, transaction_date 
    FROM transactions WHERE account_id = 2
""")
rows = cursor.fetchall()
print("Credit card transactions:")
for row in rows:
    print(row)

# Check total spent and paid
cursor.execute("""
    SELECT 
        SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as total_spent,
        SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as total_paid
    FROM transactions WHERE account_id = 2
""")
row = cursor.fetchone()
print(f"\nTotal spent: {row[0]}, Total paid: {row[1]}")

conn.close()
