# -*- coding: utf-8 -*-
"""
查询脚本：转账记录查询
"""
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 切换到项目根目录运行
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.database import init_database, get_transfers
from scripts.statistics import format_transfers_report

# 初始化数据库
init_database()

print("=" * 60)
print("转账记录查询")
print("=" * 60)

transfers = get_transfers(limit=50)
if transfers:
    print(format_transfers_report(transfers))
else:
    print("暂无转账记录")
