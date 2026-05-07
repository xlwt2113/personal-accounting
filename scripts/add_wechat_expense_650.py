# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from database import get_connection, get_account_by_name, add_transaction

# 检查微信零钱账户
wechat_account = get_account_by_name("微信零钱")
if wechat_account:
    print(f"找到微信零钱账户，ID: {wechat_account['id']}")
else:
    print("未找到微信零钱账户，需要先创建")

# 添加支出记录
# 金额：6.50元
# 类型：expense（支出）
# 账户：微信零钱
# 商家：河南颐城俊达物业管理有限公司
# 商品：膳食1
# 分类：food（餐饮）
# 日期：2026-04-30

if wechat_account:
    record_id = add_transaction(
        amount=6.50,
        transaction_type="expense",
        account_id=wechat_account['id'],
        category="food",
        transaction_date="2026-04-30",
        merchant="河南颐城俊达物业管理有限公司",
        note="膳食1"
    )
    print(f"已添加支出记录，ID: {record_id}")
else:
    print("错误：无法添加记录，微信零钱账户不存在")