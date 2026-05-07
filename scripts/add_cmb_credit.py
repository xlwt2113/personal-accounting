import sys
sys.path.insert(0, r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\scripts')

from database import init_database, get_or_create_account, get_accounts

# Initialize database
init_database()

# Create CMB credit card account
account_id, created = get_or_create_account(
    name='招商银行信用卡（7685）',
    account_type='credit_card',
    initial_balance=0,
    credit_limit=0  # Unknown limit from the receipt, will update later
)

print(f"Account created: {'NEW' if created else 'EXISTED'}")
print(f"Account ID: {account_id}")

# Show all accounts
accounts = get_accounts()
print(f"\nAll accounts ({len(accounts)}):")
for acc in accounts:
    print(f"  [{acc['id']}] {acc['name']} ({acc['account_type']}): balance={acc['current_balance']:.2f}")
