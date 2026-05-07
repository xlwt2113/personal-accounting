import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

db_path = r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 资产账户余额
cursor.execute("""
    SELECT name, account_type, initial_balance FROM accounts 
    WHERE account_type IN ('savings_card', 'wechat_wallet', 'alipay', 'cash', 'stock', 'fund')
    ORDER BY account_type, name
""")
asset_accounts = cursor.fetchall()

# 信用卡欠款
cursor.execute("""
    SELECT name, initial_balance, credit_limit FROM accounts 
    WHERE account_type = 'credit_card'
    ORDER BY name
""")
credit_cards = cursor.fetchall()

# 计算每个账户余额
def get_balance(account_id, initial):
    cursor.execute("""
        SELECT transaction_type, SUM(amount) FROM transactions 
        WHERE account_id = ? 
        GROUP BY transaction_type
    """, (account_id,))
    rows = cursor.fetchall()
    income = sum(r[1] for r in rows if r[0] == 'income')
    expense = sum(r[1] for r in rows if r[0] == 'expense')
    return initial + income - expense

# 当月收支
cursor.execute("""
    SELECT transaction_type, SUM(amount) FROM transactions 
    WHERE strftime('%Y-%m', transaction_date) = '2026-05'
    GROUP BY transaction_type
""")
this_month = {r[0]: r[1] for r in cursor.fetchall()}

# 上月收支
cursor.execute("""
    SELECT transaction_type, SUM(amount) FROM transactions 
    WHERE strftime('%Y-%m', transaction_date) = '2026-04'
    GROUP BY transaction_type
""")
last_month = {r[0]: r[1] for r in cursor.fetchall()}

print("=== 财务汇总 2026-05-02 ===")
print()

# 资产账户
total_assets = 0
print("【资产账户】")
for name, atype, init in asset_accounts:
    cursor.execute("SELECT id FROM accounts WHERE name = ?", (name,))
    aid = cursor.fetchone()[0]
    bal = get_balance(aid, init)
    total_assets += bal
    print(f"  {name}: ¥{bal:,.2f}")
print(f"  资产合计: ¥{total_assets:,.2f}")
print()

# 信用卡
total_debt = 0
print("【信用卡欠款】")
for name, init, limit in credit_cards:
    cursor.execute("SELECT id FROM accounts WHERE name = ?", (name,))
    aid = cursor.fetchone()[0]
    bal = get_balance(aid, init)  # init是负数
    debt = abs(bal)
    total_debt += debt
    available = limit - debt
    print(f"  {name}: 欠款 ¥{debt:,.2f} | 额度 ¥{limit:,.2f} | 可用 ¥{available:,.2f}")
print(f"  信用卡欠款合计: ¥{total_debt:,.2f}")
print()

# 净资产
net = total_assets - total_debt
print(f"【净资产】资产 ¥{total_assets:,.2f} - 负债 ¥{total_debt:,.2f} = ¥{net:,.2f}")
print()

# 当月收支
print("【本月收支】(2026-05)")
tm_income = this_month.get('income', 0)
tm_expense = this_month.get('expense', 0)
tm_net = tm_income - tm_expense
print(f"  收入: ¥{tm_income:,.2f}")
print(f"  支出: ¥{tm_expense:,.2f}")
print(f"  净值: ¥{tm_net:,.2f}")
print()

# 上月收支
print("【上月收支】(2026-04)")
lm_income = last_month.get('income', 0)
lm_expense = last_month.get('expense', 0)
lm_net = lm_income - lm_expense
print(f"  收入: ¥{lm_income:,.2f}")
print(f"  支出: ¥{lm_expense:,.2f}")
print(f"  净值: ¥{lm_net:,.2f}")

conn.close()