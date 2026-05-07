import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

DB_PATH = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("UPDATE accounts SET initial_balance = 39500.0 WHERE name = '光大银行储蓄卡（0771）'")
conn.commit()
print("已恢复光大储蓄卡余额为 39,500.00 元")

conn.close()