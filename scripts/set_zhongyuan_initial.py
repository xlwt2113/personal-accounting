import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\wt\\.openclaw\\workspace\\skills\\personal-accounting\\scripts')

from database import update_account, get_account_by_name

account = get_account_by_name("中原银行信用卡（8599）")
print(f"当前: {account}")

# 直接设置初始欠款为49.99
result = update_account(account['id'], initial_balance=-49.99)
print(f"更新结果: {result}")

account = get_account_by_name("中原银行信用卡（8599）")
print(f"更新后: {account}")
print(f"欠款: ¥{abs(account['current_balance']):.2f}")
print(f"额度: ¥{account['credit_limit']:.2f}")
print(f"可用: ¥{account['credit_limit'] - abs(account['current_balance']):.2f}")
