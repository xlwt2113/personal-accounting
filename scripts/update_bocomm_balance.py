import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Update credit card balance: owed = 6153 - 1000 = 5153
cursor.execute(
    """UPDATE accounts SET initial_balance = ?, updated_at = ? WHERE id = 5""",
    (5153.00, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
)
conn.commit()
print("Updated credit card owed to 5153.00")

conn.close()
