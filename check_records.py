import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
    SELECT id, merchant, amount, category, transaction_date 
    FROM transactions 
    WHERE merchant IN ('上海华程国际旅行社', '高德打车')
    ORDER BY id DESC
""")
results = cursor.fetchall()

for r in results:
    print(f"ID:{r[0]} | {r[1]} | ¥{r[2]} | {r[3]} | {r[4]}")

conn.close()