import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

db_path = r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# 直接打印SQL参数
start_date = '2026-05-01 00:00:00'
end_date = '2026-06-01 00:00:00'

# 测试参数化查询
cursor.execute("SELECT COUNT(*) as cnt FROM transactions WHERE transaction_date >= ? AND transaction_date < ?", (start_date, end_date))
row1 = cursor.fetchone()
print(f"参数化查询结果: cnt={row1['cnt']}")

# 测试硬编码查询（验证数据是否存在）
cursor.execute("SELECT COUNT(*) as cnt FROM transactions WHERE transaction_date >= '2026-05-01' AND transaction_date < '2026-06-01'")
row2 = cursor.fetchone()
print(f"硬编码(无时间)查询结果: cnt={row2['cnt']}")

cursor.execute("SELECT COUNT(*) as cnt FROM transactions WHERE transaction_date >= '2026-05-01 00:00:00' AND transaction_date < '2026-06-01 00:00:00'")
row3 = cursor.fetchone()
print(f"硬编码(有时分秒)查询结果: cnt={row3['cnt']}")

# 查看数据实际存储格式
cursor.execute("SELECT id, transaction_date FROM transactions WHERE transaction_date LIKE '2026-05%'")
print("\n5月数据:")
for r in cursor.fetchall():
    print(f"  id={r['id']}, date='{r['transaction_date']}', len={len(r['transaction_date'])}")

conn.close()