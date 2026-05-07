import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\wt\\.openclaw\\workspace\\skills\\personal-accounting\\scripts')

from database import get_account_by_name

account = get_account_by_name("中信银行信用卡（7379）")
print(f"账户: {account}")
print(f"欠款: ¥{abs(account['current_balance']):.2f}")
print(f"额度: ¥{account['credit_limit']:.2f}")
print(f"可用: ¥{account['credit_limit'] - abs(account['current_balance']):.2f}")
