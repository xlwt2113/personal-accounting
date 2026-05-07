import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
conn = sqlite3.connect('C:/Users/wt/.openclaw/workspace/skills/personal-accounting/db/accounting.db')
cur = conn.cursor()

# 删除测试创建的支付宝账户
cur.execute("DELETE FROM accounts WHERE id=22")
print(f"删除了测试账户 id=22")

conn.commit()
print("完成!")