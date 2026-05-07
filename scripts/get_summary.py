import sqlite3
from datetime import datetime, timedelta
import os

db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

def get_summary():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Get all accounts with balances
    c.execute("""
        SELECT id, name, account_type, initial_balance, credit_limit 
        FROM accounts ORDER BY account_type, name
    """)
    accounts = c.fetchall()
    
    # Calculate balance for each account
    account_balances = []
    for acc in accounts:
        acc_id, name, acc_type, initial, credit_limit = acc
        
        # Get total income and expense for this account
        c.execute("""
            SELECT 
                COALESCE(SUM(CASE WHEN transaction_type='income' THEN amount ELSE 0 END), 0) as income,
                COALESCE(SUM(CASE WHEN transaction_type='expense' THEN amount ELSE 0 END), 0) as expense
            FROM transactions WHERE account_id = ?
        """, (acc_id,))
        income, expense = c.fetchone()
        
        if acc_type == 'credit_card':
            balance = credit_limit - expense + income
            balance_type = "剩余额度"
        else:
            balance = initial + income - expense
            balance_type = "余额"
        
        account_balances.append({
            'id': acc_id,
            'name': name,
            'type': acc_type,
            'balance': balance,
            'balance_type': balance_type,
            'income': income,
            'expense': expense
        })
    
    # Get overall totals
    c.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN transaction_type='income' THEN amount ELSE 0 END), 0) as total_income,
            COALESCE(SUM(CASE WHEN transaction_type='expense' THEN amount ELSE 0 END), 0) as total_expense
        FROM transactions
    """)
    total_income, total_expense = c.fetchone()
    
    # Get this month's stats
    today = datetime.now()
    first_day_of_month = today.replace(day=1).strftime('%Y-%m-%d')
    
    c.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN transaction_type='income' THEN amount ELSE 0 END), 0) as month_income,
            COALESCE(SUM(CASE WHEN transaction_type='expense' THEN amount ELSE 0 END), 0) as month_expense
        FROM transactions WHERE transaction_date >= ?
    """, (first_day_of_month,))
    month_income, month_expense = c.fetchone()
    
    # Get expense breakdown by category this month
    c.execute("""
        SELECT category, SUM(amount) as total
        FROM transactions 
        WHERE transaction_type='expense' AND transaction_date >= ?
        GROUP BY category
        ORDER BY total DESC
    """, (first_day_of_month,))
    category_breakdown = c.fetchall()
    
    # Get income breakdown by category this month
    c.execute("""
        SELECT category, SUM(amount) as total
        FROM transactions 
        WHERE transaction_type='income' AND transaction_date >= ?
        GROUP BY category
        ORDER BY total DESC
    """, (first_day_of_month,))
    income_breakdown = c.fetchall()
    
    # Recent transactions (last 10)
    c.execute("""
        SELECT t.amount, t.transaction_type, t.merchant, t.category, t.transaction_date, a.name
        FROM transactions t
        JOIN accounts a ON t.account_id = a.id
        ORDER BY t.transaction_date DESC, t.id DESC
        LIMIT 10
    """)
    recent = c.fetchall()
    
    conn.close()
    
    return {
        'accounts': account_balances,
        'total_income': total_income,
        'total_expense': total_expense,
        'month_income': month_income,
        'month_expense': month_expense,
        'category_breakdown': category_breakdown,
        'income_breakdown': income_breakdown,
        'recent': recent,
        'month_start': first_day_of_month
    }

result = get_summary()

print("=" * 50)
print("[财务汇总报告]")
print("=" * 50)

print("\n[账户概览]")
for acc in result['accounts']:
    print(f"  {acc['name']}: ¥{acc['balance']:,.2f} ({acc['balance_type']})")

total_assets = sum(a['balance'] for a in result['accounts'])
print(f"\n总资产: ¥{total_assets:,.2f}")

print(f"\n[{result['month_start']} 至今]")
print(f"  收入: ¥{result['month_income']:,.2f}")
print(f"  支出: ¥{result['month_expense']:,.2f}")
print(f"  结余: ¥{result['month_income'] - result['month_expense']:,.2f}")

if result['category_breakdown']:
    print("\n[本月支出分类]")
    for cat, total in result['category_breakdown']:
        print(f"  {cat}: ¥{total:,.2f}")

if result['income_breakdown']:
    print("\n[本月收入分类]")
    for cat, total in result['income_breakdown']:
        print(f"  {cat}: ¥{total:,.2f}")

print("\n[最近交易]")
for t in result['recent']:
    amount, typ, merchant, cat, date, acc_name = t
    sign = "+" if typ == 'income' else "-"
    print(f"  {date} {sign}¥{amount:,.2f} {merchant or cat} ({acc_name})")

print("\n" + "=" * 50)
