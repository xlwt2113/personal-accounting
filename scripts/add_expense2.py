# -*- coding: utf-8 -*-
import sys
import os

skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, skill_dir)
sys.stdout.reconfigure(encoding='utf-8')

from scripts.database import get_or_create_account, add_transaction

# 交易信息（从图片解析）
amount = 15.00
merchant = "微信红包"
account_name = "微信零钱"
account_type = "wechat_wallet"
category = "social"  # 人情往来
transaction_date = "2026-05-07 20:28"
note = "发给宝宝"

# 获取或创建账户
account_id, created = get_or_create_account(
    name=account_name,
    account_type=account_type,
    initial_balance=0
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
