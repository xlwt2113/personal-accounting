import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\wt\\.openclaw\\workspace\\skills\\personal-accounting\\scripts')

from database import add_transfer, get_account_by_name

from_account = get_account_by_name("余额宝")
to_account = get_account_by_name("平安银行信用卡（3907）")

print(f"转出账户: {from_account}")
print(f"转入账户: {to_account}")

if from_account and to_account:
    transfer_id = add_transfer(
        from_account_id=from_account['id'],
        to_account_id=to_account['id'],
        amount=634.67,
        transfer_time="2026-05-02 19:58:11",
        note="信用卡还款"
    )
    print(f"转账记录已创建，transfer_id: {transfer_id}")
else:
    print("账户未找到")
