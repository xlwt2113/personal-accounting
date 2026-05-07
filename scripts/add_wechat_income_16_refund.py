# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from database import get_account_by_name, add_transaction

wechat = get_account_by_name("微信零钱")
if not wechat:
    print("错误：未找到微信零钱账户")
    exit(1)

# 退款视为收入
record_id = add_transaction(
    amount=16.00,
    transaction_type="income",
    account_id=wechat['id'],
    category="refund",
    transaction_date="2026-04-30",
    merchant="河南省肿瘤医院",
    note="退款"
)
print(f"已添加收入记录，ID: {record_id}")