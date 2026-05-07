import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\wt\\.openclaw\\workspace\\skills\\personal-accounting\\scripts')

from database import get_account_by_name

a = get_account_by_name("中原银行信用卡（8599）")
print(f"欠款: ¥{abs(a['current_balance']):.2f}")
print(f"额度: ¥{a['credit_limit']:.2f}")
print(f"可用: ¥{a['credit_limit'] - abs(a['current_balance']):.2f}")
