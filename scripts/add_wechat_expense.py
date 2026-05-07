import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\wt\\.openclaw\\workspace\\skills\\personal-accounting\\scripts')

from database import add_transaction, get_account_by_name

account = get_account_by_name("微信零钱")
print(f"账户: {account}")

# 添加支出记录：扫码付款 7.00 元
transaction_id = add_transaction(
    amount=7.00,
    transaction_type="expense",
    account_id=account['id'],
    merchant="晴空万里",
    category="food",
    transaction_date="2026-05-02 17:43:46",
    note="扫码付款"
)
print(f"支出记录已创建，ID: {transaction_id}")
