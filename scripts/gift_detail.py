import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

DB_PATH = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
    SELECT id, amount, transaction_type, merchant, category, transaction_date, note
    FROM transactions
    WHERE category = 'gift'
    ORDER BY transaction_date DESC
""")
rows = cursor.fetchall()

print("gift 分类记录详情：")
print("-" * 50)
for row in rows:
    print(f"ID: {row[0]}")
    print(f"  金额: {row[1]:.2f} 元")
    print(f"  类型: {row[2]}")
    print(f"  商户: {row[3]}")
    print(f"  分类: {row[4]}")
    print(f"  日期: {row[5]}")
    print(f"  备注: {row[6]}")
    print()

conn.close()
