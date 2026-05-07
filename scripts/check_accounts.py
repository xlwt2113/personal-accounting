import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
conn = sqlite3.connect('C:/Users/wt/.openclaw/workspace/skills/personal-accounting/db/accounting.db')
cur = conn.cursor()
cur.execute('SELECT id, name, account_type, initial_balance FROM accounts ORDER BY id')
rows = cur.fetchall()
for r in rows:
    print(r)