import sys
sys.path.insert(0, 'C:/Users/wt/.openclaw/workspace/skills/personal-accounting')
from scripts.parser import parse_and_save_transactions

result = parse_and_save_transactions([{
    'amount': 7.00,
    'transaction_type': 'expense',
    'source': 'alipay',
    'merchant': '烙馍卷菜',
    'category': 'food',
    'transaction_date': '2026-05-03 07:37:51'
}])

print(f"解析账单完成: total_parsed={result['total_parsed']}, total_saved={result['total_saved']}, created_accounts={result['created_accounts']}")