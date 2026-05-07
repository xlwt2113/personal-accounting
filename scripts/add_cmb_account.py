import sys
sys.path.insert(0, r'C:\Users\wt\.openclaw\workspace\skills\personal-accounting\scripts')

from database import init_database, get_or_create_account, get_accounts

# Initialize database
init_database()
print("Database initialized")

# Create CMB savings card account
account_id, created = get_or_create_account(
    name='招商银行储蓄卡（5063）',
    account_type='savings_card',
    initial_balance=92902.23
)

print(f"\nAccount created: {'NEW' if created else 'EXISTED'}")
print(f"Account ID: {account_id}")

# Show all accounts
accounts = get_accounts()
print(f"\nAll accounts ({len(accounts)}):")
for acc in accounts:
    balance = acc['current_balance']
    print(f"  [{acc['id']}] {acc['name']}: {balance:.2f}")
