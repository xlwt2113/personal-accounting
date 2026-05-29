# -*- coding: utf-8 -*-
"""
Personal Accounting - 图片解析模块
通过 AI 多模态能力解析账单截图
"""
from typing import Dict, Optional
from datetime import datetime

# 支出分类关键词映射
EXPENSE_KEYWORDS = {
    'food': ['餐饮', '美食', '吃饭', '午餐', '晚餐', '早餐', '外卖', '快餐', '餐厅', '饭店', '美团', '饿了么', '星巴克', '瑞幸', '麦当劳', '肯德基', '必胜客'],
    'transportation': ['交通', '打车', '地铁', '公交', '停车', '加油', '滴滴', '高德', '出租车', '火车票', '飞机票'],
    'shopping': ['购物', '淘宝', '天猫', '京东', '拼多多', '唯品会', '苏宁', '超市', '便利店', '商场'],
    'entertainment': ['娱乐', '电影', 'KTV', '游戏', '健身', '美容', '美发', '按摩', '旅游', '门票'],
    'bills': ['账单', '水电', '燃气', '话费', '宽带', '物业', '房租'],
    'healthcare': ['医疗', '医院', '药店', '体检', '保险'],
    'education': ['教育', '培训', '学费', '书籍', '文具', '课外班'],
    'housing': ['住房', '装修', '家具', '家纺'],
    'investment': ['投资', '理财', '基金', '股票'],
}

# 收入分类关键词映射
INCOME_KEYWORDS = {
    'salary': ['工资', '薪资', '薪酬', '发薪', '底薪', '奖金'],
    'bonus': ['奖金', '年终奖', '绩效', '分红'],
    'investment': ['投资', '收益', '分红', '利息', '股息'],
    'gift': ['红包', '礼金', '压岁钱'],
    'refund': ['退款', '退货退款', '返现', '返利'],
}

# 商家类型识别
MERCHANT_PATTERNS = {
    'wechat': ['微信支付', '微信红包', '微信转账'],
    'alipay': ['支付宝', '蚂蚁集团', '余额宝'],
    'bank': ['工商银行', '建设银行', '农业银行', '中国银行', '招商银行', '交通银行', '邮储银行'],
}


def parse_screenshot(image_path: str = None, source: str = None) -> Dict:
    """
    解析账单截图
    
    此函数由 AI Agent 调用，使用多模态能力识别图片内容。
    
    Args:
        image_path: 图片路径（如果已上传到本地）
        source: 来源标识 (wechat/alipay/bank_sms/other)
    
    Returns:
        解析结果字典，包含：
        - amount: 金额
        - transaction_type: income/expense
        - merchant: 商户
        - category: 分类
        - transaction_date: 日期
        - note: 备注
        - source: 来源
        - confidence: 可信度
    """
    # 注意：实际解析由 AI Agent 使用多模态能力完成
    # 此函数定义返回格式和辅助逻辑
    
    return {
        'amount': 0,
        'transaction_type': None,
        'merchant': None,
        'category': None,
        'transaction_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'note': None,
        'source': source,
        'confidence': 0,
        'raw_text': None
    }


def recognize_category(text: str, transaction_type: str) -> str:
    """根据文本内容识别分类"""
    if not text:
        return 'other'
    
    keywords = INCOME_KEYWORDS if transaction_type == 'income' else EXPENSE_KEYWORDS
    
    for category, words in keywords.items():
        for word in words:
            if word in text:
                return category
    
    return 'other'


def recognize_merchant(text: str) -> Optional[str]:
    """从文本中识别商户名称"""
    if not text:
        return None
    
    if '微信支付' in text:
        return '微信支付'
    elif '支付宝' in text:
        return '支付宝'
    elif '美团' in text:
        return '美团'
    elif '京东' in text:
        return '京东'
    elif '淘宝' in text:
        return '淘宝'
    
    return None


def recognize_source(text: str) -> str:
    """识别数据来源"""
    if not text:
        return 'manual'
    
    if '微信' in text:
        return 'wechat'
    elif '支付宝' in text or '余额宝' in text:
        return 'alipay'
    elif any(bank in text for bank in ['银行', '卡号', '账户']):
        return 'bank_sms'
    
    return 'other'


def parse_amount(text: str) -> float:
    """从文本中提取金额"""
    import re
    
    if not text:
        return 0
    
    pattern = r'[¥￥]?\s*(\d+\.?\d*)'
    match = re.search(pattern, text)
    if match:
        try:
            return round(float(match.group(1)), 2)
        except:
            pass
    
    return 0


def format_parsed_result(parsed: Dict, account_name: str = None) -> str:
    """格式化解析结果为可读文本"""
    lines = []
    lines.append("账单解析结果")
    lines.append("=" * 30)
    
    if parsed.get('amount'):
        lines.append(f"金额: ¥{parsed['amount']:.2f}")
    
    if parsed.get('transaction_type'):
        type_text = '收入' if parsed['transaction_type'] == 'income' else '支出'
        lines.append(f"类型: {type_text}")
    
    if parsed.get('merchant'):
        lines.append(f"商户: {parsed['merchant']}")
    
    if parsed.get('category'):
        lines.append(f"分类: {parsed['category']}")
    
    if parsed.get('transaction_date'):
        lines.append(f"日期: {parsed['transaction_date']}")
    
    if parsed.get('note'):
        lines.append(f"备注: {parsed['note']}")
    
    if account_name:
        lines.append(f"账户: {account_name}")
    
    return '\n'.join(lines)


if __name__ == '__main__':
    test_text = "微信支付-麦当劳-午餐-¥45.50"
    amount = parse_amount(test_text)
    print(f"金额: {amount}")
    
    category = recognize_category("麦当劳餐厅", "expense")
    print(f"分类: {category}")


# ==================== 自动创建账户和保存记录 ====================

def parse_and_save_transactions(parsed_records: list) -> dict:
    """
    解析账单并自动创建账户、保存收支记录

    Args:
        parsed_records: 解析出的账单列表，每个元素包含:
            - amount: 金额
            - transaction_type: income/expense
            - source: 来源 (wechat/alipay/bank_sms/other)
            - merchant: 商户（可选）
            - category: 分类（可选）
            - transaction_date: 交易时间，必须为 YYYY-MM-DD HH:MM:SS 格式（可选，未提供则使用当前时间）
            - note: 备注（可选）
            - bank_name: 银行名称（可选，用于银行卡）
            - card_last_four: 卡号后四位（可选，用于银行卡）

    Returns:
        保存结果，包含:
            - total_parsed: 解析的记录数
            - total_saved: 保存的记录数
            - created_accounts: 新创建的账户列表
            - records: 保存的记录详情
    """
    from scripts.database import (
        init_database,
        get_or_create_account_from_parser,
        add_transaction
    )

    init_database()

    saved_records = []
    created_accounts = []

    for record in parsed_records:
        # 构建账户信息
        account_info = {
            'source': record.get('source'),
            'bank_name': record.get('bank_name'),
            'card_last_four': record.get('card_last_four'),
            'account_type': record.get('account_type', 'savings')
        }

        # 获取或创建账户
        account_id, created = get_or_create_account_from_parser(account_info)
        if created:
            # 生成账户名称
            if account_info.get('bank_name') and account_info.get('card_last_four'):
                from scripts.database import format_bank_account_name
                account_name = format_bank_account_name(
                    account_info['bank_name'],
                    account_info['card_last_four'],
                    account_info['account_type']
                )
            elif account_info.get('source') == 'wechat':
                account_name = '微信零钱'
            elif account_info.get('source') == 'alipay':
                account_name = '支付宝'
            else:
                account_name = record.get('source', '未知账户')
            created_accounts.append(account_name)

        # 保存收支记录
        transaction_id = add_transaction(
            amount=record['amount'],
            transaction_type=record['transaction_type'],
            account_id=account_id,
            category=record.get('category', 'other'),
            transaction_date=record.get('transaction_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            merchant=record.get('merchant'),
            note=record.get('note')
        )

        saved_records.append({
            'transaction_id': transaction_id,
            'account_id': account_id,
            'amount': record['amount'],
            'transaction_type': record['transaction_type'],
            'category': record.get('category')
        })

    return {
        'total_parsed': len(parsed_records),
        'total_saved': len(saved_records),
        'created_accounts': created_accounts,
        'records': saved_records
    }
