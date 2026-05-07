import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

DB_PATH = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(DB_PATH)
conn.execute('UPDATE transactions SET category = "food", note = "洛馍" WHERE id = 19')
conn.commit()
conn.close()

print("已更新记录19：分类→餐饮，备注→洛馍")
