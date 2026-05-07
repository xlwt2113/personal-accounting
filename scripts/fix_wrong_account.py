import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
conn = sqlite3.connect('C:/Users/wt/.openclaw/workspace/skills/personal-accounting/db/accounting.db')
cur = conn.cursor()

# 1. 把交易记录修正到余额宝账户（account_id=10）
cur.execute("UPDATE transactions SET account_id=10 WHERE id=38")
print(f"更新交易记录: id=38, account_id=10 (余额宝)")

# 2. 删除错误创建的储蓄卡（0000）账户
cur.execute("DELETE FROM accounts WHERE id=21")
print(f"删除错误账户: id=21 (储蓄卡0000)")

conn.commit()
print("完成!")