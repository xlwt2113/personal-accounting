# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from database import get_transactions

# 查询最近添加的记录
transactions = get_transactions(account_id=7, limit=5)
print("微信零钱最近的5条记录：")
for t in transactions:
    print(f"  ID: {t['id']}, 金额: {t['amount']}, 类型: {t['transaction_type']}, 商家: {t['merchant']}, 分类: {t['category']}, 日期: {t['transaction_date']}, 备注: {t['note']}")