import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\wt\\.openclaw\\workspace\\skills\\personal-accounting\\scripts')

from database import add_transfer, get_account_by_name, get_or_create_account

# 检查中原银行信用卡是否存在，不存在则创建
to_account = get_account_by_name("中原银行信用卡（8599）")
if not to_account:
    print("创建中原银行信用卡账户...")
    account_id = get_or_create_account("中原银行信用卡（8599）", "credit_card", initial_balance=0, credit_limit=0)
    to_account = get_account_by_name("中原银行信用卡（8599）")
    print(f"已创建: {to_account}")

from_account = get_account_by_name("余额宝")
print(f"转出账户: {from_account}")
print(f"转入账户: {to_account}")

if from_account and to_account:
    transfer_id = add_transfer(
        from_account_id=from_account['id'],
        to_account_id=to_account['id'],
        amount=17.31,
        transfer_time="2026-05-02 19:58:48",
        note="信用卡还款"
    )
    print(f"转账记录已创建，transfer_id: {transfer_id}")
else:
    print("账户未找到")
