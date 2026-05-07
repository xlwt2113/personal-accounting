import sqlite3
from datetime import datetime

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# For credit card: balance = amount owed = credit_limit - available = 70000 - 63847 = 6153
# Update initial_balance to reflect current owed amount
cursor.execute(
    """UPDATE accounts SET initial_balance = ?, updated_at = ? WHERE name LIKE '%交通银行信用卡%'""",
    (6153.00, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
)
conn.commit()
print("Updated: credit card owed balance set to 6153.00, available credit: 63847")

conn.close()
