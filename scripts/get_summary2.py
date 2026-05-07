import sqlite3
from datetime import datetime

db_path = r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db'

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Get all accounts
c.execute('SELECT id, name, account_type, initial_balance, credit_limit FROM accounts ORDER BY account_type, name')
accounts = c.fetchall()

print('=== Account Overview ===')
for acc in accounts:
    acc_id, name, acc_type, initial, credit_limit = acc
    c.execute('SELECT COALESCE(SUM(CASE WHEN transaction_type="income" THEN amount ELSE 0 END), 0), COALESCE(SUM(CASE WHEN transaction_type="expense" THEN amount ELSE 0 END), 0) FROM transactions WHERE account_id = ?', (acc_id,))
    income, expense = c.fetchone()
    if acc_type == 'credit_card':
        balance = credit_limit - expense + income
        print(f'{name}: CNY {balance:,.2f} (credit limit remaining)')
    else:
        balance = initial + income - expense
        print(f'{name}: CNY {balance:,.2f}')

# Month stats
today = datetime.now()
first_day = today.replace(day=1).strftime('%Y-%m-%d')

c.execute('SELECT COALESCE(SUM(CASE WHEN transaction_type="income" THEN amount ELSE 0 END), 0), COALESCE(SUM(CASE WHEN transaction_type="expense" THEN amount ELSE 0 END), 0) FROM transactions WHERE transaction_date >= ?', (first_day,))
month_income, month_expense = c.fetchone()

print(f'\n=== {first_day} to present ===')
print(f'Income: CNY {month_income:,.2f}')
print(f'Expense: CNY {month_expense:,.2f}')
print(f'Net: CNY {month_income - month_expense:,.2f}')

# Category breakdown
print('\n=== Expense by Category (this month) ===')
c.execute('SELECT category, SUM(amount) as total FROM transactions WHERE transaction_type="expense" AND transaction_date >= ? GROUP BY category ORDER BY total DESC', (first_day,))
for cat, total in c.fetchall():
    print(f'{cat}: CNY {total:,.2f}')

print('\n=== Income by Category (this month) ===')
c.execute('SELECT category, SUM(amount) as total FROM transactions WHERE transaction_type="income" AND transaction_date >= ? GROUP BY category ORDER BY total DESC', (first_day,))
for cat, total in c.fetchall():
    print(f'{cat}: CNY {total:,.2f}')

# Recent transactions
print('\n=== Recent Transactions ===')
c.execute('SELECT t.amount, t.transaction_type, t.merchant, t.category, t.transaction_date, a.name FROM transactions t JOIN accounts a ON t.account_id = a.id ORDER BY t.transaction_date DESC, t.id DESC LIMIT 10')
for t in c.fetchall():
    amount, typ, merchant, cat, date, acc_name = t
    sign = "+" if typ == 'income' else "-"
    print(f'{date} {sign}CNY {amount:,.2f} {merchant or cat} ({acc_name})')

conn.close()
