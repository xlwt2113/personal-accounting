import sqlite3
db_path = r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('SELECT * FROM accounts')
rows = c.fetchall()

# Get column names
c.execute('PRAGMA table_info(accounts)')
cols = [col[1] for col in c.fetchall()]

print("Columns:", cols)
print()
for row in rows:
    print(row)
conn.close()
