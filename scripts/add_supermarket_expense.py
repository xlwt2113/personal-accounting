import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\wt\\.openclaw\\workspace\\skills\\personal-accounting\\scripts')

from database import add_transaction, get_account_by_name

account = get_account_by_name("广发银行信用卡（4150）")
print(f"账户: {account}")

# 添加支出记录：超市消费 10.57 元
transaction_id = add_transaction(
    amount=10.57,
    transaction_type="expense",
    account_id=account['id'],
    merchant="郑州市佰佳鲜超市有限公司",
    category="shopping",
    transaction_date="2026-05-02 19:13:00",
    note="碰一下立减0.23"
)
print(f"支出记录已创建，ID: {transaction_id}")
