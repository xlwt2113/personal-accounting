# -*- coding: utf-8 -*-
import sys
import os

skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, skill_dir)
sys.stdout.reconfigure(encoding='utf-8')

from scripts.database import update_transaction

# 更新记录ID 63的分类为购物
result = update_transaction(63, category='shopping')

if result:
    print("✓ 已更新分类为：购物 (shopping)")
else:
    print("✗ 更新失败")
