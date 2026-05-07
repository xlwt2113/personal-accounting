import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\wt\\.openclaw\\workspace\\skills\\personal-accounting\\scripts')

from database import delete_transfer, add_transaction, get_account_by_name

# 删除刚才错误的转账记录
transfer_id = 4
print(f"删除转账记录 ID: {transfer_id}")
result = delete_transfer(transfer_id)
print(f"删除结果: {result}")

# 查找账户
from_account = get_account_by_name("招商银行储蓄卡（5063）")
print(f"账户: {from_account}")

# 记录为消费支出：汽车加油
transaction_id = add_transaction(
    amount=355.98,
    transaction_type="expense",
    account_id=from_account['id'],
    merchant="加油站",
    category="transportation",
    transaction_date="2026-05-02 13:56:13",
    note="汽车加油-抖音月付支付"
)
print(f"消费记录已创建，ID: {transaction_id}")
