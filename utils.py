import time
import json
def get_date():
    return time.strftime("%Y-%m-%d", time.localtime())

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def record_message_info(group_name, message_info):
    date_str = get_date()
    message_record_file_path = f'./file/message_info/{date_str}.json'
    write_json(message_record_file_path, message_info)

def read_message_record(group_name):
    date_str = get_date()
    message_record_file_path = f'./file/message_info/{date_str}.json'
    return read_json(message_record_file_path)

def update_local_info(cur_group_window_info_list, pre_window_info_list, cur_group_window_list_file, pre_window_list_file):
    for account_info in cur_group_window_info_list:
        element_index = next((index for (index, d) in enumerate(pre_window_info_list) if d["id"] == account_info["id"]), None)
        if element_index is not None:
            pre_window_info_list[element_index] = account_info
        else:
            pre_window_info_list.append(account_info)
    write_json(cur_group_window_list_file, cur_group_window_info_list)
    write_json(pre_window_list_file, pre_window_info_list)