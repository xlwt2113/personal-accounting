# Personal Accounting - 个人记账助手

智能个人记账系统，支持账单截图自动识别、文字/语音手动录入、多账户管理、转账记录和财务统计分析。

## 功能概览

| 功能 | 说明 |
|------|------|
| 图片解析账单 | 上传微信/支付宝/拼多多账单截图，AI 自动识别金额、商户、分类、支付时间、订单号，直接入库 |
| 手动录入 | 文字或语音描述消费/收入，自动记录到对应账户 |
| 多账户管理 | 支持储蓄卡、信用卡、微信零钱、支付宝、股票、基金、现金等账户类型 |
| 转账记录 | 账户间转账，自动生成关联的收支记录 |
| 财务汇总 | 净资产、总资产/总负债、本月收支对比、各账户余额、支出分类占比 |
| 日报/周报/月报/年报 | 按时间段统计收支，按账户和分类分组汇总 |
| 分类统计 | 按消费分类（餐饮/交通/购物等）统计支出和收入 |
| 商家统计 | 按商家统计消费金额和笔数 |
| 去重保护 | 基于订单号/交易单号/转账单号自动检测重复记录，防止重复录入 |

## 文件结构

```
personal-accounting/
├── db/
│   └── accounting.db           # SQLite 数据库
├── scripts/
│   ├── __init__.py             # 包初始化
│   ├── database.py             # 核心数据库操作模块
│   ├── parser.py               # 账单图片解析模块
│   ├── statistics.py           # 统计报表与格式化模块
│   ├── cli.py                  # 统一命令行入口
│   └── examples/               # 示例脚本（演示用途）
├── README.md                   # 本文件
└── SKILL.md                    # 技能详细文档（面向 AI Agent）
```

## 快速开始

### 数据库

数据库路径由 `database.py` 自动计算，位于 `db/accounting.db`，无需手动指定：

```python
from scripts.database import DB_PATH
print(DB_PATH)  # 自动定位到 personal-accounting/db/accounting.db
```

### 命令行操作

所有操作统一通过 `scripts/cli.py` 执行：

```bash
# 切换到脚本目录
cd personal-accounting/scripts

# 查询类
python cli.py summary                  # 财务汇总
python cli.py accounts                 # 账户列表
python cli.py report daily             # 日报
python cli.py report weekly            # 周报
python cli.py report monthly           # 月报
python cli.py report yearly            # 年报
python cli.py categories expense       # 支出分类统计
python cli.py categories income        # 收入分类统计
python cli.py transactions             # 交易记录列表
python cli.py transfers                # 转账记录列表
python cli.py account-detail <账户ID>  # 账户流水

# 写入类（通过 JSON 文件传参）
python cli.py add-account --file _data.json
python cli.py add-transaction --file _data.json
python cli.py add-transfer --file _data.json
python cli.py update-transaction <ID> --file _data.json
python cli.py delete-transaction <ID>
```

## 核心 API 参考

### 1. 账户操作

| 函数 | 说明 | 返回值 |
|------|------|--------|
| `add_account(name, type, initial_balance, credit_limit)` | 添加账户 | account_id |
| `get_accounts()` | 获取所有账户 | List[Dict] |
| `get_account_by_name(name)` | 按名称查找账户 | Dict |
| `get_account_by_id(id)` | 按 ID 查找账户 | Dict |
| `update_account(id, ...)` | 更新账户信息 | bool |
| `delete_account(id)` | 删除账户 | bool |
| `calculate_account_balance(id)` | 计算账户余额 | float |

### 2. 收支记录

| 函数 | 说明 | 返回值 |
|------|------|--------|
| `add_transaction(amount, transaction_type, account_id, category, transaction_date, ...)` | 添加交易记录（含 order_no 去重） | transaction_id |
| `get_transactions(account_id, type, date_from, date_to, ...)` | 查询交易记录 | List[Dict] |
| `get_transaction_by_id(id)` | 获取单条记录 | Dict |
| `update_transaction(id, ...)` | 更新记录 | bool |
| `delete_transaction(id)` | 删除记录 | bool |

### 3. 转账操作

| 函数 | 说明 | 返回值 |
|------|------|--------|
| `add_transfer(from_id, to_id, amount, transfer_time, note)` | 添加转账（自动生成两条关联收支记录） | (transfer_id, from_tx_id, to_tx_id) |
| `get_transfers(date_from, date_to, account_id)` | 查询转账记录 | List[Dict] |
| `delete_transfer(id)` | 删除转账及关联记录 | bool |

### 4. 统计分析

| 函数 | 说明 | 返回值 |
|------|------|--------|
| `get_financial_summary()` | 完整财务汇总 | Dict |
| `get_daily_report()` | 日报数据 | Dict |
| `get_weekly_report()` | 周报数据 | Dict |
| `get_monthly_detailed_report()` | 月报数据 | Dict |
| `get_yearly_report()` | 年报数据 | Dict |
| `get_total_by_category(type, date_from, date_to)` | 按分类统计 | List[Dict] |
| `get_total_by_merchant(type, date_from, date_to)` | 按商家统计 | List[Dict] |
| `get_total_by_account(type, date_from, date_to)` | 按账户统计 | List[Dict] |
| `get_daily_summary(date_from, date_to)` | 每日汇总 | List[Dict] |

### 5. 统计格式化（statistics.py）

| 函数 | 说明 |
|------|------|
| `format_assets_report(data)` | 格式化财务汇总报表 |
| `format_monthly_report(data)` | 格式化月度报表 |
| `format_category_report(data)` | 格式化分类统计报表 |
| `format_detailed_report_text(data)` | 格式化详细报表 |
| `get_assets_report_text()` | 获取财务汇总文本 |
| `get_category_report_text(type)` | 获取分类统计文本 |
| `get_daily_report_text()` | 获取日报文本 |
| `get_weekly_report_text()` | 获取周报文本 |
| `get_monthly_detailed_report_text()` | 获取月报文本 |
| `get_yearly_report_text()` | 获取年报文本 |

## 数据库结构

### accounts 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| name | TEXT NOT NULL UNIQUE | 账户名称 |
| account_type | TEXT | savings_card / credit_card / wechat_wallet / alipay / stock / fund / cash / other |
| initial_balance | REAL | 初始余额（资产为正，信用卡为负） |
| credit_limit | REAL | 信用卡额度（仅信用卡有效） |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

### transactions 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| amount | REAL | 金额（正数） |
| transaction_type | TEXT | income / expense |
| account_id | INTEGER | 账户 ID |
| merchant | TEXT | 商家名称 |
| category | TEXT | 分类（英文值，如 food / shopping / healthcare） |
| transaction_date | TEXT | 交易时间（YYYY-MM-DD HH:MM:SS） |
| note | TEXT | 备注 |
| order_no | TEXT | 订单号/交易单号/转账单号（唯一标识，去重用） |
| transfer_id | INTEGER | 关联转账 ID |
| created_at | TEXT | 创建时间 |

### transfers 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| from_account_id | INTEGER | 转出账户 |
| to_account_id | INTEGER | 转入账户 |
| amount | REAL | 转账金额 |
| transfer_time | TEXT | 转账时间 |
| note | TEXT | 备注 |
| created_at | TEXT | 创建时间 |

## 消费分类

### 支出分类

| 分类值 | 中文名称 | 说明 |
|--------|----------|------|
| food | 餐饮 | 吃饭、外卖、饮品等 |
| transportation | 交通 | 打车、地铁、加油等 |
| shopping | 购物 | 网购、超市、便利店等 |
| entertainment | 娱乐 | 电影、游戏、旅游、健身等 |
| bills | 账单 | 水电费、话费、物业费等 |
| healthcare | 医疗 | 医院、药店、体检等 |
| social | 人情往来 | 红包、份子钱、送礼、聚会等 |
| education | 教育 | 培训、学费、书籍等 |
| housing | 住房 | 装修、家具、家纺等 |
| investment | 投资理财 | 基金、股票等投资支出 |
| other | 其他 | 未分类支出 |

### 收入分类

| 分类值 | 中文名称 | 说明 |
|--------|----------|------|
| salary | 工资 | 月薪、底薪等 |
| bonus | 奖金 | 年终奖、绩效、分红等 |
| investment | 投资收益 | 理财收益、利息、股息等 |
| gift | 礼金红包 | 红包、礼金、压岁钱等 |
| refund | 退款 | 退货退款、返现等 |
| other | 其他收入 | 未分类收入 |

## 使用示例

### 添加账户

```python
from scripts.database import add_account

# 储蓄卡（初始余额 10000）
add_account("招商银行储蓄卡（1011）", "savings_card", 10000.0)

# 信用卡（额度 50000）
add_account("招商银行信用卡（3457）", "credit_card", 0, 50000.0)

# 微信零钱
add_account("微信零钱", "wechat_wallet", 1430.67)

# 支付宝
add_account("支付宝", "alipay", 2000.0)
```

### 记录收支

```python
from scripts.database import add_transaction, get_account_by_name

account = get_account_by_name("微信零钱")

# 记录支出（图片识别时 order_no 为真实的交易单号）
add_transaction(
    amount=45.00,
    transaction_type='expense',
    account_id=account['id'],
    merchant='麦当劳',
    category='food',
    transaction_date='2026-05-29 12:30:00',
    order_no='20260529123000'  # 文字录入时用时间戳
)
```

### 转账

```python
from scripts.database import add_transfer, get_account_by_name

from_acc = get_account_by_name("招商银行储蓄卡（1011）")['id']
to_acc = get_account_by_name("支付宝")['id']

add_transfer(
    from_account_id=from_acc,
    to_account_id=to_acc,
    amount=5000.00,
    note='转账到支付宝'
)
# 自动生成：储蓄卡支出 ¥5000 + 支付宝收入 ¥5000
```

### 财务汇总

```python
from scripts.database import get_financial_summary
from scripts.statistics import format_assets_report

summary = get_financial_summary()
print(format_assets_report(summary))
```

输出示例：
```
══════════════ 财务汇总 ══════════════

【净资产】
总资产: ¥25,430.67
总负债: ¥3,500.00
净资产: ¥21,930.67

【收支概况】
本月收入: ¥15,000.00
本月支出: ¥8,245.50
本月结余: +¥6,754.50

【资产账户】
招商银行储蓄卡（1011）: ¥12,000.00
微信零钱: ¥1,430.67
支付宝: ¥2,000.00

【信用卡】
招商银行信用卡（3457）: 欠款 ¥3,500.00 / 额度 ¥50,000.00 / 可用 ¥46,500.00

【本月支出分类】
餐饮: ¥2,450.00 (29.7%)
交通: ¥1,200.00 (14.6%)
购物: ¥3,100.00 (37.6%)
人情往来: ¥500.00 (6.1%)
其他: ¥995.50 (12.1%)
```

## 使用规范

1. **禁止直接 SQL**：所有数据库操作必须通过 `database.py` 中的函数
2. **时间格式统一**：所有日期时间必须使用 `YYYY-MM-DD HH:MM:SS` 格式（精确到秒）
3. **order_no 必填**：图片识别时提取真实的订单号/交易单号/转账单号；手动录入时使用时间戳
4. **order_no 去重**：系统自动检测重复的 order_no，防止同一笔账单重复录入
5. **分类用英文值**：存储和 API 调用使用英文分类值（如 `food`），显示时自动转为中文（如"餐饮"）
6. **账户名称唯一**：同一数据库中账户名称不可重复
7. **信用卡独立显示**：财务汇总中信用卡欠款与资产账户分开

## 详细文档

更多细节（图片解析规则、支付方式映射、操作步骤等）请参阅 [SKILL.md](./SKILL.md)。
