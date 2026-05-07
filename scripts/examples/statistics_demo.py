# -*- coding: utf-8 -*-
"""
示例脚本：统计报表
"""
import sys
import os
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 切换到项目根目录运行
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.database import init_database
from scripts.statistics import (
    get_assets_report_text,
    get_account_balance_report_text,
    get_account_detail_report_text,
    get_monthly_report_text,
    get_category_report_text
)

# 初始化数据库
init_database()

print("=" * 60)
print("个人记账统计报表")
print("=" * 60)

# 资产汇总
print("\n【资产汇总】")
print("-" * 50)
print(get_assets_report_text())

# 账户余额
print("\n【账户余额】")
print("-" * 50)
print(get_account_balance_report_text())

# 本月统计
print("\n【本月统计】")
print("-" * 50)
print(get_monthly_report_text())

# 支出分类
print("\n【支出分类】")
print("-" * 50)
print(get_category_report_text('expense'))

# 收入分类
print("\n【收入分类】")
print("-" * 50)
print(get_category_report_text('income'))

# 账户详情示例
print("\n【账户详情示例 - 工商银行储蓄卡】")
print("-" * 50)
from scripts.database import get_account_by_name
icbc = get_account_by_name("工商银行储蓄卡")
if icbc:
    print(get_account_detail_report_text(icbc['id']))
else:
    print("账户不存在")
