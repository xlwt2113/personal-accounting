import sqlite3
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

today = datetime.now()
current_month_start = today.replace(day=1, hour=0, minute=0, second=0)
last_month_start = (current_month_start.month - 1 if current_month_start.month > 1 else 12)
last_month_year = current_month_start.year if current_month_start.month > 1 else current_month_start.year - 1
if current_month_start.month == 1:
    last_month_start = 12
    last_month_year = today.year - 1
else:
    last_month_year = today.year
    last_month_start = current_month_start.month - 1

def get_month_stats(year, month):
    start = f"{year}-{month:02d}-01 00:00"
    if month == 12:
        end_year = year + 1
        end_month = 1
    else:
        end_year = year
        end_month = month + 1
    end = f"{end_year}-{end_month:02d}-01 00:00"

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0) FROM transactions
        WHERE transaction_type = 'income' AND transaction_date >= ? AND transaction_date < ?
    """, (start, end))
    income = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0) FROM transactions
        WHERE transaction_type = 'expense' AND transaction_date >= ? AND transaction_date < ?
    """, (start, end))
    expense = cursor.fetchone()[0]

    return income, expense

# Current month stats
curr_income, curr_expense = get_month_stats(today.year, today.month)
curr_net = curr_income - curr_expense

# Last month stats
last_income, last_expense = get_month_stats(last_month_year, last_month_start)
last_net = last_income - last_expense

# Get all accounts with balances
cursor.execute("""
    SELECT id, name, account_type, initial_balance, credit_limit FROM accounts
    ORDER BY account_type, name
""")
accounts = cursor.fetchall()

# Calculate balances for each account
account_details = []
total_assets = 0.0
total_liabilities = 0.0

for acc in accounts:
    acc_id, name, acc_type, initial, credit_limit = acc

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0) FROM transactions
        WHERE account_id = ? AND transaction_type = 'income'
    """, (acc_id,))
    total_income = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0) FROM transactions
        WHERE account_id = ? AND transaction_type = 'expense'
    """, (acc_id,))
    total_expense = cursor.fetchone()[0]

    balance = initial + total_income - total_expense

    if acc_type == 'credit_card':
        total_liabilities += abs(balance)
        account_details.append({
            'name': name,
            'type': 'credit_card',
            'balance': balance,
            'credit_limit': credit_limit,
            'available': credit_limit - abs(balance)
        })
    else:
        total_assets += balance
        account_details.append({
            'name': name,
            'type': acc_type,
            'balance': balance
        })

net_assets = total_assets - total_liabilities

# Print summary
print("=" * 50)
print("财务晚报")
print(f"时间: {today.strftime('%Y年%m月%d日 %H:%M')}")
print("=" * 50)

print("\n【净资产】")
print(f"  总资产: ¥{total_assets:,.2f}")
print(f"  总负债: ¥{total_liabilities:,.2f}")
print(f"  净资产: ¥{net_assets:,.2f}")

print("\n【收支概况】")
print(f"  本月收入: ¥{curr_income:,.2f}")
print(f"  本月支出: ¥{curr_expense:,.2f}")
print(f"  本月净值: ¥{curr_net:,.2f}")
print(f"  --")
print(f"  上月收入: ¥{last_income:,.2f}")
print(f"  上月支出: ¥{last_expense:,.2f}")
print(f"  上月净值: ¥{last_net:,.2f}")

asset_accounts = [a for a in account_details if a['type'] != 'credit_card']
credit_accounts = [a for a in account_details if a['type'] == 'credit_card']

if asset_accounts:
    print("\n【资产账户】")
    for acc in asset_accounts:
        type_name = {
            'savings_card': '储蓄卡',
            'wechat_wallet': '微信零钱',
            'alipay': '支付宝',
            'cash': '现金',
            'stock': '股票',
            'fund': '基金',
            'other': '其他'
        }.get(acc['type'], acc['type'])
        print(f"  {acc['name']} | {type_name} | ¥{acc['balance']:,.2f}")

if credit_accounts:
    print("\n【信用卡欠款】")
    for acc in credit_accounts:
        print(f"  {acc['name']} | 欠款 ¥{abs(acc['balance']):,.2f} | 额度 ¥{acc['credit_limit']:,.2f} | 可用 ¥{acc['available']:,.2f}")

conn.close()