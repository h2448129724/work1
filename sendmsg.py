from sms_service import request_phone_num, get_code
import time
from selenium.webdriver.support.ui import WebDriverWait
from login import Google
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
def test_send_message(driver):
    message = {"phone": "9417953734", "message": "it is so hot today!!"}
    send_message(driver, message)

def send_message(driver, message):
    message_nav = select_message_nav(driver)
    if message_nav:
        print('获取消息导航按钮成功')
        had_msg = None
        try:
            had_msg = get_visible_elements(driver, 'xpath', '//a[contains(@aria-label,"Messages:")]', 5000)
        except Exception as e:
            print(e)

        if had_msg:
            print('含有未读消息')
            return 'hadUnreadMsg'
        else:
            print('不含有未读消息')
            try:
                loading_view = driver.find_element(By.CLASS_NAME, 'gvMessagingView-loading')
                if loading_view:
                    WebDriverWait(driver, 30).until(EC.invisibility_of_element(loading_view))
            except Exception as e:
                print(e)
                js_code = "var overlay = document.querySelector('.gvMessagingView-loading'); if (overlay) { overlay.style.display = 'none'; }"
                driver.execute_script(js_code)
                time.sleep(1)

            conversation_list = get_visible_element(driver, 'xpath', '//*[local-name()="gv-conversation-list"]')
            if conversation_list:
                print('开始获取新建消息按钮')
                add_message_btn = get_visible_element(driver, 'class', 'gvMessagingView-actionButton')
                if add_message_btn:
                    print('获取新建消息按钮成功')
                    time.sleep(2)
                    add_message_btn.click()
                    print('开始获取号码输入框')
                    element = get_visible_element(driver, 'class', 'cdk-overlay-pane')
                    if element:
                        print('获取到了弹窗')
                        time.sleep(2)
                        js_code = "var overlay = document.querySelector('.cdk-overlay-pane'); if (overlay) { overlay.style.display = 'none'; }"
                        driver.execute_script(js_code)
                        time.sleep(2)
                    else:
                        print('没有获取到弹窗')

                    input_div = get_visible_element(driver, 'class', 'input-field')
                    if input_div:
                        number_input = input_div.find_element(By.TAG_NAME, 'input')
                        if number_input:
                            print('获取号码输入框成功')
                            time.sleep(1)
                            number_input.clear()
                            time.sleep(2)
                            number_input.send_keys(message["phone"])
                            number_input.send_keys(',')
                            number_input.send_keys(Keys.ESCAPE)
                            time.sleep(2)
                            try:
                                had_msg = get_visible_elements(driver, 'xpath', '//a[contains(@aria-label,"Messages:")]', 1000)
                                if had_msg:
                                    print('含有未读消息')
                                    return 'hadUnreadMsg'
                            except Exception as e:
                                print(e)

                            delete_icon = get_visible_elements(driver, 'class', 'mat-mdc-chip-remove')
                            if delete_icon and len(delete_icon) > 0:
                                print('开始获取内容输入框')
                                message_input = get_visible_element(driver, 'class', 'message-input')
                                if message_input:
                                    print('获取内容输入框成功')
                                    message_input.click()
                                    time.sleep(1)
                                    message_input.clear()
                                    time.sleep(1)
                                    message_input.send_keys(message["message"])
                                    time.sleep(2)
                                    print('开始获取发送按钮')
                                    send_btn = get_visible_element(driver, 'xpath', '//button[@aria-label="Send message"]')
                                    if send_btn:
                                        print('获取发送按钮成功')
                                        send_btn.click()
                                        time.sleep(5)
                                        send_success = is_msg_send_success(driver)
                                        if send_success:
                                            print('发送成功')
                                            return 'sendSuccess'
                                        else:
                                            print('发送失败')
                                    else:
                                        print('获取发送按钮失败')
                        else:
                            print('获取号码输入框失败')
                else:
                    print('获取新建消息按钮失败')
            else:
                print('获取会话列表失败')
    else:
        print('获取消息导航按钮失败')

def select_message_nav(driver):
    try:
        elements = get_visible_elements(driver, 'xpath', '//*[@id="gvPageRoot"]/div[2]/gv-side-panel/mat-sidenav-container/mat-sidenav-content/div/div[2]/gv-side-nav/div/div/mat-nav-list/a[2]')
        if elements:
            if len(elements) > 1:
                elements[1].click()
                return elements[1]
            if len(elements) == 1:
                elements[0].click()
                return elements[0]
    except Exception as e:
        print('获取消息导航按钮失败:', e)

def is_msg_send_success(driver):
    try:
        elements = get_visible_elements(driver, 'class', 'status')
        if elements and len(elements) > 0:
            last_element = elements[-1]
            reg_exp = r'\b\d{1,2}:\d{2}\s+[AP]M\b'
            WebDriverWait(driver, 10).until(EC.text_matches(last_element, re.compile(reg_exp)))
            text = last_element.text
            print('发送时间为:', text)
            return True
    except Exception as e:
        print('is_msg_send_success', e)

def get_visible_elements(driver, by, identifier, wait_time=30):
    try:
        if by == 'xpath':
            elements = WebDriverWait(driver, wait_time).until(
                EC.presence_of_all_elements_located((By.XPATH, identifier))
            )
        elif by == 'class':
            elements = WebDriverWait(driver, wait_time).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, identifier))
            )
        return elements
    except Exception as e:
        print(f'获取元素失败: {identifier}', e)
        return []

def get_visible_element(driver, by, identifier, wait_time=30):
    try:
        if by == 'xpath':
            element = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, identifier))
            )
        elif by == 'class':
            element = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.CLASS_NAME, identifier))
            )
        return element
    except Exception as e:
        print(f'获取元素失败: {identifier}', e)
        return None

if __name__ == "__main__":
    driver = Google()
    test_send_message(driver)
