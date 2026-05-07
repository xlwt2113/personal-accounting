import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\wt\\.openclaw\\workspace\\skills\\personal-accounting\\scripts')

from database import add_transaction, get_account_by_name

account = get_account_by_name("中信银行信用卡（7379）")
print(f"账户: {account}")

# 添加收入记录：抖音红包优惠 1.26 元
transaction_id = add_transaction(
    amount=1.26,
    transaction_type="income",
    account_id=account['id'],
    merchant="抖音支付",
    category="gift",
    transaction_date="2026-05-02 13:53:00",
    note="抖音红包优惠"
)
print(f"收入记录已创建，ID: {transaction_id}")
