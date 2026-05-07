import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

db_path = r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# 检查日期范围
cursor.execute("""
    SELECT 
        MIN(transaction_date) as min_date,
        MAX(transaction_date) as max_date,
        COUNT(*) as total
    FROM transactions
""")
row = cursor.fetchone()
print(f"数据库日期范围: {row['min_date']} ~ {row['max_date']}, 共{row['total']}条")

# 测试当前月份查询逻辑
print("\n测试当前查询逻辑 (>=2026-05-01 AND <2026-06-01):")
cursor.execute("""
    SELECT COUNT(*) as cnt,
        SUM(CASE WHEN transaction_type='income' THEN amount ELSE 0 END) as income,
        SUM(CASE WHEN transaction_type='expense' THEN amount ELSE 0 END) as expense
    FROM transactions 
    WHERE transaction_date >= '2026-05-01' AND transaction_date < '2026-06-01'
""")
r = cursor.fetchone()
print(f"  记录数: {r['cnt']}, 收入: {r['income']}, 支出: {r['expense']}")

# 用LIKE匹配测试
print("\n用 LIKE '2026-05%' 测试:")
cursor.execute("""
    SELECT COUNT(*) as cnt,
        SUM(CASE WHEN transaction_type='income' THEN amount ELSE 0 END) as income,
        SUM(CASE WHEN transaction_type='expense' THEN amount ELSE 0 END) as expense
    FROM transactions 
    WHERE transaction_date LIKE '2026-05%'
""")
r = cursor.fetchone()
print(f"  记录数: {r['cnt']}, 收入: {r['income']}, 支出: {r['expense']}")

# 检查所有5月的记录
print("\n所有5月记录:")
cursor.execute("""
    SELECT id, transaction_date, transaction_type, amount, merchant
    FROM transactions 
    WHERE transaction_date >= '2026-05-01'
    ORDER BY transaction_date
""")
for r in cursor.fetchall():
    print(f"  ID={r['id']} | {r['transaction_date']} | {r['transaction_type']} | ¥{r['amount']} | {r['merchant']}")

conn.close()