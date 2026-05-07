# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from database import get_account_by_name, calculate_account_balance

wechat = get_account_by_name("微信零钱")
if wechat:
    balance = calculate_account_balance(wechat['id'])
    print(f"微信零钱余额：{balance:.2f}")
else:
    print("未找到微信零钱账户")