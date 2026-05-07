import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
from datetime import datetime

db_path = r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db'

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# 获取所有账户
cursor.execute("SELECT * FROM accounts ORDER BY account_type, name")
accounts = cursor.fetchall()

# 计算每个账户的余额
def calc_balance(account_id, initial_balance, account_type):
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN transaction_type='income' THEN amount ELSE 0 END) as income,
            SUM(CASE WHEN transaction_type='expense' THEN amount ELSE 0 END) as expense
        FROM transactions WHERE account_id = ?
    """, (account_id,))
    row = cursor.fetchone()
    income = row['income'] or 0
    expense = row['expense'] or 0
    if account_type == 'credit_card':
        # 信用卡：欠款 = initial_balance（负数）+ expense - income，结果取绝对值
        balance = abs(initial_balance + expense - income)
    else:
        balance = initial_balance + income - expense
    return balance, income, expense

# 分类统计
def get_month_summary(year, month):
    start_date = f"{year}-{month:02d}-01"
    if month == 12:
        end_year, end_month = year + 1, 1
    else:
        end_year, end_month = year, month + 1
    end_date = f"{end_year}-{end_month:02d}-01"
    
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN transaction_type='income' THEN amount ELSE 0 END) as income,
            SUM(CASE WHEN transaction_type='expense' THEN amount ELSE 0 END) as expense
        FROM transactions 
        WHERE transaction_date >= ? AND transaction_date < ?
    """, (start_date, end_date))
    row = cursor.fetchone()
    return {
        'income': row['income'] or 0,
        'expense': row['expense'] or 0,
        'net': (row['income'] or 0) - (row['expense'] or 0)
    }

# 当前日期
now = datetime.now()
current_year, current_month = now.year, now.month

# 计算上个月
if current_month == 1:
    last_year, last_month = current_year - 1, 12
else:
    last_year, last_month = current_year, current_month - 1

current_summary = get_month_summary(current_year, current_month)
last_summary = get_month_summary(last_year, last_month)

# 分离资产账户和信用卡
asset_accounts = []
credit_accounts = []
total_assets = 0
total_debt = 0

for acc in accounts:
    balance, income, expense = calc_balance(acc['id'], acc['initial_balance'], acc['account_type'])
    if acc['account_type'] == 'credit_card':
        credit_accounts.append({
            'name': acc['name'],
            'balance': balance,
            'credit_limit': acc['credit_limit'],
            'available': acc['credit_limit'] - balance
        })
        total_debt += balance
    else:
        asset_accounts.append({
            'name': acc['name'],
            'type': acc['account_type'],
            'balance': balance
        })
        total_assets += balance

net_worth = total_assets - total_debt

# 输出汇总
print("=" * 50)
print("📊 财务汇总")
print(f"📅 {current_year}年{current_month}月 | {now.strftime('%Y-%m-%d %H:%M')}")
print("=" * 50)

print("\n💰 净资产")
print(f"   总资产: ¥{total_assets:,.2f}")
print(f"   总负债: ¥{total_debt:,.2f}")
print(f"   净资产: ¥{net_worth:,.2f}")

print("\n📈 收支概况")
print(f"   本月收入: ¥{current_summary['income']:,.2f}")
print(f"   本月支出: ¥{current_summary['expense']:,.2f}")
print(f"   本月净值: ¥{current_summary['net']:,.2f}")
print(f"   ────────")
print(f"   上月收入: ¥{last_summary['income']:,.2f}")
print(f"   上月支出: ¥{last_summary['expense']:,.2f}")
print(f"   上月净值: ¥{last_summary['net']:,.2f}")

print("\n🏦 资产账户")
for acc in asset_accounts:
    type_names = {
        'savings_card': '储蓄卡',
        'wechat_wallet': '微信',
        'alipay': '支付宝',
        'cash': '现金',
        'stock': '股票',
        'fund': '基金',
        'other': '其他'
    }
    tname = type_names.get(acc['type'], acc['type'])
    print(f"   {acc['name']} | {tname} | ¥{acc['balance']:,.2f}")

if credit_accounts:
    print("\n💳 信用卡欠款")
    for acc in credit_accounts:
        print(f"   {acc['name']} | 欠款 ¥{acc['balance']:,.2f} | 额度 ¥{acc['credit_limit']:,.2f} | 可用 ¥{acc['available']:,.2f}")

conn.close()