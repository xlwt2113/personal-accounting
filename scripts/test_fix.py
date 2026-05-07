import sys
sys.path.insert(0, 'C:/Users/wt/.openclaw/workspace/skills/personal-accounting')
from scripts.database import get_or_create_account_from_parser

# 测试场景：只有 source='alipay'，没有 bank_name 和 card_last_four
result = get_or_create_account_from_parser({
    'source': 'alipay'
})
print(f"测试1 (source=alipay): account_id={result[0]}, created={result[1]}")

# 测试场景：bank_name 和 card_last_four 都是 None
result2 = get_or_create_account_from_parser({
    'bank_name': None,
    'card_last_four': None
})
print(f"测试2 (bank_name=None, card_last_four=None): account_id={result2[0]}, created={result2[1]}")