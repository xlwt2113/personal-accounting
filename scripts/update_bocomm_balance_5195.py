import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Current owed = 5153 + 41.89 = 5194.89
cursor.execute(
    """UPDATE accounts SET initial_balance = ?, updated_at = ? WHERE id = 5""",
    (5194.89, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
)
conn.commit()
print("Updated credit card owed to 5194.89")

conn.close()
