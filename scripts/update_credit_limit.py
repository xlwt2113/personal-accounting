import sys
sys.path.insert(0, r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\scripts')

from database import update_account, get_account_by_name

# Update credit limit
account = get_account_by_name('招商银行信用卡（7685）')
if account:
    success = update_account(account['id'], credit_limit=50000)
    print(f"Updated: {'OK' if success else 'FAILED'}")
    print(f"Account: {account['name']}")
    print(f"Credit limit: 50000.00")
else:
    print("Account not found")
