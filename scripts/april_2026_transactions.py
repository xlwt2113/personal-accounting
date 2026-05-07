import sqlite3

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
    SELECT t.id, a.name, t.amount, t.transaction_type, t.merchant, t.category, t.transaction_date
    FROM transactions t
    JOIN accounts a ON t.account_id = a.id
    WHERE t.transaction_date >= '2026-04-01' AND t.transaction_date <= '2026-04-30'
    ORDER BY t.transaction_date ASC, t.id ASC
""")
rows = cursor.fetchall()

if not rows:
    print("No transactions in April 2026")
else:
    total_income = 0
    total_expense = 0
    print(f"{'Date':<12} {'Account':<20} {'Type':<7} {'Amount':>10} {'Merchant':<20} {'Category'}")
    print("-" * 90)
    for row in rows:
        tx_type = "+" if row[3] == "income" else "-"
        if row[3] == "income":
            total_income += row[2]
        else:
            total_expense += row[2]
        print(f"{row[6]:<12} {row[1]:<20} {row[3]:<7} {tx_type}{row[2]:>9.2f}   {row[4]:<20} {row[5]}")
    
    print("-" * 90)
    print(f"Total Income:  +{total_income:.2f}")
    print(f"Total Expense: -{total_expense:.2f}")
    print(f"Net:           {(total_income - total_expense):+.2f}")

conn.close()
