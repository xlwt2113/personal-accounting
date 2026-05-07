import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\wt\\.openclaw\\workspace\\skills\\personal-accounting\\scripts')

from database import update_account, get_account_by_name

account = get_account_by_name("中原银行信用卡（8599）")
print(f"当前账户: {account}")

# 更新额度为20000
result = update_account(account['id'], credit_limit=20000)
print(f"更新结果: {result}")

# 重新查询
account = get_account_by_name("中原银行信用卡（8599）")
print(f"更新后账户: {account}")
