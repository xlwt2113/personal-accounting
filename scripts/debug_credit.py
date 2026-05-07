import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

DB_PATH = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 查看所有信用卡账户及其initial_balance
cursor.execute("SELECT id, name, account_type, initial_balance, credit_limit FROM accounts WHERE account_type = 'credit_card'")
credit_accounts = cursor.fetchall()

print("=== 信用卡账户 ===")
total_liabilities = 0
for acc in credit_accounts:
    acc_id, name, acc_type, init_bal, credit_limit = acc
    
    # 计算该信用卡的支出和收入
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE account_id = ? AND transaction_type = 'expense'", (acc_id,))
    total_expense = cursor.fetchone()[0]
    
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE account_id = ? AND transaction_type = 'income'", (acc_id,))
    total_income = cursor.fetchone()[0]
    
    # 欠款 = 支出 - 收入
    liability = total_expense - total_income
    
    print(f"\n{name}")
    print(f"  initial_balance: {init_bal}")
    print(f"  credit_limit: {credit_limit}")
    print(f"  total_expense: {total_expense}")
    print(f"  total_income: {total_income}")
    print(f"  欠款(支出-收入): {liability}")
    
    total_liabilities += liability

print(f"\n=== 总负债（所有信用卡欠款之和）===")
print(f"总负债: {total_liabilities}")

conn.close()
