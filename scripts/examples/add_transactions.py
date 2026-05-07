# -*- coding: utf-8 -*-
"""
示例脚本：添加收支记录
"""
import sys
import os
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 切换到项目根目录运行
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.database import (
    init_database, add_transaction, get_account_by_name, get_accounts
)
from scripts.statistics import format_transactions_report, get_account_balance_report_text

# 初始化数据库
init_database()

print("添加收支记录示例:")
print("=" * 50)

# 记录支出
wechat = get_account_by_name("微信零钱")
if wechat:
    # 在麦当劳消费
    tid1 = add_transaction(
        amount=45.50,
        transaction_type='expense',
        account_id=wechat['id'],
        category='food',
        transaction_date=datetime.now().strftime('%Y-%m-%d'),
        merchant='麦当劳',
        note='午餐'
    )
    print(f"添加支出记录: ¥45.50 麦当劳 (ID: {tid1})")
    
    # 打车
    tid2 = add_transaction(
        amount=28.00,
        transaction_type='expense',
        account_id=wechat['id'],
        category='transportation',
        transaction_date=datetime.now().strftime('%Y-%m-%d'),
        merchant='滴滴出行',
        note='上班打车'
    )
    print(f"添加支出记录: ¥28.00 滴滴出行 (ID: {tid2})")

# 支付宝消费
alipay = get_account_by_name("支付宝")
if alipay:
    # 网上购物
    tid3 = add_transaction(
        amount=199.00,
        transaction_type='expense',
        account_id=alipay['id'],
        category='shopping',
        transaction_date=datetime.now().strftime('%Y-%m-%d'),
        merchant='淘宝',
        note='买书'
    )
    print(f"添加支出记录: ¥199.00 淘宝 (ID: {tid3})")

# 记录收入
icbc = get_account_by_name("工商银行储蓄卡")
if icbc:
    # 工资收入
    tid4 = add_transaction(
        amount=15000.00,
        transaction_type='income',
        account_id=icbc['id'],
        category='salary',
        transaction_date=datetime.now().strftime('%Y-%m-%d'),
        merchant='公司',
        note='本月工资'
    )
    print(f"添加收入记录: ¥15000.00 工资 (ID: {tid4})")

# 信用卡消费
cmbc = get_account_by_name("招商银行信用卡")
if cmbc:
    # 餐厅聚餐
    tid5 = add_transaction(
        amount=380.00,
        transaction_type='expense',
        account_id=cmbc['id'],
        category='food',
        transaction_date=datetime.now().strftime('%Y-%m-%d'),
        merchant='西餐厅',
        note='团队聚餐'
    )
    print(f"添加支出记录: ¥380.00 信用卡消费 (ID: {tid5})")

print("\n账户余额:")
print("-" * 50)
print(get_account_balance_report_text())
