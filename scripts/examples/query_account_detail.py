# -*- coding: utf-8 -*-
"""
查询脚本：账户流水查询
"""
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 切换到项目根目录运行
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.database import init_database, get_account_by_name, get_accounts
from scripts.statistics import get_account_detail_report_text

# 初始化数据库
init_database()

# 查询指定账户
account_name = "工商银行储蓄卡"  # 可以修改为其他账户名

account = get_account_by_name(account_name)
if account:
    print("=" * 60)
    print(f"账户流水: {account_name}")
    print("=" * 60)
    print(get_account_detail_report_text(account['id']))
else:
    print(f"账户 '{account_name}' 不存在")
    print("\n当前账户列表:")
    for acc in get_accounts():
        print(f"  - {acc['name']}")
