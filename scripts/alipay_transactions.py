import sqlite3

conn = sqlite3.connect(r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db')
cursor = conn.cursor()

# Get Alipay account
cursor.execute("SELECT id, name, initial_balance FROM accounts WHERE name = '支付宝'")
alipay = cursor.fetchone()
if not alipay:
    print("支付宝账户不存在")
    conn.close()
    exit()

alipay_id = alipay[0]
print(f"=== 支付宝账户 (ID: {alipay_id}) ===\n")

# Get all transactions for Alipay
cursor.execute("""
    SELECT id, amount, transaction_type, merchant, category, transaction_date, note, created_at
    FROM transactions
    WHERE account_id = ?
    ORDER BY transaction_date DESC, created_at DESC
""", (alipay_id,))
transactions = cursor.fetchall()

# Get transfers involving Alipay
cursor.execute("""
    SELECT id, from_account_id, to_account_id, amount, transfer_time, note
    FROM transfers
    WHERE from_account_id = ? OR to_account_id = ?
    ORDER BY transfer_time DESC
""", (alipay_id, alipay_id))
transfers = cursor.fetchall()

print(f"--- 收支记录 ({len(transactions)} 条) ---")
total_income = 0
total_expense = 0

for t in transactions:
    t_type = "收入" if t[2] == 'income' else "支出"
    if t[2] == 'income':
        total_income += t[1]
    else:
        total_expense += t[1]
    print(f"[{t[5]}] {t_type} {t[1]:.2f} - {t[3] or ''} {t[6] or ''}")

print(f"\n收入合计: {total_income:.2f}")
print(f"支出合计: {total_expense:.2f}")

print(f"\n--- 转账记录 ({len(transfers)} 条) ---")
for tr in transfers:
    direction = "转出" if tr[1] == alipay_id else "转入"
    print(f"[{tr[4]}] {direction} {tr[3]:.2f} - {tr[5] or ''}")

conn.close()