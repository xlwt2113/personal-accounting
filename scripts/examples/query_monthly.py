# -*- coding: utf-8 -*-
"""
查询脚本：月度统计
"""
import sys
import os
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 切换到项目根目录运行
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.database import init_database
from scripts.statistics import get_monthly_report_text

# 初始化数据库
init_database()

now = datetime.now()
print("=" * 60)
print(f"{now.year}年{now.month}月 月度统计")
print("=" * 60)

print(get_monthly_report_text(now.year, now.month))
