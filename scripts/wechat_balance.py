import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

DB_PATH = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 获取微信零钱账户信息
cursor.execute("SELECT id, name, initial_balance FROM accounts WHERE name = '微信零钱'")
row = cursor.fetchone()

if row is None:
    print("微信零钱账户不存在")
else:
    account_id, name, initial_balance = row
    
    # 计算收入总额
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE account_id = ? AND transaction_type = 'income'", (account_id,))
    total_income = cursor.fetchone()[0]
    
    # 计算支出总额
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE account_id = ? AND transaction_type = 'expense'", (account_id,))
    total_expense = cursor.fetchone()[0]
    
    balance = initial_balance + total_income - total_expense
    
    print(f"账户：{name}")
    print(f"初始余额：{initial_balance:.2f} 元")
    print(f"收入：+{total_income:.2f} 元")
    print(f"支出：-{total_expense:.2f} 元")
    print(f"当前余额：{balance:.2f} 元")

conn.close()
