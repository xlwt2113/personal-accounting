# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from database import get_total_by_merchant

# 按商家统计支出
results = get_total_by_merchant(transaction_type='expense')

print("商家消费分组统计（支出）：\n")
total = 0
for r in results:
    total += r['total']
    print(f"{r['merchant']}：{r['count']}笔，合计 ¥{r['total']:.2f}")

print(f"\n总计：{len(results)}个商家，¥{total:.2f}")