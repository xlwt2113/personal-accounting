import sqlite3

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get 招商银行储蓄卡 transactions
cursor.execute("""
    SELECT t.id, t.amount, t.transaction_type, t.merchant, t.category, t.transaction_date, t.note
    FROM transactions t
    JOIN accounts a ON t.account_id = a.id
    WHERE a.name LIKE '%招商银行储蓄卡%'
    ORDER BY t.transaction_date DESC, t.id DESC
""")
transactions = cursor.fetchall()

print("=== 招商银行储蓄卡 收支记录 ===\n")
if transactions:
    for row in transactions:
        t_type = "收入" if row[2] == "income" else "支出"
        print(f"ID: {row[0]}")
        print(f"  日期: {row[5]}")
        print(f"  类型: {t_type}")
        print(f"  金额: {row[1]}")
        print(f"  商户: {row[3]}")
        print(f"  分类: {row[4]}")
        if row[6]:
            print(f"  备注: {row[6]}")
        print()
else:
    print("  No records")

conn.close()
