from undetected_chromedriver import Chrome
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback

class Google:
    def __init__(self) -> None:
        self.url    = 'https://accounts.google.com/ServiceLogin'
        driver_path = "chromedriver.exe"
        self.driver = Chrome(driver_executable_path=driver_path); self.driver.get(self.url)
        self.time   = 10
    
    def login(self, email, password):
        try:
            sleep(2)
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, 'identifier'))).send_keys(email)
            sleep(2)
            self.driver.find_element(By.ID, 'identifierNext').click()
            
            # 等待密码输入框出现
            password_input = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, 'Passwd')))
            password_input.send_keys(password)
            sleep(1)
            
            # 点击下一步按钮
            password_next_button = self.driver.find_element(By.ID, 'passwordNext')
            password_next_button.click()
            
            # 等待跳转到Google Account页面
            WebDriverWait(self.driver, 10).until(EC.title_contains('Google Account'))
            print("已登录成功！！！！")
            self.to_gv_tab()
        except Exception as e:
            print('登录时发生错误:', e)
            print(traceback.format_exc())
            try:
                WebDriverWait(self.driver, 5).until(EC.title_contains('Google Account'))
                print("已登录成功！！！！")
                self.to_gv_tab()
            except Exception as err:
                print("登录失败！！！", err)

    def code(self):
        sleep(self.time)                                                                                  
    def to_gv_tab(self):
        try:
            all_handles = self.driver.window_handles
            gv_handle = None
            for handle in all_handles:
                self.driver.switch_to.window(handle)
                if 'Voice - Calls' in self.driver.title:
                    gv_handle = handle
                    break
            if not gv_handle:
                sleep(1)
                self.driver.execute_script("window.open('https://voice.google.com/', '_blank');")
                sleep(2)
                self.to_gv_tab()
            else:
                print('成功跳转到Voice-Calls页面')
        except Exception as e:
            print('跳转GV标签时发生错误:', e)
            print(traceback.format_exc())
    def close_browser(self):
        try:
            self.driver.quit()
            print("浏览器已关闭")
        except Exception as e:
            print("关闭浏览器时发生错误:", e)


if __name__ == "__main__":
    #  ---------- EDIT ----------
    email = 'HolshueUmbrell@gmail.com' 
    password = 'apyzwgbyod' 
    #  ---------- EDIT ----------                                                                                                                                                         
    
    google = Google()
    google.login(email, password)
