import json
import os

def get_accounts(directory='./nodejs-demo/file/account_info'):
    accounts = []
    
    # 遍历指定目录下的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for account in data:
                    accounts.append({
                        "userName": account["userName"],
                        "password": account["password"]
                    })
    
    return accounts

if __name__ == "__main__":
    accounts = get_accounts()
    for account in accounts:
        print(f"UserName: {account['userName']}, Password: {account['password']}")
