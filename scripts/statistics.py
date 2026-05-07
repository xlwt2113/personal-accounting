# -*- coding: utf-8 -*-
"""
Personal Accounting - 统计报表模块
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.database import (
    get_accounts, get_transactions, get_transfers,
    get_total_by_type, get_total_by_category, get_total_by_account,
    get_daily_summary, get_monthly_summary, get_financial_summary,
    get_account_transactions_with_transfers
)


# 分类中文名称映射
CATEGORY_NAMES = {
    'food': '餐饮',
    'transportation': '交通',
    'shopping': '购物',
    'entertainment': '娱乐',
    'bills': '账单',
    'healthcare': '医疗',
    'education': '教育',
    'housing': '住房',
    'investment': '投资理财',
    'salary': '工资',
    'bonus': '奖金',
    'gift': '礼金红包',
    'refund': '退款',
    'transfer': '转账',
    'other': '其他',
}

# 账户类型中文名称映射
ACCOUNT_TYPE_NAMES = {
    'savings_card': '储蓄卡',
    'savings': '储蓄卡',      # 兼容旧数据
    'credit_card': '信用卡',
    'credit': '信用卡',       # 兼容旧数据
    'wechat_wallet': '微信零钱',
    'alipay': '支付宝',
    'stock': '股票账户',
    'fund': '基金账户',
    'cash': '现金',
    'other': '其他',
}


def format_currency(amount: float) -> str:
    """格式化货币金额"""
    return f"¥{amount:,.2f}"


def get_category_name(category: str) -> str:
    """获取分类中文名称"""
    return CATEGORY_NAMES.get(category, category)


def get_account_type_name(account_type: str) -> str:
    """获取账户类型中文名称"""
    return ACCOUNT_TYPE_NAMES.get(account_type, account_type)


def format_report_text(data: Dict, report_type: str) -> str:
    """
    格式化报表为可读文本
    
    Args:
        data: 报表数据
        report_type: 报表类型
    
    Returns:
        格式化的文本
    """
    if report_type == 'assets':
        return format_assets_report(data)
    elif report_type == 'account':
        return format_account_balance_report(data)
    elif report_type == 'account_detail':
        return format_account_detail_report(data)
    elif report_type == 'monthly':
        return format_monthly_report(data)
    elif report_type == 'daily':
        return format_daily_report(data)
    elif report_type == 'category':
        return format_category_report(data)
    elif report_type == 'transactions':
        return format_transactions_report(data)
    elif report_type == 'transfers':
        return format_transfers_report(data)
    
    return str(data)


def format_assets_report(data: Dict) -> str:
    """格式化资产汇总报表（基于 get_financial_summary 返回值）"""
    # 净值格式化：正值显示为 +¥xxx，负值显示为 -¥xxx
    def fmt_net(v):
        return f"+¥{v:,.2f}" if v >= 0 else f"-¥{abs(v):,.2f}"
    
    lines = []
    lines.append("资产汇总报表")
    lines.append("=" * 40)
    lines.append(f"净资产: {format_currency(data['net_worth'])}")
    lines.append(f"总资产: {format_currency(data['total_assets'])}")
    lines.append(f"总负债: {format_currency(data['total_debt'])}")
    lines.append("")
    lines.append("本月收支:")
    lines.append(f"  收入: {format_currency(data['current_month']['income'])}")
    lines.append(f"  支出: {format_currency(data['current_month']['expense'])}")
    lines.append(f"  净值: {fmt_net(data['current_month']['net'])}")
    lines.append("")
    lines.append("上月收支:")
    lines.append(f"  收入: {format_currency(data['last_month']['income'])}")
    lines.append(f"  支出: {format_currency(data['last_month']['expense'])}")
    lines.append(f"  净值: {fmt_net(data['last_month']['net'])}")
    lines.append("")
    lines.append("资产账户:")
    for acc in data.get('asset_accounts', []):
        lines.append(f"  {acc['name']}: {format_currency(acc['balance'])}")
    lines.append("")
    lines.append("信用卡欠款:")
    for card in data.get('credit_accounts', []):
        lines.append(f"  {card['name']}: 欠款 {format_currency(card['balance'])}, 额度 {format_currency(card['credit_limit'])}, 可用 {format_currency(card['available'])}")
    
    # 本月支出分类
    if data.get('expense_by_category'):
        lines.append("")
        lines.append("本月支出分类:")
        total_exp = sum(c['total'] for c in data['expense_by_category'])
        for cat in data['expense_by_category']:
            pct = cat['total'] / total_exp * 100
            cat_name = CATEGORY_NAMES.get(cat['category'], cat['category'])
            lines.append(f"  {cat_name}: {format_currency(cat['total'])} ({pct:.0f}%)")
    
    return '\n'.join(lines)


def format_account_balance_report(accounts: List[Dict]) -> str:
    """格式化账户余额报表"""
    lines = []
    lines.append("账户余额报表")
    lines.append("=" * 60)
    
    # 按类型分组
    by_type = {}
    for acc in accounts:
        acc_type = acc['account_type']
        if acc_type not in by_type:
            by_type[acc_type] = []
        by_type[acc_type].append(acc)
    
    for acc_type, accs in by_type.items():
        type_name = get_account_type_name(acc_type)
        lines.append(f"\n{type_name}:")
        
        for acc in accs:
            balance = format_currency(acc['current_balance'])
            if acc_type == 'credit_card':
                used = acc['credit_limit'] - acc['current_balance']
                available = format_currency(acc['current_balance'])
                lines.append(f"  {acc['name']}: 可用 {available} / 额度 {format_currency(acc['credit_limit'])}")
            else:
                lines.append(f"  {acc['name']}: {balance}")
    
    return '\n'.join(lines)


def format_account_detail_report(data: Dict) -> str:
    """格式化账户详情报表"""
    acc = data['account']
    transactions = data.get('transactions', [])
    
    lines = []
    lines.append(f"账户详情: {acc['name']}")
    lines.append("=" * 60)
    lines.append(f"类型: {get_account_type_name(acc['account_type'])}")
    lines.append(f"初始余额: {format_currency(acc['initial_balance'])}")
    lines.append(f"当前余额: {format_currency(acc['current_balance'])}")
    
    if acc['account_type'] == 'credit_card':
        lines.append(f"固定额度: {format_currency(acc['credit_limit'])}")
        lines.append(f"剩余额度: {format_currency(acc['current_balance'])}")
        lines.append(f"已用额度: {format_currency(acc['credit_limit'] - acc['current_balance'])}")
    
    lines.append(f"\n收入笔数: {data.get('income_count', 0)} / {format_currency(data.get('total_income', 0))}")
    lines.append(f"支出笔数: {data.get('expense_count', 0)} / {format_currency(data.get('total_expense', 0))}")
    
    if transactions:
        lines.append("\n最近流水:")
        lines.append("-" * 60)
        for t in transactions[:20]:
            date = t['transaction_date']
            amount = format_currency(t['amount'])
            type_icon = '+' if t['transaction_type'] == 'income' else '-'
            
            # 构建描述
            desc_parts = []
            if t['merchant']:
                desc_parts.append(t['merchant'])
            if t['category'] != 'transfer':
                desc_parts.append(get_category_name(t['category']))
            else:
                desc_parts.append(f"{t['transfer_desc']}{t['counterparty']}" if t.get('counterparty') else '转账')
            
            desc = ' - '.join(desc_parts) if desc_parts else t['note'] or ''
            lines.append(f"{date} {type_icon}{amount} {desc}")
    
    return '\n'.join(lines)


def format_monthly_report(data: Dict) -> str:
    """格式化月度报表"""
    year = data['year']
    month = data['month']
    total_income = data['total_income']
    total_expense = data['total_expense']
    category_stats = data.get('category_stats', [])
    
    lines = []
    lines.append(f"{year}年{month}月 月度报表")
    lines.append("=" * 60)
    lines.append(f"收入: {format_currency(total_income)} ({data.get('income_count', 0)}笔)")
    lines.append(f"支出: {format_currency(total_expense)} ({data.get('expense_count', 0)}笔)")
    lines.append(f"结余: {format_currency(total_income - total_expense)}")
    
    if category_stats:
        lines.append("\n支出分类:")
        for cat in category_stats[:10]:
            cat_name = get_category_name(cat['category'])
            pct = (cat['total'] / total_expense * 100) if total_expense else 0
            lines.append(f"  {cat_name}: {format_currency(cat['total'])} ({pct:.1f}%)")
    
    return '\n'.join(lines)


def format_daily_report(data: Dict) -> str:
    """格式化日报"""
    lines = []
    lines.append(f"日报: {data['date']}")
    lines.append("=" * 40)
    lines.append(f"收入: {format_currency(data['total_income'])} ({data['income_count']}笔)")
    lines.append(f"支出: {format_currency(data['total_expense'])} ({data['expense_count']}笔)")
    lines.append(f"净流量: {format_currency(data['net'])}")
    return '\n'.join(lines)


def format_category_report(data: Dict) -> str:
    """格式化分类报表"""
    lines = []
    lines.append("分类统计报表")
    lines.append("=" * 40)
    
    total = sum(item['total'] for item in data)
    
    for item in data:
        cat_name = get_category_name(item['category'])
        pct = (item['total'] / total * 100) if total else 0
        lines.append(f"{cat_name}: {format_currency(item['total'])} ({pct:.1f}%) - {item['count']}笔")
    
    return '\n'.join(lines)


def format_transactions_report(transactions: List[Dict]) -> str:
    """格式化收支记录列表"""
    lines = []
    lines.append("收支记录")
    lines.append("=" * 70)
    lines.append(f"{'日期':<12} {'类型':<6} {'金额':>12} {'商户':<15} {'分类':<8} {'备注'}")
    lines.append("-" * 70)
    
    for t in transactions:
        date = t['transaction_date']
        type_text = '收入' if t['transaction_type'] == 'income' else '支出'
        amount = format_currency(t['amount'])
        merchant = (t['merchant'] or '')[:12]
        category = get_category_name(t.get('category', 'other'))
        note = (t['note'] or '')[:15]
        
        lines.append(f"{date:<12} {type_text:<6} {amount:>12} {merchant:<15} {category:<8} {note}")
    
    return '\n'.join(lines)


def format_transfers_report(transfers: List[Dict]) -> str:
    """格式化转账记录"""
    lines = []
    lines.append("转账记录")
    lines.append("=" * 70)
    lines.append(f"{'时间':<20} {'金额':>12} {'转出':<15} {'转入':<15} {'备注'}")
    lines.append("-" * 70)
    
    for tr in transfers:
        time_str = tr['transfer_time'][:19]
        amount = format_currency(tr['amount'])
        from_acc = tr['from_account_name'][:13]
        to_acc = tr['to_account_name'][:13]
        note = (tr['note'] or '')[:15]
        
        lines.append(f"{time_str:<20} {amount:>12} {from_acc:<15} {to_acc:<15} {note}")
    
    return '\n'.join(lines)


# ==================== 便捷统计函数 ====================

def get_monthly_report_text(year: int = None, month: int = None) -> str:
    """获取月度报表文本"""
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month
    
    date_from = f'{year}-{month:02d}-01'
    if month == 12:
        date_to = f'{year + 1}-01-01'
    else:
        date_to = f'{year}-{month + 1:02d}-01'
    
    total_income = get_total_by_type('income', date_from, date_to)
    total_expense = get_total_by_type('expense', date_from, date_to)
    
    # 获取笔数
    income_list = get_transactions(date_from=date_from, date_to=date_to, transaction_type='income')
    expense_list = get_transactions(date_from=date_from, date_to=date_to, transaction_type='expense')
    
    category_stats = get_total_by_category('expense', date_from, date_to)
    
    data = {
        'year': year,
        'month': month,
        'total_income': total_income,
        'total_expense': total_expense,
        'income_count': len(income_list),
        'expense_count': len(expense_list),
        'category_stats': category_stats
    }
    
    return format_report_text(data, 'monthly')


def get_account_balance_report_text() -> str:
    """获取账户余额报表文本"""
    accounts = get_accounts()
    return format_report_text(accounts, 'account')


def get_account_detail_report_text(account_id: int) -> str:
    """获取账户详情报表文本"""
    acc = next((a for a in get_accounts() if a['id'] == account_id), None)
    if not acc:
        return "账户不存在"
    
    # 获取账户统计
    stats = get_total_by_account()
    stat = next((s for s in stats if s['account_id'] == account_id), None)
    
    # 获取最近流水
    transactions = get_account_transactions_with_transfers(account_id, limit=50)
    
    data = {
        'account': acc,
        'transactions': transactions
    }
    
    if stat:
        data.update({
            'total_income': stat['total_income'],
            'total_expense': stat['total_expense'],
            'income_count': stat['income_count'],
            'expense_count': stat['expense_count']
        })
    
    return format_report_text(data, 'account_detail')


def get_assets_report_text() -> str:
    """获取资产汇总报表文本"""
    from scripts.database import get_financial_summary
    data = get_financial_summary()
    return format_report_text(data, 'assets')


def get_category_report_text(transaction_type: str, date_from: str = None, date_to: str = None) -> str:
    """获取分类统计报表文本"""
    data = get_total_by_category(transaction_type, date_from, date_to)
    return format_report_text(data, 'category')


if __name__ == '__main__':
    print("统计报表测试")
    print("-" * 40)
    print(get_account_balance_report_text())
