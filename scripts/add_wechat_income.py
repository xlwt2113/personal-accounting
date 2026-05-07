import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\wt\\.openclaw\\workspace\\skills\\personal-accounting\\scripts')

from database import add_transaction, get_account_by_name

account = get_account_by_name("微信零钱")
print(f"账户: {account}")

# 添加收入记录：微信红包 0.01 元
transaction_id = add_transaction(
    amount=0.01,
    transaction_type="income",
    account_id=account['id'],
    merchant="微信红包",
    category="gift",
    transaction_date="2026-05-02 19:18:00",
    note="收到红包"
)
print(f"收入记录已创建，ID: {transaction_id}")
