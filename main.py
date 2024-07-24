# main.py
from sms_service import request_phone_num, get_code
import time
from accounts import get_accounts
from login import Google
from sendmsg import test_send_message,send_message,select_message_nav,is_msg_send_success
import json
from utils import get_date,read_json,write_json,record_message_info,read_message_record,update_local_info

if __name__ == "__main__":
    # main.py
    account_path = './nodejs-demo/file/account_info'
    accounts = get_accounts()
    if not accounts:
        print("没有获取到账号信息")
        exit()
    # for account in accounts:
    #     print(f"Processing account with UserName: {account['userName']} and Password: {account['password']}")
    #     # 在这里添加你希望对每个账号进行的操作
    import random
    first_account = accounts[random.randint(0,len(accounts)-1)]
    # 配置和初始化
    EMAIL = first_account['userName']
    PASSWORD = first_account['password']
    # EMAIL = '...'
    # PASSWORD = '...'
    MESSAGE_CONTENT = "Hello, this is a test message."
    print(EMAIL)
    print(PASSWORD)
    # 获取电话号码
    phone_data = request_phone_num()
    if phone_data:
        phone_num, request_id = phone_data[2], phone_data[1]
        print(f"获取到的电话号码: {phone_num}")
        google = Google()
        google.login(EMAIL, PASSWORD)
        # 发送消息
        send_message(phone_num, MESSAGE_CONTENT)
        # 获取验证码
        start_time = time.time()
        code = get_code(request_id, start_time)
        if code != -1:
            print(f"Received code: {code}")
        else:
            print("验证码获取超时")

        # 关闭浏览器
        google.close_browser()
    else:
        print("Failed to get phone number.")
 