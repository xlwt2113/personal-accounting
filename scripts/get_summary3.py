import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
from datetime import datetime

db_path = r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('SELECT id, name, account_type, initial_balance, credit_limit FROM accounts ORDER BY account_type, name')
accounts = c.fetchall()

print("=" * 55)
print("           财务汇总报告")
print("=" * 55)

# Calculate assets and liabilities
savings_total = 0      # 储蓄卡 + 现金
credit_total = 0       # 信用卡负债
other_total = 0        # 其他账户（支付宝、微信、基金、股票等）

savings_accounts = []
credit_accounts = []
other_accounts = []

for acc in accounts:
    acc_id, name, acc_type, initial, credit_limit = acc
    c.execute('SELECT COALESCE(SUM(CASE WHEN transaction_type="income" THEN amount ELSE 0 END), 0), COALESCE(SUM(CASE WHEN transaction_type="expense" THEN amount ELSE 0 END), 0) FROM transactions WHERE account_id = ?', (acc_id,))
    income, expense = c.fetchone()

    if acc_type == 'savings_card' or acc_type == 'cash':
        balance = initial + income - expense
        savings_total += balance
        savings_accounts.append((name, balance))
    elif acc_type == 'credit_card':
        # initial_balance 是已用金额（欠款）
        owed = initial
        credit_total += owed
        credit_accounts.append((name, owed, credit_limit))
    else:
        # alipay, wechat_wallet, stock, fund, etc.
        balance = initial + income - expense
        other_total += balance
        other_accounts.append((name, balance))

# Month stats
today = datetime.now()
first_day = today.replace(day=1).strftime('%Y-%m-%d')
c.execute('SELECT COALESCE(SUM(CASE WHEN transaction_type="income" THEN amount ELSE 0 END), 0), COALESCE(SUM(CASE WHEN transaction_type="expense" THEN amount ELSE 0 END), 0) FROM transactions WHERE transaction_date >= ?', (first_day,))
month_income, month_expense = c.fetchone()

# Net worth
net_worth = savings_total + other_total - credit_total

print("\n[储蓄卡/现金]")
for name, balance in savings_accounts:
    print(f"  {name}: CNY {balance:,.2f}")
print(f"  储蓄卡小计: CNY {savings_total:,.2f}")

print("\n[信用卡欠款]")
for name, owed, limit in credit_accounts:
    print(f"  {name}: CNY {owed:,.2f} (额度 CNY {limit:,.2f})")
print(f"  信用卡欠款合计: CNY {credit_total:,.2f}")

print("\n[其他账户]")
for name, balance in other_accounts:
    print(f"  {name}: CNY {balance:,.2f}")
print(f"  其他账户小计: CNY {other_total:,.2f}")

print(f"\n[本月统计] {first_day} 至今")
print(f"  收入: CNY {month_income:,.2f}")
print(f"  支出: CNY {month_expense:,.2f}")
print(f"  结余: CNY {month_income - month_expense:,.2f}")

print(f"\n[净资产]")
print(f"  储蓄卡+现金: CNY {savings_total:,.2f}")
print(f"  其他账户: CNY {other_total:,.2f}")
print(f"  信用卡欠款: CNY -{credit_total:,.2f}")
print(f"  净资产: CNY {net_worth:,.2f}")

print("\n" + "=" * 55)
conn.close()
