import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\wt\\.openclaw\\workspace\\skills\\personal-accounting\\scripts')

from database import update_account, get_account_by_name

account = get_account_by_name("中原银行信用卡（8599）")
print(f"当前账户: {account}")

# 用户说：额度2万，当前剩余额度19950.01（这是包含那17.31已还后的状态）
# 所以当前欠款 = 20000 - 19950.01 = 49.99
# 系统中已记录17.31收入
# initial_balance + 17.31 = -49.99
# initial_balance = -49.99 - 17.31 = -67.30

# 等等，但这样current_balance就不对了...
# current_balance = -67.30 + 17.31 = -49.99 ✓

new_initial_balance = -67.30
result = update_account(account['id'], initial_balance=new_initial_balance)
print(f"更新结果: {result}")

account = get_account_by_name("中原银行信用卡（8599）")
print(f"更新后账户: {account}")
print(f"欠款: ¥{abs(account['current_balance']):.2f}")
print(f"可用: ¥{account['credit_limit'] - abs(account['current_balance']):.2f}")
