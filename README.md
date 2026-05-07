# Personal Accounting - 个人记账助手

智能个人记账系统，支持账单图片解析、手动录入、账户管理、转账记录和统计分析。

## 📁 文件结构

```
personal-accounting/
├── db/
│   └── accounting.db          # SQLite 数据库
├── scripts/
│   ├── __init__.py            # 包初始化
│   ├── database.py            # 核心数据库操作模块
│   ├── parser.py               # 账单图片解析模块
│   ├── daily_report.py         # 日报统计
│   ├── daily_summary.py        # 日汇总
│   ├── financial_summary.py    # 财务汇总
│   ├── statistics.py           # 统计分析
│   └── examples/               # 示例脚本
│       ├── add_accounts.py
│       ├── add_transactions.py
│       ├── add_transfers.py
│       ├── query_*.py
│       └── statistics_demo.py
├── README.md                   # 本文件
└── SKILL.md                    # 详细技能文档
```

---

## 🚀 快速开始

### 数据库路径

```python
# Windows
db_path = r"C:\Users\wt\.openclaw\workspace\skills\personal-accounting\db\accounting.db"

# macOS/Linux
db_path = "/Users/wt/.openclaw/plugin-skills/personal-accounting/db/accounting.db"
```

### 编码处理（Windows）

```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

---

## 📚 核心 API 参考

### 1. 账户操作

| 函数 | 说明 | 返回值 |
|------|------|--------|
| `add_account(name, type, initial_balance, credit_limit)` | 添加账户 | account_id |
| `get_accounts()` | 获取所有账户 | List[Dict] |
| `get_account_by_id(id)` | 根据ID获取账户 | Dict |
| `get_account_by_name(name)` | 根据名称获取账户 | Dict |
| `update_account(id, ...)` | 更新账户信息 | bool |
| `delete_account(id)` | 删除账户 | bool |
| `calculate_account_balance(id)` | 计算账户余额 | float |

### 2. 收支记录

| 函数 | 说明 | 返回值 |
|------|------|--------|
| `add_transaction(amount, type, account_id, category, date, ...)` | 添加记录 | transaction_id |
| `get_transactions(account_id, type, date_from, date_to, ...)` | 查询记录 | List[Dict] |
| `get_transaction_by_id(id)` | 获取单条记录 | Dict |
| `update_transaction(id, ...)` | 更新记录 | bool |
| `delete_transaction(id)` | 删除记录 | bool |
| `get_account_transactions_with_transfers(id, ...)` | 获取账户流水(含转账) | List[Dict] |

### 3. 转账操作

| 函数 | 说明 | 返回值 |
|------|------|--------|
| `add_transfer(from_id, to_id, amount, time, note)` | 添加转账 | (transfer_id, from_tx_id, to_tx_id) |
| `get_transfers(date_from, date_to, account_id)` | 查询转账记录 | List[Dict] |
| `delete_transfer(id)` | 删除转账及关联记录 | bool |

### 4. 统计分析

| 函数 | 说明 | 返回值 |
|------|------|--------|
| `get_financial_summary()` | 完整财务汇总 | Dict |
| `get_total_by_type(type, date_from, date_to, account_id)` | 收支总额 | float |
| `get_total_by_category(type, date_from, date_to, account_id)` | 按分类统计 | List[Dict] |
| `get_total_by_merchant(type, date_from, date_to, account_id)` | 按商家统计 | List[Dict] |
| `get_total_by_account(type, date_from, date_to)` | 按账户统计 | List[Dict] |
| `get_daily_summary(date_from, date_to)` | 每日汇总 | List[Dict] |
| `get_monthly_summary(year, month)` | 月度汇总 | List[Dict] |

### 5. 辅助函数

| 函数 | 说明 |
|------|------|
| `format_bank_account_name(bank, card_last_four, type)` | 格式化银行卡名称 |
| `get_or_create_account(name, type, ...)` | 获取或创建账户 |
| `get_or_create_account_from_parser(info)` | 解析后自动创建账户 |
| `init_database()` | 初始化数据库表 |
| `get_local_now()` | 获取当前时间(东八区) |

---

## 🗄️ 数据库结构

### accounts 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| name | TEXT | 账户名称（唯一） |
| account_type | TEXT | 类型：savings_card/credit_card/wechat_wallet/alipay/stock/fund/cash/other |
| initial_balance | REAL | 初始余额（资产为正，信用卡为负） |
| credit_limit | REAL | 信用卡额度 |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

### transactions 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| amount | REAL | 金额（正数） |
| transaction_type | TEXT | income/expense |
| account_id | INTEGER | 账户ID |
| merchant | TEXT | 商家 |
| category | TEXT | 分类 |
| transaction_date | TEXT | 交易时间 |
| note | TEXT | 备注 |
| transfer_id | INTEGER | 关联转账ID |
| created_at | TEXT | 创建时间 |

### transfers 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| from_account_id | INTEGER | 转出账户 |
| to_account_id | INTEGER | 转入账户 |
| amount | REAL | 金额 |
| transfer_time | TEXT | 转账时间 |
| note | TEXT | 备注 |
| created_at | TEXT | 创建时间 |

---

## 💡 使用示例

### 添加账户

```python
from scripts.database import add_account

# 储蓄卡
acc_id = add_account("招商银行储蓄卡(1011)", "savings_card", 10000.0)

# 信用卡（额度5万）
acc_id = add_account("招商银行信用卡(3457)", "credit_card", 0, 50000.0)
```

### 记录收支

```python
from scripts.database import add_transaction, get_account_by_name

# 获取账户ID
acc = get_account_by_name("微信零钱")
account_id = acc['id']

# 记录支出
add_transaction(
    amount=45.00,
    transaction_type='expense',
    account_id=account_id,
    merchant='麦当劳',
    category='food',
    transaction_date='2024-01-15 12:30'
)
```

### 转账

```python
from scripts.database import add_transfer, get_account_by_name

from_acc = get_account_by_name("招商银行储蓄卡(1011)")['id']
to_acc = get_account_by_name("支付宝")['id']

transfer_id, _, _ = add_transfer(
    from_account_id=from_acc,
    to_account_id=to_acc,
    amount=5000.00,
    note='转账'
)
```

### 财务汇总

```python
from scripts.database import get_financial_summary

summary = get_financial_summary()

print(f"净资产: ¥{summary['net_worth']:,.2f}")
print(f"总资产: ¥{summary['total_assets']:,.2f}")
print(f"总负债: ¥{summary['total_debt']:,.2f}")
print(f"本月收入: ¥{summary['current_month']['income']:,.2f}")
print(f"本月支出: ¥{summary['current_month']['expense']:,.2f}")
```

---

## ⚠️ 使用规范

1. **禁止直接 SQL**：所有数据库操作必须通过 `database.py` 中的函数
2. **图片直接入库**：收到账单图片 → AI解析 → **直接保存**，不询问确认
3. **账户名称唯一**：同一数据库中账户名称不可重复
4. **信用卡欠款独立显示**：财务汇总中信用卡与资产账户分开

---

## 📖 详细文档

更多详细内容请参阅 [SKILL.md](./SKILL.md)
