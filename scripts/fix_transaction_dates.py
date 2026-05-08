# -*- coding: utf-8 -*-
"""
修复 transactions 表中 transaction_date 格式不完整的记录
格式要求: YYYY-MM-DD HH:MM:SS
"""
import sqlite3
import re

db_path = "/Users/wt/.openclaw/plugin-skills/personal-accounting/db/accounting.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查询所有 transaction_date 格式不完整的记录
cursor.execute("""
    SELECT id, transaction_date, created_at 
    FROM transactions 
    WHERE transaction_date NOT GLOB '????-??-?? ??:??:??'
""")
records = cursor.fetchall()

print(f"发现 {len(records)} 条格式不正确的记录")

fixed_count = 0
for row in records:
    record_id, transaction_date, created_at = row
    
    # 解析 created_at 获取时间部分
    # 格式: 2026-05-01 14:51:11
    match = re.match(r'^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}):(\d{2})$', created_at)
    if not match:
        print(f"警告: 无法解析 created_at '{created_at}' for id={record_id}")
        continue
    
    date_part = match.group(1)  # 2026-05-01
    hour_minute = match.group(2)  # 14:51
    seconds = match.group(3)  # 11
    
    # 处理 transaction_date 的不同格式
    new_transaction_date = None
    
    if re.match(r'^\d{4}-\d{2}-\d{2}$', transaction_date):
        # 只有日期: 2026-04-30 -> 2026-04-30 14:51:11
        new_transaction_date = f"{date_part} {hour_minute}:{seconds}"
    elif re.match(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}$', transaction_date):
        # 有日期和时间(缺秒): 2026-05-04 11:43 -> 2026-05-04 11:43:11
        new_transaction_date = f"{transaction_date}:{seconds}"
    else:
        print(f"未知格式: transaction_date='{transaction_date}', created_at='{created_at}'")
        continue
    
    # 更新数据库
    cursor.execute(
        "UPDATE transactions SET transaction_date = ? WHERE id = ?",
        (new_transaction_date, record_id)
    )
    fixed_count += 1
    print(f"ID {record_id}: '{transaction_date}' -> '{new_transaction_date}'")

conn.commit()

# 验证修复结果
cursor.execute("""
    SELECT COUNT(*) FROM transactions 
    WHERE transaction_date NOT GLOB '????-??-?? ??:??:??'
""")
remaining = cursor.fetchone()[0]

print(f"\n修复完成: {fixed_count} 条")
print(f"剩余格式不正确的记录: {remaining} 条")

conn.close()
