import sqlite3

conn = sqlite3.connect(r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db')
cursor = conn.cursor()

print("=== 招商银行储蓄卡 收支明细 ===\n")

# Get CMB account
cursor.execute("SELECT id, name, initial_balance FROM accounts WHERE account_type = 'savings_card' LIMIT 1")
cmb = cursor.fetchone()
if not cmb:
    print("招商银行储蓄卡不存在")
    conn.close()
    exit()

cmb_id = cmb[0]
print(f"账户: {cmb[1]} (ID: {cmb_id})\n")

# Get all transactions for CMB
cursor.execute("""
    SELECT id, amount, transaction_type, merchant, category, transaction_date, note, created_at
    FROM transactions
    WHERE account_id = ?
    ORDER BY transaction_date DESC, created_at DESC
""", (cmb_id,))
transactions = cursor.fetchall()

# Get transfers involving CMB
cursor.execute("""
    SELECT id, from_account_id, to_account_id, amount, transfer_time, note
    FROM transfers
    WHERE from_account_id = ? OR to_account_id = ?
    ORDER BY transfer_time DESC
""", (cmb_id, cmb_id))
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
    direction = "转出" if tr[1] == cmb_id else "转入"
    print(f"[{tr[4]}] {direction} {tr[3]:.2f} - {tr[5] or ''}")

conn.close()