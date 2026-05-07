import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\wt\\.openclaw\\workspace\\skills\\personal-accounting\\scripts')

from database import add_transaction, get_account_by_name, get_or_create_account

# 查找余额宝账户（支付宝）
account = get_account_by_name("余额宝")
if not account:
    print("创建支付宝账户...")
    account_id = get_or_create_account("支付宝", "alipay", initial_balance=0)
    account = get_account_by_name("支付宝")
print(f"账户: {account}")

# 添加支出记录：理发店消费 10.00 元
transaction_id = add_transaction(
    amount=10.00,
    transaction_type="expense",
    account_id=account['id'],
    merchant="理发店",
    category="other",
    transaction_date="2026-05-02 18:48:09",
    note="美容美发-扫码付款"
)
print(f"支出记录已创建，ID: {transaction_id}")
