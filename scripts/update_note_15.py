# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("UPDATE transactions SET note = '哇哈哈矿泉水一瓶' WHERE id = 15")
conn.commit()

cursor.execute("SELECT id, amount, category, merchant, note FROM transactions WHERE id = 15")
row = cursor.fetchone()
conn.close()

print(f"已更新备注：ID={row[0]}, 金额={row[1]}, 分类={row[2]}, 商家={row[3]}, 备注={row[4]}")