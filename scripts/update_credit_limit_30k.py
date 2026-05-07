import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Update credit limit to 30000
cursor.execute(
    """UPDATE accounts SET credit_limit = ?, updated_at = ? WHERE name LIKE '%招商银行信用卡%'""",
    (30000.00, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
)
conn.commit()
print("Credit limit updated to 30000.00")

conn.close()
