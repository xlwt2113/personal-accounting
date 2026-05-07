import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
from datetime import datetime

DB_PATH = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

now = datetime.now()
current_month = now.strftime('%Y-%m')

# 按分类汇总当月支出
cursor.execute("""
    SELECT category, SUM(amount), COUNT(*)
    FROM transactions
    WHERE transaction_type = 'expense' AND transaction_date LIKE ?
    GROUP BY category
    ORDER BY SUM(amount) DESC
""", (f"{current_month}%",))
rows = cursor.fetchall()

category_names = {
    'food': '餐饮',
    'transportation': '交通',
    'shopping': '购物',
    'entertainment': '娱乐',
    'bills': '账单',
    'healthcare': '医疗',
    'social': '人情往来',
    'education': '教育',
    'housing': '住房',
    'investment': '投资理财',
    'other': '其他'
}

total = sum(row[1] for row in rows)

print(f"当月（{current_month}）支出分类汇总")
print(f"总支出：-{total:,.2f} 元（共 {sum(row[2] for row in rows)} 笔）")
print("-" * 40)
for row in rows:
    cat, amount, count = row
    name = category_names.get(cat, cat)
    pct = amount / total * 100 if total > 0 else 0
    print(f"{name}: {amount:,.2f} 元 | {count} 笔 | {pct:.1f}%")

conn.close()
