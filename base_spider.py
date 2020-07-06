from abc import ABC, abstractmethod
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas


class BaseSpider(ABC):

    def __init__(self, login_url: str, verify_url: str):
        self.login_url = login_url
        self.verify_url = verify_url
        self.driver = self.get_chrome_driver()
        self.is_login = False
        self.data_list = []

    @staticmethod
    def get_chrome_driver() -> webdriver:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        # options.add_argument('--headless')  # 无头参数
        options.add_argument('--disable-gpu')
        # 關閉瀏覽器左上角通知提示
        prefs = {
            'profile.default_content_setting_values':
                {
                    'notifications': 2
                }
        }
        options.add_experimental_option('prefs', prefs)
        # 關閉'chrome目前受到自動測試軟體控制'的提示
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        driver.maximize_window()
        driver.implicitly_wait(10)
        return driver

    def login(self):
        driver = self.driver
        driver.get(self.login_url)
        self.sub_login()
        self.verify_login()

    @abstractmethod
    def sub_login(self):
        pass

    def verify_login(self):
        wait_time = 0
        while True and not self.is_login:
            print(f'登录中...等待时间为{wait_time}s')
            time.sleep(5)
            wait_time = wait_time + 5
            if self.verify_url in self.driver.current_url and not self.driver.current_url == self.login_url:
                print('登录成功')
                self.is_login = True
                break
            if wait_time >= 300:
                raise Exception('登录失败')
        return self.is_login

    def close(self):
        self.driver.close()
        self.is_login = False

    def to_csv(self):
        if not self.data_list:
            print('数据为空')
            return
        data_list = [i.__dict__ for i in self.data_list]
        df = pandas.DataFrame()
        df = df.append(data_list)
        df.to_csv(self.__class__.__name__ + '.csv')
