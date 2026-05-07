import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.database import get_transactions
from collections import defaultdict

# 获取所有支出记录
transactions = get_transactions(transaction_type='expense', limit=1000)

# 按分类汇总
category_totals = defaultdict(lambda: {'count': 0, 'amount': 0})
category_names = {
    'food': '餐饮',
    'transportation': '交通',
    'shopping': '购物',
    'entertainment': '娱乐',
    'bills': '账单',
    'healthcare': '医疗',
    'education': '教育',
    'housing': '住房',
    'investment': '投资理财',
    'other': '其他'
}

for t in transactions:
    cat = t['category']
    category_totals[cat]['count'] += 1
    category_totals[cat]['amount'] += t['amount']

# 按金额排序
sorted_categories = sorted(category_totals.items(), key=lambda x: x[1]['amount'], reverse=True)

# 总计
total_expense = sum(v['amount'] for v in category_totals.values())
total_count = sum(v['count'] for v in category_totals.values())

print("=" * 40)
print("         支出分类汇总")
print("=" * 40)
print(f"\n总支出：-{total_expense:,.2f} 元（共 {total_count} 笔）")
print("\n【分类明细】")
print("-" * 40)

for cat, data in sorted_categories:
    name = category_names.get(cat, cat)
    pct = data['amount'] / total_expense * 100 if total_expense > 0 else 0
    bar = '█' * int(pct / 5) + '░' * (20 - int(pct / 5))
    print(f"  {name}")
    print(f"    金额：{data['amount']:,.2f} 元 | {data['count']} 笔 | 占比：{pct:.1f}%")
    print(f"    {bar}")

conn = None  # get_transactions already handles connection
