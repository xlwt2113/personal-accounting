import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\wt\\.openclaw\\workspace\\skills\\personal-accounting\\scripts')

from database import update_account, get_account_by_name

account = get_account_by_name("中原银行信用卡（8599）")
print(f"当前账户: {account}")

# 初始欠款 = 20000 - 19950.01 = 49.99
# 因为已经记录了17.31的还款，所以 initial_balance 应该是 -(49.99 - 17.31) = -32.68
# 不对，让我重新理解：
# 用户说"没有还17块3毛1的情况下剩余额度为19,950.01"
# 这意味着在17.31还款之前，欠款是 49.99
# 还款17.31后，欠款应该是 49.99 - 17.31 = 32.68

# 但系统中 current_balance = -17.31 (这是17.31收入的结果)
# 所以 initial_balance 应该 = -17.31 - 17.31 = -34.68... 不对

# 重新想：
# current_balance = initial_balance + income - expense
# -17.31 = initial_balance + 17.31 - 0
# initial_balance = -34.62... 不对

# 等等，让我换个方式理解：
# 用户说额度2万，剩余19950.01是在没还17.31的时候
# 所以在那之前：额度2万，可用19950.01，欠款 = 20000 - 19950.01 = 49.99
# 然后还了17.31，现在欠款 = 49.99 - 17.31 = 32.68
# 但系统中只记录了一笔17.31的收入...
# 如果 initial_balance = -32.68，那么 current_balance = -32.68 + 17.31 = -15.37... 还是不对

# 最简单的理解：用户的可用额度19950.01是当前实际状态
# 欠款 = 20000 - 19950.01 = 49.99 (这是当前欠款)
# 但系统中 current_balance = -17.31

# 差额：49.99 - 17.31 = 32.68... 这应该就是 initial_balance

# 所以：initial_balance 应该是 -32.68
new_initial_balance = -32.68
result = update_account(account['id'], initial_balance=new_initial_balance)
print(f"更新结果: {result}")

account = get_account_by_name("中原银行信用卡（8599）")
print(f"更新后账户: {account}")
print(f"欠款: ¥{abs(account['current_balance']):.2f}")
