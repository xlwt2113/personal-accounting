import sqlite3
import codecs

db_path = r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('SELECT id, name, account_type, initial_balance, credit_limit FROM accounts ORDER BY id')
rows = c.fetchall()

# Write to file with UTF-8
with open(r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\scripts\accounts_output.txt', 'w', encoding='utf-8') as f:
    f.write("id | name | account_type | initial_balance | credit_limit\n")
    f.write("-" * 80 + "\n")
    for row in rows:
        f.write(f"{row}\n")

conn.close()
print("Done")
