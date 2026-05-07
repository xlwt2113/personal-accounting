# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from database import get_account_by_name, add_transaction

# 获取微信零钱账户
wechat_account = get_account_by_name("微信零钱")
if not wechat_account:
    print("错误：未找到微信零钱账户")
    exit(1)

print(f"找到微信零钱账户，ID: {wechat_account['id']}")

# 添加支出记录
record_id = add_transaction(
    amount=3.00,
    transaction_type="expense",
    account_id=wechat_account['id'],
    category="food",
    transaction_date="2026-04-30",
    merchant="营养餐厅",
    note="餐车1"
)
print(f"已添加支出记录，ID: {record_id}")