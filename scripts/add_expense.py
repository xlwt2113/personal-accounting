# -*- coding: utf-8 -*-
import sys
import os

# 添加技能目录到路径
skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, skill_dir)
sys.stdout.reconfigure(encoding='utf-8')

from scripts.database import (
    get_account_by_name,
    get_or_create_account,
    add_transaction,
    get_local_now
)

# 交易信息（从图片解析）
amount = 19.65
merchant = "全日鲜生活便利店石楠店2"
account_name = "广发银行信用卡（4150）"
account_type = "credit_card"
category = "other"  # 日常消费归类为"其他"
transaction_date = "2026-05-07 20:09"
note = "原订单金额¥19.80，优惠¥0.15"

# 获取或创建账户
account_id, created = get_or_create_account(
    name=account_name,
    account_type=account_type,
    initial_balance=0,
    credit_limit=50000  # 假设额度5万，具体以实际为准
)

if created:
    print(f"✓ 新建账户: {account_name} (ID: {account_id})")
else:
    print(f"✓ 使用已有账户: {account_name} (ID: {account_id})")

# 添加支出记录
record_id = add_transaction(
    amount=amount,
    transaction_type="expense",
    account_id=account_id,
    category=category,
    transaction_date=transaction_date,
    merchant=merchant,
    note=note
)

print(f"✓ 已记录支出: ¥{amount:.2f}")
print(f"  商家: {merchant}")
print(f"  时间: {transaction_date}")
print(f"  备注: {note}")
print(f"  记录ID: {record_id}")
