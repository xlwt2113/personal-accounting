# -*- coding: utf-8 -*-
"""
个人记账系统统一命令行入口
Agent 通过命令行参数调用此脚本执行所有操作，无需自己写临时脚本。

用法：
  python scripts/cli.py report daily              # 日报
  python scripts/cli.py report weekly             # 周报
  python scripts/cli.py report monthly            # 月报
  python scripts/cli.py report yearly             # 年报
  python scripts/cli.py report monthly --year 2024 --month 3  # 指定月份
  python scripts/cli.py summary                   # 财务汇总
  python scripts/cli.py accounts                  # 账户列表
  python scripts/cli.py account-detail <id>       # 账户流水
  python scripts/cli.py categories expense        # 支出分类统计
  python scripts/cli.py categories income         # 收入分类统计
  python scripts/cli.py transactions              # 交易记录列表
  python scripts/cli.py transfers                 # 转账记录列表
  python scripts/cli.py add-transaction <json>    # 添加交易记录
  python scripts/cli.py add-transfer <json>       # 添加转账记录
  python scripts/cli.py add-account <json>        # 添加账户
  python scripts/cli.py update-transaction <id> <json>  # 更新交易
  python scripts/cli.py delete-transaction <id>   # 删除交易
"""
import sys
import os
import json
import argparse

# Windows 中文编码处理
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 确保路径正确：将项目根目录加入 sys.path，并切换到项目根目录
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROJECT_ROOT)
os.chdir(_PROJECT_ROOT)

from scripts.database import (
    init_database, get_accounts, get_account_by_id, get_account_by_name,
    add_account, add_transaction, add_transfer, get_transactions, get_transfers,
    update_transaction, delete_transaction
)
from scripts.statistics import (
    get_assets_report_text,
    get_account_balance_report_text,
    get_account_detail_report_text,
    get_monthly_report_text,
    get_category_report_text,
    get_daily_report_text,
    get_weekly_report_text,
    get_monthly_detailed_report_text,
    get_yearly_report_text,
    format_transactions_report,
    format_transfers_report,
)

init_database()


def cmd_report(args):
    """生成日报/周报/月报/年报"""
    if args.type == 'daily':
        print(get_daily_report_text())
    elif args.type == 'weekly':
        print(get_weekly_report_text())
    elif args.type == 'monthly':
        print(get_monthly_detailed_report_text(args.year, args.month))
    elif args.type == 'yearly':
        print(get_yearly_report_text(args.year))
    else:
        print(f"未知报表类型: {args.type}", file=sys.stderr)
        sys.exit(1)


def cmd_summary(args):
    """财务汇总"""
    print(get_assets_report_text())


def cmd_accounts(args):
    """账户列表"""
    print(get_account_balance_report_text())


def cmd_account_detail(args):
    """账户流水"""
    print(get_account_detail_report_text(args.account_id))


def cmd_categories(args):
    """分类统计"""
    print(get_category_report_text(args.transaction_type))


def cmd_transactions(args):
    """交易记录列表"""
    txs = get_transactions(
        account_id=args.account_id,
        transaction_type=args.type,
        limit=args.limit,
        offset=args.offset,
    )
    print(format_transactions_report(txs))


def cmd_transfers(args):
    """转账记录列表"""
    transfers = get_transfers(limit=args.limit)
    print(format_transfers_report(transfers))


def _load_json(args):
    """从 --file 或位置参数加载 JSON 数据"""
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return json.loads(args.json_data)


def cmd_add_transaction(args):
    """添加交易记录"""
    data = _load_json(args)
    tid = add_transaction(**data)
    print(json.dumps({"id": tid, "success": True}, ensure_ascii=False))


def cmd_add_transfer(args):
    """添加转账记录"""
    data = _load_json(args)
    transfer_id, from_tid, to_tid = add_transfer(**data)
    print(json.dumps({
        "transfer_id": transfer_id,
        "from_transaction_id": from_tid,
        "to_transaction_id": to_tid,
        "success": True,
    }, ensure_ascii=False))


def cmd_add_account(args):
    """添加账户"""
    data = _load_json(args)
    acc_id = add_account(**data)
    print(json.dumps({"id": acc_id, "success": True}, ensure_ascii=False))


def cmd_update_transaction(args):
    """更新交易记录"""
    data = _load_json(args)
    ok = update_transaction(args.transaction_id, **data)
    print(json.dumps({"success": ok}, ensure_ascii=False))


def cmd_delete_transaction(args):
    """删除交易记录"""
    ok = delete_transaction(args.transaction_id)
    print(json.dumps({"success": ok}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description='个人记账系统CLI')
    sub = parser.add_subparsers(dest='command', required=True)

    # report 命令
    p_report = sub.add_parser('report', help='生成报表')
    p_report.add_argument('type', choices=['daily', 'weekly', 'monthly', 'yearly'])
    p_report.add_argument('--year', type=int)
    p_report.add_argument('--month', type=int)
    p_report.set_defaults(func=cmd_report)

    # summary 命令
    p_summary = sub.add_parser('summary', help='财务汇总')
    p_summary.set_defaults(func=cmd_summary)

    # accounts 命令
    p_accounts = sub.add_parser('accounts', help='账户列表')
    p_accounts.set_defaults(func=cmd_accounts)

    # account-detail 命令
    p_detail = sub.add_parser('account-detail', help='账户流水')
    p_detail.add_argument('account_id', type=int)
    p_detail.set_defaults(func=cmd_account_detail)

    # categories 命令
    p_cat = sub.add_parser('categories', help='分类统计')
    p_cat.add_argument('transaction_type', choices=['expense', 'income'])
    p_cat.set_defaults(func=cmd_categories)

    # transactions 命令
    p_tx = sub.add_parser('transactions', help='交易记录列表')
    p_tx.add_argument('--account-id', type=int)
    p_tx.add_argument('--type', choices=['expense', 'income'])
    p_tx.add_argument('--limit', type=int, default=100)
    p_tx.add_argument('--offset', type=int, default=0)
    p_tx.set_defaults(func=cmd_transactions)

    # transfers 命令
    p_tr = sub.add_parser('transfers', help='转账记录列表')
    p_tr.add_argument('--limit', type=int, default=100)
    p_tr.set_defaults(func=cmd_transfers)

    # add-transaction 命令
    p_atx = sub.add_parser('add-transaction', help='添加交易记录')
    p_atx.add_argument('json_data', nargs='?', help='JSON格式的交易数据（与--file二选一）')
    p_atx.add_argument('--file', '-f', help='从JSON文件读取数据')
    p_atx.set_defaults(func=cmd_add_transaction)

    # add-transfer 命令
    p_atr = sub.add_parser('add-transfer', help='添加转账记录')
    p_atr.add_argument('json_data', nargs='?', help='JSON格式的转账数据（与--file二选一）')
    p_atr.add_argument('--file', '-f', help='从JSON文件读取数据')
    p_atr.set_defaults(func=cmd_add_transfer)

    # add-account 命令
    p_aac = sub.add_parser('add-account', help='添加账户')
    p_aac.add_argument('json_data', nargs='?', help='JSON格式的账户数据（与--file二选一）')
    p_aac.add_argument('--file', '-f', help='从JSON文件读取数据')
    p_aac.set_defaults(func=cmd_add_account)

    # update-transaction 命令
    p_utx = sub.add_parser('update-transaction', help='更新交易记录')
    p_utx.add_argument('transaction_id', type=int)
    p_utx.add_argument('json_data', nargs='?', help='JSON格式的更新字段（与--file二选一）')
    p_utx.add_argument('--file', '-f', help='从JSON文件读取数据')
    p_utx.set_defaults(func=cmd_update_transaction)

    # delete-transaction 命令
    p_dtx = sub.add_parser('delete-transaction', help='删除交易记录')
    p_dtx.add_argument('transaction_id', type=int)
    p_dtx.set_defaults(func=cmd_delete_transaction)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
