import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
from datetime import datetime

DB = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

today = datetime.now().strftime("%Y-%m-%d")
current_month = today[:7]
last_month = (datetime.strptime(today + "-01", "%Y-%m-%d").replace(day=1)).strftime("%Y-%m")

def get_month_summary(month):
    cur.execute(f"""
        SELECT SUM(CASE WHEN transaction_type='income' THEN amount ELSE 0 END),
               SUM(CASE WHEN transaction_type='expense' THEN amount ELSE 0 END)
        FROM transactions WHERE transaction_date LIKE '{month}%'
    """)
    row = cur.fetchone()
    return row[0] or 0, row[1] or 0

def get_net_asset():
    cur.execute("SELECT name, account_type, initial_balance FROM accounts")
    rows = cur.fetchall()
    total_asset = 0
    total_liability = 0
    accounts_info = []
    credit_info = []
    for name, atype, init_bal in rows:
        cur.execute("""
            SELECT SUM(CASE WHEN transaction_type='income' THEN amount ELSE 0 END),
                   SUM(CASE WHEN transaction_type='expense' THEN amount ELSE 0 END)
            FROM transactions WHERE account_id=(
                SELECT id FROM accounts WHERE name=?
            )
        """, (name,))
        inc, exp = cur.fetchone()
        inc = inc or 0
        exp = exp or 0
        balance = init_bal + inc - exp
        if atype == 'credit_card':
            owed = abs(balance)
            cur.execute("SELECT credit_limit FROM accounts WHERE name=?", (name,))
            limit = cur.fetchone()[0] or 0
            credit_info.append((name, owed, limit, limit - owed))
            total_liability += owed
        else:
            total_asset += balance
            accounts_info.append((name, atype, balance))
    return total_asset, total_liability, total_asset - total_liability, accounts_info, credit_info

def get_top_categories(month):
    cur.execute(f"""
        SELECT category, SUM(amount) as total
        FROM transactions
        WHERE transaction_type='expense' AND transaction_date LIKE '{month}%'
        GROUP BY category
        ORDER BY total DESC
        LIMIT 5
    """)
    return cur.fetchall()

print("=" * 28)
print("   财务早报 · " + datetime.now().strftime("%Y-%m-%d"))
print("=" * 28)

total_asset, total_liability, net_asset, accounts_info, credit_info = get_net_asset()

print(f"\n📊 净资产")
print(f"   总资产  ¥{total_asset:,.2f}")
print(f"   总负债  ¥{total_liability:,.2f}")
print(f"   净资产  ¥{net_asset:,.2f}")

cur_inc, cur_exp = get_month_summary(current_month)
last_inc, last_exp = get_month_summary(last_month)

print(f"\n💰 收支概况（{current_month}）")
print(f"   收入  ¥{cur_inc:,.2f}")
print(f"   支出  ¥{cur_exp:,.2f}")
print(f"   净值  ¥{cur_inc - cur_exp:,.2f}")

print(f"\n📌 上月（{last_month}）")
print(f"   收入  ¥{last_inc:,.2f}")
print(f"   支出  ¥{last_exp:,.2f}")
print(f"   净值  ¥{last_inc - last_exp:,.2f}")

print(f"\n🏦 资产账户")
for name, atype, bal in accounts_info:
    print(f"   {name}  ¥{bal:,.2f}")

if credit_info:
    print(f"\n💳 信用卡欠款")
    for name, owed, limit, avail in credit_info:
        print(f"   {name}  欠款 ¥{owed:,.2f}  额度 ¥{limit:,.2f}  可用 ¥{avail:,.2f}")

top = get_top_categories(current_month)
if top:
    print(f"\n🔝 本月支出 TOP5")
    for cat, total in top:
        print(f"   {cat}  ¥{total:,.2f}")

conn.close()
