import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create accounts table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        account_type TEXT NOT NULL,
        initial_balance REAL DEFAULT 0,
        credit_limit REAL DEFAULT 0,
        created_at TEXT,
        updated_at TEXT
    )
""")

# Create transactions table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        transaction_type TEXT NOT NULL,
        account_id INTEGER NOT NULL,
        merchant TEXT,
        category TEXT NOT NULL,
        transaction_date TEXT NOT NULL,
        note TEXT,
        transfer_id INTEGER,
        created_at TEXT,
        FOREIGN KEY (account_id) REFERENCES accounts(id)
    )
""")

# Create transfers table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS transfers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_account_id INTEGER NOT NULL,
        to_account_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        transfer_time TEXT NOT NULL,
        note TEXT,
        created_at TEXT,
        FOREIGN KEY (from_account_id) REFERENCES accounts(id),
        FOREIGN KEY (to_account_id) REFERENCES accounts(id)
    )
""")

conn.commit()

# Create account: 招商银行储蓄卡（5689）
cursor.execute("""
    INSERT INTO accounts (name, account_type, initial_balance, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?)
""", ("招商银行储蓄卡（5689）", "savings_card", 1000.00, datetime.now().isoformat(), datetime.now().isoformat()))

conn.commit()

# Verify
cursor.execute("SELECT id, name, account_type, initial_balance FROM accounts WHERE name = '招商银行储蓄卡（5689）'")
row = cursor.fetchone()
if row:
    print(f"Account created successfully!")
    print(f"ID: {row[0]}")
    print(f"Name: {row[1]}")
    print(f"Type: {row[2]}")
    print(f"Initial Balance: {row[3]}")

conn.close()
