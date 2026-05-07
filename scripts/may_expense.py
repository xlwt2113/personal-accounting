import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\wt\\.openclaw\\workspace\\skills\\personal-accounting\\scripts')

from database import get_total_by_type

# 5月支出
expense = get_total_by_type("expense", date_from="2026-05-01")
print(f"5月份支出总额: ¥{expense:.2f}")
