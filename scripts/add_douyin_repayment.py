import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\wt\\.openclaw\\workspace\\skills\\personal-accounting\\scripts')

from database import add_transfer, get_account_by_name, get_or_create_account

# 确保抖音月付账户存在
douyin_account = get_account_by_name("抖音月付")
if not douyin_account:
    print("创建抖音月付账户...")
    account_id = get_or_create_account("抖音月付", "other", initial_balance=0, credit_limit=0)
    douyin_account = get_account_by_name("抖音月付")
    print(f"抖音月付账户已创建: {douyin_account}")
else:
    print(f"抖音月付账户已存在: {douyin_account}")

# 查找储蓄卡账户
from_account = get_account_by_name("招商银行储蓄卡（5063）")
print(f"转出账户: {from_account}")
print(f"抖音月付账户: {douyin_account}")

if from_account and douyin_account:
    # 记录转账：抖音月付还款 355.98 元
    transfer_id = add_transfer(
        from_account_id=from_account['id'],
        to_account_id=douyin_account['id'],
        amount=355.98,
        transfer_time="2026-05-02 13:56:13",
        note="抖音月付2026年5月账单还款"
    )
    print(f"转账记录已创建，transfer_id: {transfer_id}")
else:
    print("账户未找到")
