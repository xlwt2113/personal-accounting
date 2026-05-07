import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.database import update_transaction

# 更新记录14和16，分类从gift改为social
result1 = update_transaction(14, category='social')
result2 = update_transaction(16, category='social')

print(f"记录14更新结果：{result1}")
print(f"记录16更新结果：{result2}")
print("已将微信红包支出分类从gift改为social（人情往来）")
