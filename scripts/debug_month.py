import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

db_path = r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

now = __import__('datetime').datetime.now()
current_year, current_month = now.year, now.month

start_date = f"{current_year}-{current_month:02d}-01 00:00:00"
if current_month == 12:
    end_year, end_month = current_year + 1, 1
else:
    end_year, end_month = current_year, current_month + 1
end_date = f"{end_year}-{end_month:02d}-01 00:00:00"

print(f"当前: {current_year}-{current_month:02d}")
print(f"查询区间: [{start_date}, {end_date})")

cursor.execute("""
    SELECT COUNT(*) as cnt,
        SUM(CASE WHEN transaction_type='income' THEN amount ELSE 0 END) as income,
        SUM(CASE WHEN transaction_type='expense' THEN amount ELSE 0 END) as expense
    FROM transactions 
    WHERE transaction_date >= ? AND transaction_date < ?
""", (start_date, end_date))
row = cursor.fetchone()
print(f"查询结果: cnt={row['cnt']}, income={row['income']}, expense={row['expense']}")

# 检查原始数据
print("\n原始transaction_date字段值:")
cursor.execute("SELECT id, transaction_date, typeof(transaction_date) FROM transactions")
for r in cursor.fetchall():
    print(f"  ID={r['id']}: '{r['transaction_date']}' (type={r['typeof(transaction_date)']})")

conn.close()