# Personal Accounting - 个人记账助手

智能个人记账系统，支持账单图片解析、手动录入、账户管理、转账记录和统计分析。

## 触发条件

当用户消息包含以下关键词时自动触发此技能：记账、记一笔、记录、花了、消费、买了、付款、支付、转账、日报、周报、月报、年报、财务汇总、统计、汇总、账户、余额、账单、流水、收支、收入、支出、信用卡、储蓄卡、微信、支付宝、现金、分类统计、商家统计。

## Agent 使用规范（重要）

### 执行方式优先级（强制执行）

**CRITICAL：所有操作必须优先使用技能内置函数。禁止 Agent 自己创建脚本执行查询或统计操作，除非技能中确实没有相应的功能。**

| 优先级 | 方式 | 说明 |
|--------|------|------|
| **1（首选）** | 使用内置 `get_xxx_text()` 函数 | 所有查询和统计操作都有对应的内置函数，直接调用即可 |
| **2（备选）** | 编写临时脚本调用内置函数 | 仅当需要组合多个函数、或需要特殊参数格式时使用 |
| **3（最后手段）** | 编写临时脚本直接查询 | 仅当内置函数完全不满足需求时才允许，且必须用完后删除 |

### 内置函数速查表

**查询/报表类（直接调用，返回格式化文本）：**

| 用户意图 | 调用函数 | 返回内容 |
|----------|----------|----------|
| 财务汇总 | `get_assets_report_text()` | 净资产、收支概况、资产账户、信用卡、支出分类 |
| 日报 | `get_daily_report_text()` | 当日收支总览 + 明细 + 汇总 |
| 周报 | `get_weekly_report_text()` | 本周收支总览 + 汇总 |
| 月报 | `get_monthly_detailed_report_text()` | 本月收支总览 + 汇总 |
| 年报 | `get_yearly_report_text()` | 本年收支总览 + 汇总 |
| 月度对比 | `get_monthly_report_text()` | 多个月份的收支对比 |
| 分类统计 | `get_category_report_text()` | 按分类汇总收支 |
| 账户余额 | `get_account_balance_report_text()` | 所有账户余额列表 |
| 账户流水 | `get_account_detail_report_text(account_id)` | 指定账户的所有交易明细 |
| 所有交易 | `get_transactions()` + `format_transactions_report()` | 交易记录列表 |
| 所有转账 | `get_transfers()` + `format_transfers_report()` | 转账记录列表 |

**写入/修改类（直接调用 database.py 函数）：**

| 用户意图 | 调用函数 |
|----------|----------|
| 添加账户 | `add_account(name, account_type, ...)` |
| 查看账户 | `get_accounts()` |
| 添加交易 | `add_transaction(amount, transaction_type, account_id, ...)` |
| 添加转账 | `add_transfer(from_account_id, to_account_id, amount, ...)` |
| 更新交易 | `update_transaction(transaction_id, **kwargs)` |
| 删除交易 | `delete_transaction(transaction_id)` |
| 图片解析 | `parse_and_save_transactions(records)` |

**所有内置函数位于：**
- `scripts/statistics.py` — 统计报表和格式化函数
- `scripts/database.py` — 数据库操作函数
- `scripts/parser.py` — 账单图片解析函数

### 临时脚本规范（仅在必要时使用）

**仅在技能内置函数确实无法满足需求时，才允许创建临时脚本。创建时必须遵守：**

1. **临时脚本写在工作区根目录下**（`{workspace}/`），不要写在技能目录里。技能目录是代码库，不应被临时文件污染。
2. **使用有意义的文件名**，如 `_query_daily_report.py`、`_add_transaction.py`，前缀 `_` 表示临时文件。
3. **执行完毕后立即删除临时脚本**，不要让临时文件残留。如果生成了输出文件（如 `output.txt`），读完后也一并删除。
4. **禁止直接写 SQL 查询**：临时脚本中也必须通过 `database.py` 中的函数操作数据，不得直接使用 `sqlite3` 写 SQL。

正确方式：
```bash
# 1. 在 workspace 根目录写一个 .py 脚本（如 _query_accounts.py）
# 2. 执行: python _query_accounts.py
# 3. 执行完毕后删除: del _query_accounts.py（Windows）/ rm _query_accounts.py（Linux）
```

**中文输出编码处理**
Windows 控制台默认 GBK 编码，直接 print 中文会乱码。务必在脚本开头添加：
```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```
或使用写入文件方式（见下方示例）。

```python
# 方式1: 重新配置 stdout（推荐）
import sys
sys.stdout.reconfigure(encoding='utf-8')
print("中文输出测试")

# 方式2: 写入文件再读取
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(f"账户名称: {name}\n")
```

数据库路径：
```
{技能目录}\db\accounting.db
```
> 路径由 `database.py` 中的 `DB_PATH` 自动计算，无需手动指定。

---

## 核心原则（必须遵守）

1. **图片解析直接入库**：收到账单图片 → AI解析 → **直接保存**，不询问确认
2. **使用技能内置函数**：所有数据操作必须通过 `database.py` 中的函数，禁止直接写 SQL
3. **先更新技能再执行新功能**：遇到技能没有的功能时，先补充技能文档和函数，再执行
4. **信用卡欠款独立显示**：财务汇总中信用卡欠款必须与资产账户分开显示

---

## 一、数据库表结构

> **⚠️ 数据库结构保护规则**
>
> 1. **禁止修改表结构**：不得 ALTER TABLE、CREATE TABLE、DROP TABLE 等操作
> 2. **禁止直接操作数据**：不得直接 INSERT/UPDATE/DELETE 数据，必须通过本技能定义的函数
> 3. **账户名称唯一性**：同一数据库中账户名称不可重复
> 4. **数据一致性**：所有操作必须保持数据完整性，不得绕过约束
> 5. **时间格式强制统一**：
>    - **所有收支记录和转账记录的日期/时间字段，必须使用 `YYYY-MM-DD HH:MM:SS` 格式（精确到秒）**
>    - 如果用户未提供具体时间，自动以记录的创建时间（current_timestamp）作为交易时间
>    - 禁止使用 `YYYY-MM-DD`、`YYYY-MM-DD HH:MM` 或其他任何不完整的时间格式

### 1. accounts 表（账户信息）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY | 账户唯一标识 |
| name | TEXT NOT NULL UNIQUE | 账户名称（唯一） |
| account_type | TEXT NOT NULL | 账户类型（见下方类型定义） |
| initial_balance | REAL DEFAULT 0 | 初始余额，默认为0 |
| credit_limit | REAL DEFAULT 0 | 信用卡固定额度（仅信用卡有效） |
| created_at | TEXT | 创建时间（东八区，YYYY-MM-DD HH:MM:SS） |
| updated_at | TEXT | 更新时间（东八区，YYYY-MM-DD HH:MM:SS） |

**账户类型 (account_type)：**
| 类型值 | 说明 |
|--------|------|
| savings_card | 储蓄卡 |
| credit_card | 信用卡 |
| wechat_wallet | 微信零钱 |
| alipay | 支付宝 |
| stock | 股票账户 |
| fund | 基金账户 |
| cash | 现金 |
| other | 其他 |

**说明：**
- **支付宝账户**：统一管理支付宝余额、余额宝、花呗等资金
  - 余额宝是支付宝的货币基金账户，如需单独追踪可使用备注字段
  - 花呗是支付宝的消费信贷服务，属于支付宝账户管理
  - **转账等操作涉及花呗或余额宝时，都视为支付宝账户**
- 股票账户：用于记录股票买卖、持仓市值
- 基金账户：用于记录基金申赎、持仓市值

### 2. transactions 表（收支记录）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY | 记录唯一标识 |
| amount | REAL NOT NULL | 金额（始终为正数） |
| transaction_type | TEXT NOT NULL | 类型：income(收入) / expense(支出) |
| account_id | INTEGER NOT NULL | 账户ID（外键） |
| merchant | TEXT | 商家/商户名称 |
| category | TEXT NOT NULL | 分类 |
| transaction_date | TEXT NOT NULL | 交易日期（YYYY-MM-DD HH:MM:SS，精确到秒） |
| note | TEXT | 备注信息 |
| transfer_id | INTEGER | 关联转账ID（如果是由转账产生） |
| created_at | TEXT | 创建时间 |

### 3. transfers 表（转账记录）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY | 转账记录唯一标识 |
| from_account_id | INTEGER NOT NULL | 转出账户ID（外键） |
| to_account_id | INTEGER NOT NULL | 转入账户ID（外键） |
| amount | REAL NOT NULL | 转账金额 |
| transfer_time | TEXT NOT NULL | 转账时间（YYYY-MM-DD HH:MM:SS，东八区） |
| note | TEXT | 备注 |
| created_at | TEXT | 创建时间（东八区，YYYY-MM-DD HH:MM:SS） |

### 4. 转账与收支记录联动机制（重要）

**转账操作会自动产生两条收支记录：**

| 操作 | 收支类型 | 账户 | 说明 |
|------|----------|------|------|
| 转出 | expense（支出） | from_account_id | 从源账户扣除金额 |
| 转入 | income（收入） | to_account_id | 向目标账户增加金额 |

**关联方式：**
- 两条收支记录的 `transfer_id` 字段指向同一转账记录 ID
- 删除转账记录时，关联的收支记录会**一并删除**
- 删除收支记录时，转账记录保持不变（仅解除关联）

**示例：**
- 从「招商银行储蓄卡」转账 ¥1000 到「支付宝」
- 自动创建：
  - 支出记录：储蓄卡 -¥1000（transfer_id=1）
  - 收入记录：支付宝 +¥1000（transfer_id=1）
  - 转账记录：ID=1，关联以上两条记录

---

## 二、账户管理

### 支持的账户类型

| 类型 | 类型值 | 特点 |
|------|--------|------|
| 储蓄卡 | savings_card | 银行储蓄卡，支持收入/支出 |
| 信用卡 | credit_card | 有固定额度，有剩余额度，支出增加欠款 |
| 微信零钱 | wechat_wallet | 微信支付账户 |
| 支付宝 | alipay | 支付宝账户（含余额宝） |
| 股票账户 | stock | 股票投资账户 |
| 基金账户 | fund | 基金投资账户 |
| 现金 | cash | 现金 |
| 其他 | other | 其他类型账户 |

### 余额计算规则（统一公式）

**核心原则：所有账户使用统一公式计算，`initial_balance` 直接反映账户性质。**

**计算公式（所有账户类型统一）：**
```
余额 = initial_balance + 收入总和 - 支出总和
```

**initial_balance 的录入规则：**
- **资产类账户**（储蓄卡、微信、支付宝、基金、股票、现金）：录入**正数**
- **负债类账户**（信用卡）：录入**负数**（表示欠款）

**示例：**
- 储蓄卡：创建时存入 ¥10,000 → `initial_balance` = 10,000
- 微信零钱：创建时有钱 ¥1,430.67 → `initial_balance` = 1,430.67
- 信用卡：创建时欠 ¥500 → `initial_balance` = -500

**显示规则：**
- 非信用卡账户：显示「余额」（可能为正）
- 信用卡账户：显示「欠款」（取绝对值），额度独立显示

**净资产计算：**
```
总资产 = 所有资产账户余额之和（正数）
总负债 = 所有信用卡欠款绝对值之和
净资产 = 总资产 - 总负债
```

---

## 三、消费分类

### 支出分类

| 分类 | 说明 |
|------|------|
| food | 餐饮 |
| transportation | 交通 |
| shopping | 购物 |
| entertainment | 娱乐 |
| bills | 账单（水电费、话费等） |
| healthcare | 医疗 |
| social | 人情往来 |
| education | 教育 |
| housing | 住房 |
| investment | 投资理财支出 |
| other | 其他 |

### 收入分类

| 分类 | 说明 |
|------|------|
| salary | 工资 |
| bonus | 奖金 |
| investment | 投资收益 |
| gift | 礼金/红包 |
| refund | 退款 |
| other | 其他收入 |

---

## 四、功能特性

### 1. 图片解析账单
- 📷 上传账单截图（微信、支付宝、银行短信等）
- 🔍 AI 自动识别消费金额、时间、商户、分类
- ✏️ **直接入库，不需二次确认**

### 2. 手动录入账单
- 💰 支持收入、支出记录
- 📝 填写金额、账户、商家、分类、日期、备注

### 3. 转账记录
- 🔄 账户间转账
- 📊 自动关联收支记录
- 💳 信用卡还款视为转账

### 4. 账户管理
- ➕ 添加新账户（设置初始余额、信用卡额度）
- 📝 编辑账户信息
- 🗑️ 删除账户（需确认无关联记录）
- 📊 查看所有账户及余额

### 5. 统计汇总
- 📊 **财务汇总**：所有账户汇总、收支汇总、净资产、本月及上月收支对比
- 📋 **日报**：当日所有支出/收入明细分开显示，支出按账户和分类分组汇总
- 📅 **周报**：本周（周一~周日）所有支出/收入明细，支出按账户和分类分组汇总
- 🗓️ **月报**：本月所有支出/收入明细，支出按账户和分类分组汇总
- 🗓️ **年报**：本年所有支出/收入明细，支出按账户和分类分组汇总
- 📂 按分类统计收支
- 🏪 按商家统计收支（收入/支出分别统计）
- 🏦 按账户统计
- 📈 趋势分析

---

## 五、常用操作示例

### 5.1 添加账户

```
用户: 添加一个工商银行的储蓄卡账户
→ 创建账户：名称=工商银行储蓄卡，类型=savings_card，初始余额=0

用户: 添加一张招商银行信用卡，额度5万
→ 创建账户：名称=招商信用卡，类型=credit_card，固定额度=50000

用户: 添加微信零钱账户，初始有1000元
→ 创建账户：名称=微信零钱，类型=wechat_wallet，初始余额=1000
```

### 5.2 记录支出

```
用户: 今天在麦当劳消费了45元，用微信支付的
→ 记录支出：金额=45，类型=expense，账户=微信零钱，商家=麦当劳，分类=food，日期=今天

用户: 上传了支付宝截图
→ AI解析图片 → 显示解析结果 → 用户确认 → 保存记录
```

### 5.3 记录收入

```
用户: 今天发了工资15000元到工商卡
→ 记录收入：金额=15000，类型=income，账户=工商银行储蓄卡，商家=公司，分类=salary

用户: 收到红包200元，微信
→ 记录收入：金额=200，类型=income，账户=微信零钱，商家=红包，分类=gift
```

### 5.4 转账记录

```
用户: 从工商卡转了5000到支付宝
→ 记录转账：转出账户=工商银行储蓄卡，转入账户=支付宝，金额=5000
→ 自动生成两条关联的收支记录

用户: 用工商卡还了信用卡3000
→ 记录转账：转出账户=工商银行储蓄卡，转入账户=招商信用卡，金额=3000，备注=还信用卡
```

### 5.5 更新和删除记录

```
用户: 把记录ID 19的分类改成餐饮，备注改成洛馍
→ 调用 update_transaction(id=19, category='food', note='洛馍')

用户: 删除记录ID 20
→ 调用 delete_transaction(id=20)
```

### 5.6 查询统计

```
用户: 查看所有账户余额
→ 返回：所有账户名称、类型、余额列表

用户: 财务汇总
→ 调用 get_financial_summary() → format_assets_report()
→ 返回：净资产、总资产/总负债、本月/上月收支对比、资产账户列表、信用卡欠款、本月支出分类

用户: 日报 / 今天花了多少钱
→ 调用 get_daily_report_text()
→ 返回：当日收支总览、支出明细、收入明细、支出按账户汇总、支出按分类汇总

用户: 周报 / 这周花了多少
→ 调用 get_weekly_report_text()
→ 返回：本周（周一~周日）收支总览、支出明细、收入明细、支出按账户汇总、支出按分类汇总

用户: 月报 / 这个月花了多少
→ 调用 get_monthly_detailed_report_text()
→ 返回：本月收支总览、支出明细、收入明细、支出按账户汇总、支出按分类汇总

用户: 查看本月支出统计
→ 返回：本月支出总额、各分类支出占比

用户: 按商家统计一下支出
→ 调用 get_total_by_merchant(transaction_type='expense')
→ 返回：各商家支出笔数和金额

用户: 查看工商卡这个月的流水
→ 返回：该账户所有收支记录（含转账）
```

### 5.7 财务汇总

```
用户: 财务汇总
```

财务汇总**必须**调用 `get_financial_summary()` 获取数据，用 `format_assets_report()` 格式化输出，按以下结构显示：

**【净资产】**
- 总资产、总负债、净资产

**【收支概况】**
- 本月收入、本月支出、本月结余（正数显示 +¥xxx，负数显示 -¥xxx）
- 上月收入、上月支出、上月结余

**【资产账户】**（储蓄卡、微信、支付宝、现金、股票、基金）
- 每行显示：账户名 (类型): 余额

**【信用卡】**（独立分组）
- 每行显示：账户名: 欠款 / 额度 / 可用额度
- 欠款 = |initial_balance + 累计支出 - 累计收入|
- 可用额度 = 固定额度 - 欠款

**【本月支出分类】**
- 每行显示：分类名: 金额 (百分比)

---

## 六、金额规则

- **所有金额保留两位小数**
- **币种：人民币 (CNY)**
- **金额格式：¥1,234.56**

---

## 七、数据库路径

```
{技能目录}\db\accounting.db
```
> 路径由 `database.py` 中的 `DB_PATH` 自动计算，无需手动指定。
```

---

## 八、银行卡账户命名规则

创建银行卡账户时，账户名自动按以下规则命名：

| 银行卡 | 命名格式 | 示例 |
|--------|----------|------|
| 储蓄卡 | 银行名称 + 储蓄卡（后四位） | 招商银行储蓄卡（1011） |
| 信用卡 | 银行名称 + 信用卡（后四位） | 招商银行信用卡（3457） |

相关函数：
```python
from scripts.database import format_bank_account_name, get_or_create_account_from_parser

# 生成账户名称
name = format_bank_account_name("招商银行", "1011", "savings")
# 结果: "招商银行储蓄卡（1011）"

name = format_bank_account_name("招商银行", "3457", "credit")
# 结果: "招商银行信用卡（3457）"
```

---

## 九、自动创建账户功能

当解析账单时，如果检测到未创建的账户，系统会自动创建：

```python
from scripts.parser import parse_and_save_transactions

# 解析账单并自动创建账户
result = parse_and_save_transactions([{
    'amount': 38.50,
    'transaction_type': 'expense',
    'source': 'wechat',  # 自动创建"微信零钱"账户
    'merchant': '星巴克',
    'category': 'food',
    'transaction_date': '2024-01-15'
}])

# 返回结果
# {
#     'total_parsed': 1,
#     'total_saved': 1,
#     'created_accounts': ['微信零钱'],  # 新创建的账户
#     'records': [{...}]                 # 保存的记录
# }
```

**支持的自动识别来源：**

| source | 账户名 | account_type |
|--------|--------|--------------|
| wechat | 微信零钱 | wechat_wallet |
| alipay | 支付宝 | alipay |
| stock | 股票账户 | stock |
| fund | 基金账户 | fund |
| bank_sms | 银行名称+类型（后四位） | savings_card / credit_card |

**注意：** 余额宝已合并到支付宝账户中统一管理，无需单独创建。

---

## 十、收支记录更新与删除

### 更新记录

```python
from scripts.database import update_transaction

# 更新记录（只更新提供的字段）
update_transaction(19, category='food', note='洛馍')
```

**支持的更新字段：**

| 字段 | 说明 |
|------|------|
| amount | 金额 |
| transaction_type | 类型（income/expense） |
| account_id | 账户ID |
| merchant | 商家/商户 |
| category | 分类 |
| transaction_date | 交易日期（YYYY-MM-DD HH:MM:SS） |
| note | 备注 |

### 删除记录

```python
from scripts.database import delete_transaction

# 删除记录（自动解除转账关联）
delete_transaction(20)
```

---

## 十一、错误处理

| 错误类型 | 说明 | 处理建议 |
|----------|------|----------|
| 账户不存在 | 指定的账户ID或名称不存在 | 先创建账户或检查名称 |
| 余额不足 | 转账金额超过转出账户余额 | 检查账户余额 |
| 无效金额 | 金额为负数或非数字 | 输入正确的金额 |
| 无效日期 | 日期格式不正确 | 使用 YYYY-MM-DD HH:MM:SS 格式 |
| 账户类型错误 | 无效的账户类型 | 检查类型值 |
