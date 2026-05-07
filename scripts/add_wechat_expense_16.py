# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from database import get_account_by_name, add_transaction

wechat = get_account_by_name("微信零钱")
if not wechat:
    print("错误：未找到微信零钱账户")
    exit(1)

record_id = add_transaction(
    amount=16.00,
    transaction_type="expense",
    account_id=wechat['id'],
    category="healthcare",
    transaction_date="2026-04-30",
    merchant="河南省肿瘤医院",
    note="挂号订单 就诊卡号：0006479679"
)
print(f"已添加支出记录，ID: {record_id}")