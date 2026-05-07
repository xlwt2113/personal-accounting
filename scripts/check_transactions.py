import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

db_path = r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# 查看最近的交易记录
cursor.execute("""
    SELECT id, amount, transaction_type, account_id, merchant, category, transaction_date
    FROM transactions 
    ORDER BY transaction_date DESC 
    LIMIT 30
""")
rows = cursor.fetchall()

print("最近30条交易记录：")
for r in rows:
    print(f"ID={r['id']} | {r['transaction_date']} | {r['transaction_type']} | ¥{r['amount']} | {r['merchant']} | cat={r['category']}")

conn.close()