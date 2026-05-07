# -*- coding: utf-8 -*-
"""
Personal Accounting - 数据库操作模块
"""
import sqlite3
import os
import re
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional, Tuple

# 数据库路径（相对于技能目录）
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(SKILL_DIR, 'db')
DB_PATH = os.path.join(DB_DIR, 'accounting.db')

# 东八区时区
CST = timezone(timedelta(hours=8))

def get_local_now() -> str:
    """获取当前本地时间（东八区），格式为 YYYY-MM-DD HH:MM:SS"""
    return datetime.now(CST).strftime('%Y-%m-%d %H:%M:%S')


def get_db_path():
    """获取数据库路径，确保目录存在"""
    os.makedirs(DB_DIR, exist_ok=True)
    return DB_PATH


# ==================== 账户名称格式化 ====================

def format_bank_account_name(bank_name: str, card_last_four: str, account_type: str = 'savings') -> str:
    """
    格式化银行卡账户名称

    Args:
        bank_name: 银行名称（如"招商银行"）
        card_last_four: 卡号后四位
        account_type: 账户类型 ('savings'/'savings_card' 或 'credit'/'credit_card')

    Returns:
        格式化后的账户名称
        - 储蓄卡：招商银行储蓄卡（1011）
        - 信用卡：招商银行信用卡（3457）
    """
    # 兼容新旧账户类型值
    type_map = {
        'savings': '储蓄卡', 'savings_card': '储蓄卡',
        'credit': '信用卡', 'credit_card': '信用卡'
    }
    # 处理 None 值
    bank_name = bank_name or ''
    card_last_four = card_last_four or '0000'
    type_name = type_map.get(account_type, account_type or '储蓄卡')
    return f"{bank_name}{type_name}（{card_last_four}）"


def extract_card_last_four(card_number: str) -> Optional[str]:
    """从卡号中提取后四位"""
    digits = re.sub(r'\D', '', card_number)
    if len(digits) >= 4:
        return digits[-4:]
    return None


def get_or_create_account(name: str, account_type: str, initial_balance: float = 0,
                          credit_limit: float = 0) -> Tuple[int, bool]:
    """
    获取或创建账户（如果不存在则创建）

    Args:
        name: 账户名称
        account_type: 账户类型
        initial_balance: 初始余额
        credit_limit: 信用卡额度

    Returns:
        (account_id, created): 账户ID和是否新建
    """
    existing = get_account_by_name(name)
    if existing:
        return existing['id'], False
    account_id = add_account(name, account_type, initial_balance, credit_limit)
    return account_id, True


def get_or_create_account_from_parser(account_info: Dict) -> Tuple[int, bool]:
    """
    根据解析结果获取或创建账户（支持自动识别银行卡命名）

    Args:
        account_info: 解析出的账户信息

    Returns:
        (account_id, created): 账户ID和是否新建

    Supported sources:
        - wechat: 微信零钱
        - alipay: 支付宝
        - bank_sms: 银行卡
    """
    name = None
    account_type = 'savings'

    # 银行卡处理
    if account_info.get('bank_name') and account_info.get('card_last_four'):
        name = format_bank_account_name(
            account_info['bank_name'],
            account_info['card_last_four'],
            account_info.get('account_type', 'savings')
        )
        account_type = account_info.get('account_type', 'savings')
    # 微信零钱
    elif account_info.get('source') == 'wechat':
        name = '微信零钱'
        account_type = 'wechat_wallet'
    # 支付宝（含余额宝）
    elif account_info.get('source') == 'alipay':
        name = '支付宝'
        account_type = 'alipay'
    # 股票账户
    elif account_info.get('source') == 'stock':
        name = account_info.get('name', '股票账户')
        account_type = 'stock'
    # 基金账户
    elif account_info.get('source') == 'fund':
        name = account_info.get('name', '基金账户')
        account_type = 'fund'
    # 直接指定名称
    elif 'name' in account_info:
        name = account_info['name']
        account_type = account_info.get('account_type', 'savings')
    else:
        raise ValueError("无法确定账户名称，请提供 bank_name+card_last_four 或 source 或 name")

    return get_or_create_account(name, account_type,
                                  account_info.get('initial_balance', 0),
                                  account_info.get('credit_limit', 0))


def get_connection():
    """获取数据库连接"""
    return sqlite3.connect(get_db_path())


def init_database():
    """初始化数据库，创建所有表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 创建账户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            account_type TEXT NOT NULL,
            initial_balance REAL DEFAULT 0,
            credit_limit REAL DEFAULT 0,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    
    # 创建收支记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            transaction_type TEXT NOT NULL CHECK(transaction_type IN ('income', 'expense')),
            account_id INTEGER NOT NULL,
            merchant TEXT,
            category TEXT NOT NULL,
            transaction_date TEXT NOT NULL,
            note TEXT,
            transfer_id INTEGER,
            created_at TEXT,
            FOREIGN KEY (account_id) REFERENCES accounts(id),
            FOREIGN KEY (transfer_id) REFERENCES transfers(id)
        )
    ''')
    
    # 创建转账记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transfers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_account_id INTEGER NOT NULL,
            to_account_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            transfer_time TEXT NOT NULL,
            note TEXT,
            created_at TEXT,
            FOREIGN KEY (from_account_id) REFERENCES accounts(id),
            FOREIGN KEY (to_account_id) REFERENCES accounts(id)
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_account ON transactions(account_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(transaction_type)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_transfers_from ON transfers(from_account_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_transfers_to ON transfers(to_account_id)')
    
    conn.commit()
    conn.close()


# ==================== 账户操作 ====================

def add_account(name: str, account_type: str, initial_balance: float = 0, credit_limit: float = 0) -> int:
    """
    添加账户

    Args:
        name: 账户名称
        account_type: 账户类型
        initial_balance: 初始余额，默认为0
        credit_limit: 信用卡额度，默认为0

    Returns:
        新账户ID

    Raises:
        ValueError: 账户名称已存在时抛出异常
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 应用层检查：验证账户名称唯一性
    cursor.execute('SELECT id FROM accounts WHERE name = ?', (name,))
    if cursor.fetchone():
        conn.close()
        raise ValueError(f"账户名称「{name}」已存在，请使用已存在的账户或换一个名称")

    cursor.execute(
        'INSERT INTO accounts (name, account_type, initial_balance, credit_limit, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)',
        (name, account_type, initial_balance, credit_limit, get_local_now(), get_local_now())
    )
    conn.commit()
    account_id = cursor.lastrowid
    conn.close()
    return account_id


def get_accounts() -> List[Dict]:
    """获取所有账户列表"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, account_type, initial_balance, credit_limit, created_at FROM accounts ORDER BY id')
    rows = cursor.fetchall()
    conn.close()
    
    accounts = []
    for row in rows:
        balance = calculate_account_balance(row[0])
        accounts.append({
            'id': row[0],
            'name': row[1],
            'account_type': row[2],
            'initial_balance': row[3],
            'credit_limit': row[4],
            'created_at': row[5],
            'current_balance': balance
        })
    return accounts


def get_account_by_id(account_id: int) -> Optional[Dict]:
    """根据ID获取账户"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, account_type, initial_balance, credit_limit FROM accounts WHERE id = ?', (account_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        balance = calculate_account_balance(row[0])
        return {
            'id': row[0],
            'name': row[1],
            'account_type': row[2],
            'initial_balance': row[3],
            'credit_limit': row[4],
            'current_balance': balance
        }
    return None


def get_account_by_name(name: str) -> Optional[Dict]:
    """根据名称获取账户"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, account_type, initial_balance, credit_limit FROM accounts WHERE name = ?', (name,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        balance = calculate_account_balance(row[0])
        return {
            'id': row[0],
            'name': row[1],
            'account_type': row[2],
            'initial_balance': row[3],
            'credit_limit': row[4],
            'current_balance': balance
        }
    return None


def update_account(account_id: int, name: str = None, account_type: str = None, 
                   initial_balance: float = None, credit_limit: float = None) -> bool:
    """更新账户信息"""
    conn = get_connection()
    cursor = conn.cursor()
    
    updates = []
    params = []
    if name is not None:
        updates.append('name = ?')
        params.append(name)
    if account_type is not None:
        updates.append('account_type = ?')
        params.append(account_type)
    if initial_balance is not None:
        updates.append('initial_balance = ?')
        params.append(initial_balance)
    if credit_limit is not None:
        updates.append('credit_limit = ?')
        params.append(credit_limit)
    
    if updates:
        updates.append('updated_at = ?')
        params.append(get_local_now())
        params.append(account_id)
        set_clause = ', '.join(updates)
        cursor.execute(f'UPDATE accounts SET {set_clause} WHERE id = ?', params)
        conn.commit()
    
    conn.close()
    return cursor.rowcount > 0


def delete_account(account_id: int) -> bool:
    """删除账户（需先删除关联记录）"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 先检查是否有关联的收支记录
    cursor.execute('SELECT COUNT(*) FROM transactions WHERE account_id = ?', (account_id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return False
    
    # 检查是否有作为转出/转入账户的转账记录
    cursor.execute('SELECT COUNT(*) FROM transfers WHERE from_account_id = ? OR to_account_id = ?', (account_id, account_id))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return False
    
    cursor.execute('DELETE FROM accounts WHERE id = ?', (account_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def calculate_account_balance(account_id: int) -> float:
    """计算账户当前余额"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 获取初始余额和账户类型
    cursor.execute('SELECT initial_balance, account_type FROM accounts WHERE id = ?', (account_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return 0
    
    initial_balance, account_type = row
    
    # 计算收入总额
    cursor.execute(
        'SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE account_id = ? AND transaction_type = ?',
        (account_id, 'income')
    )
    total_income = cursor.fetchone()[0]
    
    # 计算支出总额
    cursor.execute(
        'SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE account_id = ? AND transaction_type = ?',
        (account_id, 'expense')
    )
    total_expense = cursor.fetchone()[0]
    
    conn.close()
    
    # 计算余额（所有账户统一公式）
    # initial_balance: 资产为正数，负债（信用卡）为负数
    # 余额 = initial_balance + 收入 - 支出
    return round(initial_balance + total_income - total_expense, 2)


# ==================== 收支记录操作 ====================

def add_transaction(amount: float, transaction_type: str, account_id: int, 
                   category: str, transaction_date: str, merchant: str = None,
                   note: str = None, transfer_id: int = None) -> int:
    """
    添加收支记录
    
    Args:
        amount: 金额（正数）
        transaction_type: income 或 expense
        account_id: 账户ID
        category: 分类
        transaction_date: 交易日期 YYYY-MM-DD HH:MM（精确到分钟）
        merchant: 商家
        note: 备注
        transfer_id: 转账关联ID
    
    Returns:
        新记录ID
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (amount, transaction_type, account_id, merchant, category, transaction_date, note, transfer_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (round(amount, 2), transaction_type, account_id, merchant, category, transaction_date, note, transfer_id, get_local_now()))
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id


def get_transactions(account_id: int = None, transaction_type: str = None,
                    date_from: str = None, date_to: str = None,
                    category: str = None, limit: int = 100) -> List[Dict]:
    """查询收支记录"""
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = '''
        SELECT t.id, t.amount, t.transaction_type, t.account_id, a.name as account_name,
               t.merchant, t.category, t.transaction_date, t.note, t.transfer_id, t.created_at
        FROM transactions t
        JOIN accounts a ON t.account_id = a.id
        WHERE 1=1
    '''
    params = []
    
    if account_id:
        sql += ' AND t.account_id = ?'
        params.append(account_id)
    if transaction_type:
        sql += ' AND t.transaction_type = ?'
        params.append(transaction_type)
    if date_from:
        sql += ' AND t.transaction_date >= ?'
        params.append(date_from)
    if date_to:
        sql += ' AND t.transaction_date <= ?'
        params.append(date_to)
    if category:
        sql += ' AND t.category = ?'
        params.append(category)
    
    sql += ' ORDER BY t.transaction_date DESC, t.id DESC LIMIT ?'
    params.append(limit)
    
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            'id': row[0],
            'amount': row[1],
            'transaction_type': row[2],
            'account_id': row[3],
            'account_name': row[4],
            'merchant': row[5],
            'category': row[6],
            'transaction_date': row[7],
            'note': row[8],
            'transfer_id': row[9],
            'created_at': row[10]
        }
        for row in rows
    ]


def get_transaction_by_id(transaction_id: int) -> Optional[Dict]:
    """根据ID获取单条记录"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.id, t.amount, t.transaction_type, t.account_id, a.name as account_name,
               t.merchant, t.category, t.transaction_date, t.note, t.transfer_id, t.created_at
        FROM transactions t
        JOIN accounts a ON t.account_id = a.id
        WHERE t.id = ?
    ''', (transaction_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'amount': row[1],
            'transaction_type': row[2],
            'account_id': row[3],
            'account_name': row[4],
            'merchant': row[5],
            'category': row[6],
            'transaction_date': row[7],
            'note': row[8],
            'transfer_id': row[9],
            'created_at': row[10]
        }
    return None


def update_transaction(transaction_id: int, **kwargs) -> bool:
    """更新收支记录"""
    allowed_fields = ['amount', 'transaction_type', 'account_id', 'merchant', 'category', 'transaction_date', 'note']
    
    updates = []
    params = []
    for key, value in kwargs.items():
        if key in allowed_fields and value is not None:
            if key == 'amount':
                value = round(value, 2)
            updates.append(f'{key} = ?')
            params.append(value)
    
    if not updates:
        return False
    
    params.append(transaction_id)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f'UPDATE transactions SET {", ".join(updates)} WHERE id = ?', params)
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def delete_transaction(transaction_id: int) -> bool:
    """删除收支记录"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 如果有转账关联，先解除关联
    cursor.execute('UPDATE transactions SET transfer_id = NULL WHERE transfer_id = ?', (transaction_id,))
    cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


# ==================== 转账记录操作 ====================

def add_transfer(from_account_id: int, to_account_id: int, amount: float,
                transfer_time: str = None, note: str = None) -> Tuple[int, int, int]:
    """
    添加转账记录
    
    Args:
        from_account_id: 转出账户ID
        to_account_id: 转入账户ID
        amount: 转账金额
        transfer_time: 转账时间
        note: 备注
    
    Returns:
        (transfer_id, from_transaction_id, to_transaction_id)
    """
    if transfer_time is None:
        transfer_time = get_local_now()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # 创建转账记录
    cursor.execute('''
        INSERT INTO transfers (from_account_id, to_account_id, amount, transfer_time, note, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (from_account_id, to_account_id, round(amount, 2), transfer_time, note, get_local_now()))
    transfer_id = cursor.lastrowid
    
    # 获取转出账户类型
    cursor.execute('SELECT account_type FROM accounts WHERE id = ?', (from_account_id,))
    result = cursor.fetchone()
    if result is None:
        raise ValueError(f"转出账户 ID {from_account_id} 不存在")
    from_type = result[0]
    
    # 创建转出记录（支出）
    cursor.execute('''
        INSERT INTO transactions (amount, transaction_type, account_id, category, transaction_date, note, transfer_id, created_at)
        VALUES (?, 'expense', ?, 'transfer', ?, ?, ?, ?)
    ''', (round(amount, 2), from_account_id, transfer_time, note, transfer_id, get_local_now()))
    from_transaction_id = cursor.lastrowid
    
    # 创建转入记录（收入）
    cursor.execute('''
        INSERT INTO transactions (amount, transaction_type, account_id, category, transaction_date, note, transfer_id, created_at)
        VALUES (?, 'income', ?, 'transfer', ?, ?, ?, ?)
    ''', (round(amount, 2), to_account_id, transfer_time, note, transfer_id, get_local_now()))
    to_transaction_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return transfer_id, from_transaction_id, to_transaction_id


def get_transfers(date_from: str = None, date_to: str = None, 
                 account_id: int = None, limit: int = 100) -> List[Dict]:
    """查询转账记录"""
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = '''
        SELECT tr.id, tr.from_account_id, fa.name as from_account_name,
               tr.to_account_id, ta.name as to_account_name,
               tr.amount, tr.transfer_time, tr.note, tr.created_at
        FROM transfers tr
        JOIN accounts fa ON tr.from_account_id = fa.id
        JOIN accounts ta ON tr.to_account_id = ta.id
        WHERE 1=1
    '''
    params = []
    
    if date_from:
        sql += ' AND tr.transfer_time >= ?'
        params.append(date_from)
    if date_to:
        sql += ' AND tr.transfer_time <= ?'
        params.append(date_to)
    if account_id:
        sql += ' AND (tr.from_account_id = ? OR tr.to_account_id = ?)'
        params.append(account_id)
    
    sql += ' ORDER BY tr.transfer_time DESC LIMIT ?'
    params.append(limit)
    
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            'id': row[0],
            'from_account_id': row[1],
            'from_account_name': row[2],
            'to_account_id': row[3],
            'to_account_name': row[4],
            'amount': row[5],
            'transfer_time': row[6],
            'note': row[7],
            'created_at': row[8]
        }
        for row in rows
    ]


def delete_transfer(transfer_id: int) -> bool:
    """删除转账记录（同时删除关联的收支记录）"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 删除关联的收支记录
    cursor.execute('DELETE FROM transactions WHERE transfer_id = ?', (transfer_id,))
    # 删除转账记录
    cursor.execute('DELETE FROM transfers WHERE id = ?', (transfer_id,))
    conn.commit()
    conn.close()
    return True


# ==================== 统计汇总 ====================

def get_total_by_type(transaction_type: str, date_from: str = None, 
                     date_to: str = None, account_id: int = None) -> float:
    """获取某类型收支总额"""
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = 'SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE transaction_type = ?'
    params = [transaction_type]
    
    if date_from:
        sql += ' AND transaction_date >= ?'
        params.append(date_from)
    if date_to:
        sql += ' AND transaction_date <= ?'
        params.append(date_to)
    if account_id:
        sql += ' AND account_id = ?'
        params.append(account_id)
    
    cursor.execute(sql, params)
    total = cursor.fetchone()[0]
    conn.close()
    return round(total, 2)


def get_total_by_category(transaction_type: str, date_from: str = None,
                          date_to: str = None, account_id: int = None) -> List[Dict]:
    """按分类统计收支"""
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = '''
        SELECT category, SUM(amount) as total, COUNT(*) as count
        FROM transactions
        WHERE transaction_type = ?
    '''
    params = [transaction_type]
    
    if date_from:
        sql += ' AND transaction_date >= ?'
        params.append(date_from)
    if date_to:
        sql += ' AND transaction_date <= ?'
        params.append(date_to)
    if account_id:
        sql += ' AND account_id = ?'
        params.append(account_id)
    
    sql += ' GROUP BY category ORDER BY total DESC'
    
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {'category': row[0], 'total': round(row[1], 2), 'count': row[2]}
        for row in rows
    ]


def get_total_by_merchant(transaction_type: str = None,
                          date_from: str = None, date_to: str = None,
                          account_id: int = None) -> List[Dict]:
    """
    按商家统计收支

    Args:
        transaction_type: income 或 expense
        date_from: 开始日期 YYYY-MM-DD
        date_to: 结束日期 YYYY-MM-DD
        account_id: 账户ID（可选）

    Returns:
        [{'merchant': str, 'total': float, 'count': int}, ...]
    """
    conn = get_connection()
    cursor = conn.cursor()

    sql = '''
        SELECT merchant, SUM(amount) as total, COUNT(*) as count
        FROM transactions
        WHERE merchant IS NOT NULL AND merchant != ''
    '''
    params = []

    if transaction_type:
        sql += ' AND transaction_type = ?'
        params.append(transaction_type)
    if date_from:
        sql += ' AND transaction_date >= ?'
        params.append(date_from)
    if date_to:
        sql += ' AND transaction_date <= ?'
        params.append(date_to)
    if account_id:
        sql += ' AND account_id = ?'
        params.append(account_id)

    sql += ' GROUP BY merchant ORDER BY total DESC'

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    return [
        {'merchant': row[0], 'total': round(row[1], 2), 'count': row[2]}
        for row in rows
    ]


def get_total_by_account(transaction_type: str = None, date_from: str = None,
                         date_to: str = None) -> List[Dict]:
    """按账户统计收支"""
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = '''
        SELECT a.id, a.name, a.account_type, a.initial_balance, a.credit_limit,
               COALESCE(SUM(CASE WHEN t.transaction_type = 'income' THEN t.amount ELSE 0 END), 0) as total_income,
               COALESCE(SUM(CASE WHEN t.transaction_type = 'expense' THEN t.amount ELSE 0 END), 0) as total_expense,
               COUNT(CASE WHEN t.transaction_type = 'income' THEN 1 END) as income_count,
               COUNT(CASE WHEN t.transaction_type = 'expense' THEN 1 END) as expense_count
        FROM accounts a
        LEFT JOIN transactions t ON a.id = t.account_id
        WHERE 1=1
    '''
    params = []
    
    if transaction_type:
        sql += ' AND t.transaction_type = ?'
        params.append(transaction_type)
    if date_from:
        sql += ' AND t.transaction_date >= ?'
        params.append(date_from)
    if date_to:
        sql += ' AND t.transaction_date <= ?'
        params.append(date_to)
    
    sql += ' GROUP BY a.id ORDER BY a.id'
    
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    
    result = []
    for row in rows:
        current_balance = round(row[3] + row[5] - row[6], 2)
        if row[2] == 'credit_card':
            available = round(row[4] - row[6] + row[5], 2)
        else:
            available = current_balance
        
        result.append({
            'account_id': row[0],
            'account_name': row[1],
            'account_type': row[2],
            'initial_balance': row[3],
            'credit_limit': row[4],
            'total_income': round(row[5], 2),
            'total_expense': round(row[6], 2),
            'current_balance': current_balance,
            'available_amount': available,
            'income_count': row[7],
            'expense_count': row[8]
        })
    
    return result


def get_daily_summary(date_from: str, date_to: str) -> List[Dict]:
    """获取每日收支汇总"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT transaction_date,
               COALESCE(SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END), 0) as total_income,
               COALESCE(SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END), 0) as total_expense,
               COUNT(CASE WHEN transaction_type = 'income' THEN 1 END) as income_count,
               COUNT(CASE WHEN transaction_type = 'expense' THEN 1 END) as expense_count
        FROM transactions
        WHERE transaction_date >= ? AND transaction_date <= ?
        GROUP BY transaction_date
        ORDER BY transaction_date DESC
    ''', (date_from, date_to))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            'date': row[0],
            'total_income': round(row[1], 2),
            'total_expense': round(row[2], 2),
            'net': round(row[1] - row[2], 2),
            'income_count': row[3],
            'expense_count': row[4]
        }
        for row in rows
    ]


def get_monthly_summary(year: int = None, month: int = None) -> List[Dict]:
    """获取月度收支汇总"""
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month
    
    date_from = f'{year}-{month:02d}-01'
    # 计算月末
    if month == 12:
        date_to = f'{year + 1}-01-01'
    else:
        date_to = f'{year}-{month + 1:02d}-01'
    
    return get_daily_summary(date_from, date_to)


def get_account_transactions_with_transfers(account_id: int, date_from: str = None,
                                            date_to: str = None, limit: int = 100) -> List[Dict]:
    """获取账户所有流水（含转账关联信息）"""
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = '''
        SELECT 
            t.id,
            t.amount,
            t.transaction_type,
            t.merchant,
            t.category,
            t.transaction_date,
            t.note,
            t.transfer_id,
            t.created_at,
            CASE 
                WHEN t.transfer_id IS NOT NULL THEN 
                    CASE 
                        WHEN t.transaction_type = 'expense' THEN 
                            (SELECT ta.name FROM transfers tr JOIN accounts ta ON tr.to_account_id = ta.id WHERE tr.id = t.transfer_id)
                        ELSE 
                            (SELECT fa.name FROM transfers tr JOIN accounts fa ON tr.from_account_id = fa.id WHERE tr.id = t.transfer_id)
                    END
                ELSE NULL
            END as counterparty,
            CASE 
                WHEN t.transfer_id IS NOT NULL THEN 
                    CASE 
                        WHEN t.transaction_type = 'expense' THEN '转出到'
                        ELSE '转入自'
                    END
                ELSE NULL
            END as transfer_desc
        FROM transactions t
        WHERE t.account_id = ?
    '''
    params = [account_id]
    
    if date_from:
        sql += ' AND t.transaction_date >= ?'
        params.append(date_from)
    if date_to:
        sql += ' AND t.transaction_date <= ?'
        params.append(date_to)
    
    sql += ' ORDER BY t.transaction_date DESC, t.id DESC LIMIT ?'
    params.append(limit)
    
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            'id': row[0],
            'amount': row[1],
            'transaction_type': row[2],
            'merchant': row[3],
            'category': row[4],
            'transaction_date': row[5],
            'note': row[6],
            'transfer_id': row[7],
            'created_at': row[8],
            'counterparty': row[9],
            'transfer_desc': row[10]
        }
        for row in rows
    ]



def get_financial_summary() -> Dict:
    """获取财务汇总数据（资产、负债、收支统计）"""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    now = datetime.now()
    current_year = now.year
    current_month = now.month

    if current_month == 1:
        last_month_year = current_year - 1
        last_month = 12
    else:
        last_month_year = current_year
        last_month = current_month - 1

    current_month_start = f"{current_year}-{current_month:02d}-01"
    last_month_start = f"{last_month_year}-{last_month:02d}-01"
    last_month_end = f"{last_month_year}-{last_month:02d}-31"

    cursor.execute("SELECT * FROM accounts ORDER BY account_type, name")
    accounts = cursor.fetchall()

    account_balances = {}
    for acc in accounts:
        cursor.execute("""
            SELECT COALESCE(SUM(CASE WHEN transaction_type='income' THEN amount ELSE 0 END), 0) as income,
                   COALESCE(SUM(CASE WHEN transaction_type='expense' THEN amount ELSE 0 END), 0) as expense
            FROM transactions WHERE account_id = ?
        """, (acc['id'],))
        result = cursor.fetchone()
        balance = acc['initial_balance'] + result['income'] - result['expense']
        account_balances[acc['id']] = balance

    cursor.execute("""
        SELECT COALESCE(SUM(CASE WHEN transaction_type='income' THEN amount ELSE 0 END), 0) as income,
               COALESCE(SUM(CASE WHEN transaction_type='expense' THEN amount ELSE 0 END), 0) as expense
        FROM transactions WHERE transaction_date >= ? AND transaction_date <= ?
    """, (current_month_start, f"{current_month}-{now.day:02d} 23:59"))
    current_stats = cursor.fetchone()

    cursor.execute("""
        SELECT COALESCE(SUM(CASE WHEN transaction_type='income' THEN amount ELSE 0 END), 0) as income,
               COALESCE(SUM(CASE WHEN transaction_type='expense' THEN amount ELSE 0 END), 0) as expense
        FROM transactions WHERE transaction_date >= ? AND transaction_date <= ?
    """, (last_month_start, last_month_end))
    last_stats = cursor.fetchone()

    cursor.execute("""
        SELECT category, SUM(amount) as total
        FROM transactions WHERE transaction_type='expense' AND transaction_date >= ?
        GROUP BY category ORDER BY total DESC
    """, (current_month_start,))
    expense_by_category = cursor.fetchall()

    total_assets = 0
    total_debt = 0
    asset_accounts = []
    credit_accounts = []

    for acc in accounts:
        balance = account_balances[acc['id']]
        if acc['account_type'] == 'credit_card':
            total_debt += abs(balance)
            credit_accounts.append({
                'name': acc['name'],
                'balance': abs(balance),
                'credit_limit': acc['credit_limit'],
                'available': acc['credit_limit'] - abs(balance)
            })
        else:
            total_assets += balance
            asset_accounts.append({
                'name': acc['name'],
                'balance': balance,
                'account_type': acc['account_type']
            })

    conn.close()

    return {
        'net_worth': round(total_assets - total_debt, 2),
        'total_assets': round(total_assets, 2),
        'total_debt': round(total_debt, 2),
        'current_month': {
            'income': round(current_stats['income'], 2),
            'expense': round(current_stats['expense'], 2),
            'net': round(current_stats['income'] - current_stats['expense'], 2)
        },
        'last_month': {
            'income': round(last_stats['income'], 2),
            'expense': round(last_stats['expense'], 2),
            'net': round(last_stats['income'] - last_stats['expense'], 2)
        },
        'asset_accounts': asset_accounts,
        'credit_accounts': credit_accounts,
        'expense_by_category': [dict(row) for row in expense_by_category]
    }


if __name__ == '__main__':
    # 初始化数据库
    init_database()
    print('数据库初始化完成')
    
    # 测试添加账户
    accounts = get_accounts()
    print(f'\n当前账户数: {len(accounts)}')
    for acc in accounts:
        print(f"  {acc['name']}: ¥{acc['current_balance']:.2f}")
