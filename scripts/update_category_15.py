# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from database import get_connection

conn = get_connection()
cursor = conn.cursor()

# 更新ID=15的记录，分类从other改为food
cursor.execute("UPDATE transactions SET category = 'food' WHERE id = 15")
conn.commit()

# 验证更新
cursor.execute("SELECT id, amount, category, merchant, note FROM transactions WHERE id = 15")
row = cursor.fetchone()
conn.close()

if row:
    print(f"已更新记录：")
    print(f"  ID: {row[0]}, 金额: {row[1]}, 分类: {row[2]}, 商家: {row[3]}, 备注: {row[4]}")
else:
    print("未找到该记录")