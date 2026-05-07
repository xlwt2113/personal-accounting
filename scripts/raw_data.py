import sqlite3
db_path = r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('SELECT id, name, account_type, initial_balance, credit_limit FROM accounts ORDER BY id')
print("ID | account_type | initial_balance | credit_limit | name")
for row in c.fetchall():
    print(row)
conn.close()
