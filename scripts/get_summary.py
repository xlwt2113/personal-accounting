# -*- coding: utf-8 -*-
import sys
import os

skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, skill_dir)
sys.stdout.reconfigure(encoding='utf-8')

from scripts.database import get_financial_summary

summary = get_financial_summary()

print("=" * 40)
print("              财 务 汇 总")
print("=" * 40)

print("\n📊 净资产")
print(f"  总资产:  ¥{summary['total_assets']:,.2f}")
print(f"  总负债:  ¥{summary['total_debt']:,.2f}")
print(f"  净资产:  ¥{summary['net_worth']:,.2f}")

print("\n💰 收支概况")
print(f"  本月收入:  ¥{summary['current_month']['income']:,.2f}")
print(f"  本月支出:  ¥{summary['current_month']['expense']:,.2f}")
print(f"  本月净值:  ¥{summary['current_month']['net']:,.2f}")
print(f"  上月收入:  ¥{summary['last_month']['income']:,.2f}")
print(f"  上月支出:  ¥{summary['last_month']['expense']:,.2f}")
print(f"  上月净值:  ¥{summary['last_month']['net']:,.2f}")

print("\n🏦 资产账户")
for acc in summary['asset_accounts']:
    print(f"  {acc['name']}: ¥{acc['balance']:,.2f}")

print("\n💳 信用卡欠款")
for acc in summary['credit_accounts']:
    print(f"  {acc['name']}: 欠款 ¥{acc['balance']:,.2f} | 额度 ¥{acc['credit_limit']:,.2f} | 可用 ¥{acc['available']:,.2f}")

if summary['expense_by_category']:
    print("\n📂 本月支出分类")
    for cat in summary['expense_by_category']:
        print(f"  {cat['category']}: ¥{cat['total']:,.2f}")

print("\n" + "=" * 40)
