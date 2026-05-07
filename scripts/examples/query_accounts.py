# -*- coding: utf-8 -*-
"""
查询脚本：查看所有账户余额
"""
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 切换到项目根目录运行
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.database import init_database, get_accounts
from scripts.statistics import get_assets_report_text, get_account_balance_report_text

# 初始化数据库
init_database()

print("=" * 60)
print("账户余额查询")
print("=" * 60)

print("\n资产汇总:")
print(get_assets_report_text())

print("\n账户明细:")
print(get_account_balance_report_text())
