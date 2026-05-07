import sqlite3

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Delete all transaction records first (foreign key dependency)
cursor.execute("DELETE FROM transactions")
# Delete all transfer records
cursor.execute("DELETE FROM transfers")
# Delete all accounts
cursor.execute("DELETE FROM accounts")

conn.commit()

# Verify tables are empty
cursor.execute("SELECT COUNT(*) FROM transactions")
tx_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM transfers")
tf_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM accounts")
acc_count = cursor.fetchone()[0]

print(f"Cleared: {tx_count} transactions, {tf_count} transfers, {acc_count} accounts remaining")

conn.close()
