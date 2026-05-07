import sqlite3

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check accounts
print("=== Accounts ===")
cursor.execute("SELECT id, name, account_type, initial_balance FROM accounts")
for row in cursor.fetchall():
    print(f"  ID {row[0]}: {row[1]} | Type: {row[2]} | Initial: {row[3]}")

# Check transfer
print("\n=== Latest Transfer ===")
cursor.execute("""
    SELECT t.id, t.amount, t.transfer_time, 
           a1.name as from_account, a2.name as to_account
    FROM transfers t
    JOIN accounts a1 ON t.from_account_id = a1.id
    JOIN accounts a2 ON t.to_account_id = a2.id
    ORDER BY t.id DESC LIMIT 1
""")
row = cursor.fetchone()
if row:
    print(f"  Transfer ID: {row[0]}, Amount: {row[1]}, Time: {row[2]}")
    print(f"  From: {row[3]}")
    print(f"  To: {row[4]}")

# Check transactions
print("\n=== Related Transactions ===")
cursor.execute("""
    SELECT id, amount, transaction_type, account_id, category
    FROM transactions WHERE transfer_id = (SELECT MAX(id) FROM transfers)
""")
for row in cursor.fetchall():
    print(f"  ID {row[0]}: {row[1]} | {row[2]} | Account {row[3]} | {row[4]}")

conn.close()
