import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

DB_PATH = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 获取光大储蓄卡账户信息
cursor.execute("SELECT id, initial_balance FROM accounts WHERE name = '光大银行储蓄卡（0771）'")
row = cursor.fetchone()
account_id, current_initial = row

# 计算该账户的总收入和总支出
cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE account_id = ? AND transaction_type = 'income'", (account_id,))
total_income = cursor.fetchone()[0]

cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE account_id = ? AND transaction_type = 'expense'", (account_id,))
total_expense = cursor.fetchone()[0]

# 计算正确的initial_balance
# 余额 = initial_balance + 收入 - 支出
# 17438.33 = initial_balance + income - expense
correct_initial = 17438.33 - total_income + total_expense

print(f"当前 initial_balance: {current_initial}")
print(f"总收入: {total_income}")
print(f"总支出: {total_expense}")
print(f"计算出的正确 initial_balance: {correct_initial:.2f}")

# 更新
cursor.execute("UPDATE accounts SET initial_balance = ? WHERE id = ?", (correct_initial, account_id))
conn.commit()

# 验证
cursor.execute("SELECT initial_balance FROM accounts WHERE id = ?", (account_id,))
new_initial = cursor.fetchone()[0]
print(f"已更新 initial_balance 为: {new_initial:.2f}")

conn.close()