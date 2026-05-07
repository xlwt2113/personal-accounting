# -*- coding: utf-8 -*-
"""
示例脚本：添加账户
"""
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 切换到项目根目录运行
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.database import init_database, add_account, get_accounts

# 初始化数据库
init_database()

# 添加一些示例账户
print("添加账户示例:")
print("-" * 40)

# 储蓄卡
acc1_id = add_account("工商银行储蓄卡", "savings_card", initial_balance=10000)
print(f"添加储蓄卡账户: 工商银行储蓄卡 (ID: {acc1_id})")

# 信用卡
acc2_id = add_account("招商银行信用卡", "credit_card", initial_balance=50000, credit_limit=50000)
print(f"添加信用卡账户: 招商银行信用卡 (ID: {acc2_id})")

# 微信零钱
acc3_id = add_account("微信零钱", "wechat_wallet", initial_balance=1000)
print(f"添加微信零钱账户: (ID: {acc3_id})")

# 支付宝
acc4_id = add_account("支付宝", "alipay", initial_balance=2000)
print(f"添加支付宝账户: (ID: {acc4_id})")

# 股票账户
acc5_id = add_account("股票账户", "stock", initial_balance=10000)
print(f"添加股票账户: (ID: {acc5_id})")

# 基金账户
acc6_id = add_account("基金账户", "fund", initial_balance=30000)
print(f"添加基金账户: (ID: {acc6_id})")

print("\n当前所有账户:")
print("-" * 40)
accounts = get_accounts()
for acc in accounts:
    print(f"  [{acc['id']}] {acc['name']} ({acc['account_type']}): ¥{acc['current_balance']:.2f}")
