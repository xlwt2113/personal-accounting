import sqlite3
conn = sqlite3.connect(r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db')
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM transactions')
print('Total transactions:', c.fetchone()[0])
c.execute('SELECT COUNT(*) FROM accounts')
print('Total accounts:', c.fetchone()[0])
conn.close()
