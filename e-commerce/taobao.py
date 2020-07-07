from base_spider import BaseSpider
from numpy import *
import string
import time
# import re
# import json


class TaoBaoSpider(BaseSpider):

    def run(self):
        pass

    def __init__(self):
        super().__init__(base_url='https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm',
                         login_url='https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fbuyertrade'
                                   '.taobao.com%2Ftrade%2Fitemlist%2Flist_bought_items.htm',
                         verify_url='https://buyertrade.taobao.com/')

    def sub_login(self):
        pass

    @property
    def get_order_list(self):
        driver = self.driver
        time.sleep(3)
        # 获取 总页数
        lis = driver.find_element_by_xpath('//*[@id="tp-bought-root"]/div[19]/div[2]/ul').find_elements_by_tag_name('li')
        for index in range(len(lis)):
            if lis[index].get_attribute('title') in ['上一页', '下一页']:
                continue
            page = lis[index].text
            time.sleep(10)
            # TODO 这块 加了 等待时间 有时也会 弹窗 让休息一会(随机的 不是每次都出现) 弹窗中有 滑动验证, 手动验证失效(疑似有检测)
            lis[index].click()
            print('当前页码::' + page)
            time.sleep(5)
            # 获取商品列表
            self.get_goods_list()
        return self

    # 获取商品列表
    def get_goods_list(self):
        driver = self.driver
        divs = driver.find_element_by_xpath('//*[@id="tp-bought-root"]').find_elements_by_tag_name('div')
        for index in range(len(divs)):
            if index < 4:
                continue
            try:
                # TODO 这个地方存在缺陷:  一个订单对应多个商品 目前只能 拿到第一个商品信息
                # # 交易时间
                var = driver.find_element_by_xpath(
                    '//*[@id="tp-bought-root"]/div[' + str(index) + ']/div/table/tbody[1]/tr/td[1]/label/span[2]').text
                print('交易时间:' + var)
                # # 店铺名称
                var = driver.find_element_by_xpath(
                    '//*[@id="tp-bought-root"]/div[' + str(index) + ']/div/table/tbody[1]/tr/td[2]/span/a').text
                print('店铺名称:' + var)
                # # 商品链接
                var = driver.find_element_by_xpath(
                    '//*[@id="tp-bought-root"]/div[' + str(index) + ']/div/table/tbody[2]/tr[1]/td[1]/div/div[2]/p[1]/a[1]').text
                print('商品链接:' + var)
                # # 商品名称
                var = driver.find_element_by_xpath(
                    '//*[@id="tp-bought-root"]/div[' + str(
                        index) + ']/div/table/tbody[2]/tr/td[1]/div/div[2]/p[1]/a/span[2]').text
                print('商品名称:' + var)

                # # 订单号
                var = driver.find_element_by_xpath(
                    '//*[@id="tp-bought-root"]/div[' + str(index) + ']/div/table/tbody[1]/tr/td[1]/span/span[3]').text
                print('订单号:' + var)
                # # 实付款
                var = driver.find_element_by_xpath(
                    '//*[@id="tp-bought-root"]/div[' + str(
                        index) + ']/div/table/tbody[2]/tr/td[5]/div/div[1]/p/strong/span[2]').text
                print('实付款:' + var)
                # # 交易状态
                var = driver.find_element_by_xpath(
                    '//*[@id="tp-bought-root"]/div[' + str(index) + ']/div/table/tbody[2]/tr/td[6]/div/p/span').text
                print('交易状态:' + var)
                # # 订单详情
                # TODO [未实现] 这块 统一 获取 https://buyertrade.taobao.com/trade/detail/trade_item_detail.htm
                var = driver.find_element_by_xpath(
                    '//*[@id="viewDetail"]').get_attribute('href')
                print('订单详情:' + var)
                # self.get_goods_info(var)
            except:
                break

    # 获取商品详情
    def get_goods_info(self, url):
        driver = self.driver
        driver.get(url)
        try:
            var = driver.find_element_by_xpath('//*[@id="J_trade_imfor"]/div/ul/li[1]/div[2]/span').text
            print('收货地址：' + var)
            var = driver.find_element_by_xpath('//*[@id="J_trade_detail"]/div/ul/li/div/span[1]').text
            print('运送方式：' + var)
            var = driver.find_element_by_xpath('//*[@id="J_trade_detail"]/div/ul/li/div/span[3]').text
            print('运单号：' + var)

        except:
            var = driver.find_element_by_xpath('//*[@id="detail-panel"]/div/div[5]/div/div/div/div/div[1]/div[1]/dl[1]/dd').text
            print('收货地址：' + var)
            var = driver.find_element_by_xpath('//*[@id="detail-panel"]/div/div[5]/div/div/div/div/div[1]/div[1]/dl[3]/dd').text
            print('运送方式：' + var)


if __name__ == '__main__':
    dd = TaoBaoSpider()
    dd.login_by_cookies()
    dd.get_order_list()
    # TODO 保存 conkie 无作用
    # #dd.save_cookie()
    # TODO[未实现] 生成文件未实现
    # dd.to_csv()
    dd.close()
