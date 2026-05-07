import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\wt\\.openclaw\\workspace\\skills\\personal-accounting\\scripts')

from database import get_transactions

# 获取所有交易记录
transactions = get_transactions(limit=500)
print(f"时间 | 类型 | 金额 | 分类 | 商户 | 账户 | 备注")
print("-" * 100)
for t in transactions:
    print(f"{t['transaction_date']} | {t['transaction_type']} | ¥{t['amount']:.2f} | {t['category']} | {t['merchant'] or '-'} | {t['account_name']} | {t['note'] or '-'}")

print(f"\n共 {len(transactions)} 条记录")
