from base_spider import BaseSpider
import time
import re
import json

class JdSpider(BaseSpider):

    def __init__(self):
        super().__init__(login_url='https://passport.jd.com/new/login.aspx', verify_url='https://www.jd.com/')

    def sub_login(self):
        pass

    def get_order_list(self):

        for year in range(2015,2021):
            self.driver.get(f'https://order.jd.com/center/list.action?search=0&d={year}&s=4096')

            for i in range(1,11):
                try:
                    order_number=self.driver.find_element_by_xpath('//table[@class="td-void order-tb"]/tbody[{}]'.format(str(i))).get_attribute('id').replace('tb-','')  # 订单ｉｄ
                    timedate=self.driver.find_element_by_xpath('//table[@class="td-void order-tb"]/tbody[{}]/tr[2]/td/span[2]'.format(str(i))).text  # 购买时间
                    shop_name=self.driver.find_element_by_xpath('//table[@class="td-void order-tb"]/tbody[{}]/tr[2]/td/div/span[1]/a[1]'.format(str(i))).text #店铺名
                    trade_name=self.driver.find_element_by_xpath('//table[@class="td-void order-tb"]/tbody[{}]/tr[3]/td/div/div[2]/div[1]/a'.format(str(i))).text  # 商品名
                    goods_number=self.driver.find_element_by_xpath('//table[@class="td-void order-tb"]/tbody[{}]/tr[3]/td[1]/div[2]'.format(str(i))).text # 购买数量
                    addressee=self.driver.find_element_by_xpath('//table[@class="td-void order-tb"]/tbody[{}]/tr[3]/td[2]/div/span'.format(str(i))).text # 收件人
                    # '//table[@class="td-void order-tb"]/tbody[2]/tr[3]/td[2]//div[@class="pc"]'

                    money=self.driver.find_element_by_xpath('//table[@class="td-void order-tb"]/tbody[{}]/tr[3]/td[3]/div/span[1]'.format(str(i))).text.replace('总额 ','') # 金额
                    pay_mode=self.driver.find_element_by_xpath('//table[@class="td-void order-tb"]/tbody[{}]/tr[3]/td[3]/div/span[2]'.format(str(i))).text # 支付方式
                    status=self.driver.find_element_by_xpath('//table[@class="td-void order-tb"]/tbody[{}]/tr[3]/td[4]/div/span'.format(str(i))).text

                    print(order_number,timedate,shop_name,trade_name,goods_number,addressee,money,pay_mode,status)

                except:
                    print(f'{year}年共查询到{i-1}条数据！')
                    break

if __name__ == '__main__':
    dd = JdSpider()
    dd.login()
    # print(dd.get_order_list().data_list)
    dd.get_order_list()
    dd.close()

