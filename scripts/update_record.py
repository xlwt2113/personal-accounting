import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
import os

# 添加父目录到路径以导入database模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.database import update_transaction

result = update_transaction(19, category='food', note='洛馍')
print(f"✅ 更新结果：{result}")
print("已更新记录19：分类→餐饮，备注→洛馍")
