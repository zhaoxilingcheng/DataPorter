from random import random

from base_spider import BaseSpider
from selenium import webdriver,common
import time
from models import *
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

class JdSpider(BaseSpider):

    def __init__(self, sleep_time: int = 3, item_id: int = 100012043978):
        super().__init__(base_url='http://jd.com', login_url='https://passport.jd.com/new/login.aspx',
                         verify_url='https://www.jd.com/', sleep_time=sleep_time)
        self.item_id = item_id
        self.item_url = f'https://item.jd.com/{item_id}.html'
        self.kill_url = f'https://marathon.jd.com/seckill/seckill.action?skuId={item_id}&num=1'
        # //*[@id="app"]/div/div[2]/div/div[5]/div[3]/div[2]/div/div/div/button

    def sub_login(self):
        pass

    def kill(self):
        self.driver.get(self.kill_url)
        # 提交订单
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[5]/div[3]/div[2]/div/div/div/button').click()

    def run(self):
        tag = 1
        while True:
            self.driver.get(self.item_url)
            first_result = self.wait.until(presence_of_element_located((By.ID, "btn-reservation")))
            textContent = first_result.get_attribute("textContent")
            if (textContent == '等待抢购'):
                print('还没开始，等待抢购！{}'.format(tag))
            elif (textContent == '立即抢购'):
                try:
                    print('终于开始了，立即抢购!')
                    first_result.click()
                    first_result = self.wait.until(presence_of_element_located((By.CLASS_NAME, "checkout-submit")))
                    first_result.click()
                    print("提交订单！")
                    time.sleep(100)
                    break
                except common.exceptions.TimeoutException as e:
                    print('没赶上，明天再来吧！')
                    break
            time.sleep(random.randint(1, 3) * 0.01)
            tag += 1
            if (tag > 300):
                break

if __name__ == '__main__':
    dd = JdSpider().login_by_cookies()
    dd.to_csv()
    dd.save_cookie()

    dd.close()

