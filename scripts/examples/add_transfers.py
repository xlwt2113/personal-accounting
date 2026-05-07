# -*- coding: utf-8 -*-
"""
示例脚本：转账记录
"""
import sys
import os
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 切换到项目根目录运行
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.database import (
    init_database, add_transfer, get_account_by_name, get_transfers
)
from scripts.statistics import format_transfers_report, get_account_balance_report_text

# 初始化数据库
init_database()

print("转账记录示例:")
print("=" * 50)

icbc = get_account_by_name("工商银行储蓄卡")
alipay = get_account_by_name("支付宝")
wechat = get_account_by_name("微信零钱")
cmbc = get_account_by_name("招商银行信用卡")

# 从银行卡转钱到支付宝
if icbc and alipay:
    transfer_id, from_tid, to_tid = add_transfer(
        from_account_id=icbc['id'],
        to_account_id=alipay['id'],
        amount=5000,
        transfer_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        note='转账到支付宝'
    )
    print(f"转账记录: 工商银行 -> 支付宝 ¥5000 (Transfer ID: {transfer_id})")
    print(f"  生成支出记录 ID: {from_tid}")
    print(f"  生成收入记录 ID: {to_tid}")

# 从银行卡转钱到微信
if icbc and wechat:
    transfer_id, from_tid, to_tid = add_transfer(
        from_account_id=icbc['id'],
        to_account_id=wechat['id'],
        amount=2000,
        transfer_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        note='转账到微信'
    )
    print(f"转账记录: 工商银行 -> 微信 ¥2000 (Transfer ID: {transfer_id})")

# 信用卡还款（从储蓄卡转到信用卡）
if icbc and cmbc:
    transfer_id, from_tid, to_tid = add_transfer(
        from_account_id=icbc['id'],
        to_account_id=cmbc['id'],
        amount=3000,
        transfer_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        note='还信用卡'
    )
    print(f"还款记录: 工商银行 -> 招商信用卡 ¥3000 (Transfer ID: {transfer_id})")

# 查看所有转账记录
print("\n转账记录列表:")
print("-" * 50)
transfers = get_transfers(limit=10)
print(format_transfers_report(transfers))

print("\n账户余额:")
print("-" * 50)
print(get_account_balance_report_text())
