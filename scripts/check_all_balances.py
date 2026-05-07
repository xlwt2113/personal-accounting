import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

DB_PATH = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 获取所有账户
cursor.execute("SELECT id, name, account_type, initial_balance, credit_limit FROM accounts ORDER BY account_type, name")
accounts = cursor.fetchall()

print("=" * 80)
print("账户详细检查")
print("=" * 80)

total_assets = 0
total_liabilities = 0

for acc in accounts:
    acc_id, name, acc_type, init_bal, credit_limit = acc
    
    # 计算该账户的收入和支出
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE account_id = ? AND transaction_type = 'income'", (acc_id,))
    total_income = cursor.fetchone()[0]
    
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE account_id = ? AND transaction_type = 'expense'", (acc_id,))
    total_expense = cursor.fetchone()[0]
    
    if acc_type == 'credit_card':
        # 信用卡：欠款 = initial_balance + 支出 - 收入
        liability = init_bal + total_expense - total_income
        total_liabilities += liability
        print(f"\n【信用卡】{name}")
        print(f"  initial_balance: {init_bal:.2f}")
        print(f"  总支出: {total_expense:.2f}")
        print(f"  总收入: {total_income:.2f}")
        print(f"  欠款: {liability:.2f}")
        print(f"  额度: {credit_limit:.2f}")
    else:
        # 其他账户：余额 = initial_balance + 收入 - 支出
        balance = init_bal + total_income - total_expense
        total_assets += balance
        print(f"\n【资产】{name}")
        print(f"  initial_balance: {init_bal:.2f}")
        print(f"  总收入: {total_income:.2f}")
        print(f"  总支出: {total_expense:.2f}")
        print(f"  余额: {balance:.2f}")

print("\n" + "=" * 80)
print(f"总资产: {total_assets:.2f}")
print(f"总负债: {total_liabilities:.2f}")
print(f"净资产: {total_assets - total_liabilities:.2f}")
print("=" * 80)

conn.close()