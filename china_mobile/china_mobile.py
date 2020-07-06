from selenium.common.exceptions import NoAlertPresentException

from base_spider import BaseSpider

import time


# 请求包
# from urllib import request

class ChinaMobileSpider(BaseSpider):

    # 初始化
    def __init__(self):
        super().__init__(login_url='https://login.10086.cn/login.html',
                         verify_url='https://shop.10086.cn/i/?f=home')
        self.data_list = []

    # 登录 页面的 操作 # TODO 这块可以完全交给 用户支配 , 故 这边 不做操作
    def sub_login(self):
        pass

    # 获取订单列表
    def get_order_list(self):
        driver = self.driver

        # 点击个人中心 获取基本信息
        self.driver.find_element_by_id('topA1').click()

        # 详情查询
        driver.find_element_by_xpath('//*[@id="stcnavmenu"]/ul[2]/li/ul/li[4]/a').click()
        # 通话详单
        driver.find_element_by_xpath('//*[@id="switch-data"]/li[2]/a').click()
        time.sleep(1)

        # 按日期 查询
        ul = driver.find_element_by_xpath('//*[@id="month-data"]').find_elements_by_tag_name('li')

        for li in ul:
            li.click()
            time.sleep(1)
            if self.wait_authentication():
                # file_name = li.text
                trs = driver.find_element_by_id('tmpl-data').find_element_by_id('tbody').find_elements_by_tag_name('tr')
                # fp = open(file_name + '.htm', 'w+b')  # 打开一个文本文件
                for tr in trs:
                    tds = tr.find_elements_by_tag_name('td')
                    header = ['起始时间', '通信地点', '通信方式', '对方号码', '通信时长', '通信类型', '套餐优惠', '实收通信费(元)']
                    print('------------')
                    # fp.write('------------'.encode())  # 写入数据
                    for index in range(len(tds)):
                        string = header[index] + ':' + tds[index].text
                        print(string)
                        # fp.write(string.encode())  # 写入数据
                    print('------------')
                    # fp.write('------------'.encode())  # 写入数据
                # fp.close()

    # 等待 用户 认证
    def wait_authentication(self):
        driver = self.driver
        # 等待用户 认证
        flag = True
        # 循环等待元素消失
        while flag:
            # 每 1 秒检查 一次
            time.sleep(1)
            try:
                try:
                    alert = driver.switch_to.alert
                    print(alert.text)
                    alert.accept()  # 点击弹窗中的【确定】
                    continue
                except NoAlertPresentException:
                    pass
                driver.find_element_by_id('undefined')
                print("身份验证弹窗 存在,等待用户认证")
                flag = True
            except Exception:
                print("身份验证弹窗 不存在,人中通过 或 退出")
                return True
                # TODO  认证 按钮 不存在 也可能是取消 认证了

    # 获取基本信息
    def get_basic_information(self):
        # print('当前访问的 url :' + self.driver.current_url)

        # 点击个人中心 获取基本信息
        self.driver.find_element_by_id('topA1').click()

        time.sleep(5)

        # 获取当前页面
        html = self.driver.page_source
        fp = open('test.htm', 'w+b')  # 打开一个文本文件
        fp.write(html.encode())  # 写入数据  bytes和str两种类型转换的函数encode()、decode()即可
        fp.close()  # 关闭文件

        # TODO 这块获取信息可以直接 从 html 中 取  , 然后 封装成固定格式 写入到文件中
        # TODO 获取信息 这块要增加 容错机制  如 个别用户套餐中不包含 流量 , 获取时可能会 导致 拿不到元素
        while True:
            try:
                driver = self.driver
                # 归属地  # TODO 将“下拉列表”保存到项目级词典p按Ctrl+Shift+I打开预览
                dropdownMenu3 = driver.find_element_by_id('dropdownMenu3').text  # 省
                dropdownMenu4 = driver.find_element_by_id('dropdownMenu4').text  # 市

                print('省:', dropdownMenu3)
                print('市:', dropdownMenu4)

                # 我的账户
                stc_balance = driver.find_element_by_id('stc_balance').text  # 可用余额
                # TODO 将“下拉列表”保存到项目级词典p按Ctrl+Shift+I打开预览
                stc_tolbalance = driver.find_element_by_id('stc_tolbalance').text  # 账户总余额
                stc_real = driver.find_element_by_id('stc_real').text  # 当月消费
                stc_point = driver.find_element_by_id('stc_point').text  # 我的积分

                print('可用余额:', stc_balance)
                print('账户总余额:', stc_tolbalance)
                print('当月消费:', stc_real)
                print('我的积分:', stc_point)

                # 套餐信息
                vip = driver.find_element_by_xpath('//*[@id="stc_user_acc"]/ul/li[1]/div/span[2]').text  # 星级
                ktype = driver.find_element_by_id('stc_user_bland').text  # 卡类型
                stc_cur_packages = driver.find_element_by_id('stc_cur_packages').text  # 当前套餐

                print('星级:', vip)
                print('卡类型:', ktype)
                print('当前套餐:', stc_cur_packages)

                # 套餐详情
                voice_details = driver.find_element_by_xpath('//*[@id="stc_packramin"]/div[1]/span[3]').text  # 语音详情
                voice_surplus = driver.find_element_by_xpath('//*[@id="stc_packramin"]/div[1]/span[4]').text  # 语音余量
                voice_percentage = driver.find_element_by_xpath(
                    '//*[@id="stc_packramin"]/div[1]/div/div/span').text  # 语音百分比

                print('语音详情:', voice_details)
                print('语音余量:', voice_surplus)
                print('语音百分比:', voice_percentage)

                flow_details = driver.find_element_by_xpath('//*[@id="stc_packramin"]/div[2]/span[3]').text  # 流量详情
                flow_surplus = driver.find_element_by_xpath('//*[@id="stc_packramin"]/div[2]/span[4]').text  # 流量余量
                flow_percentage = driver.find_element_by_xpath(
                    '//*[@id="stc_packramin"]/div[2]/div/div/span').text  # 流量百分比

                print('流量详情:', flow_details)
                print('流量余量:', flow_surplus)
                print('流量百分比:', flow_percentage)

                sm_details = driver.find_element_by_xpath('//*[@id="stc_packramin"]/div[3]/span[3]').text  # 短信详情
                sm_surplus = driver.find_element_by_xpath('//*[@id="stc_packramin"]/div[3]/span[4]').text  # 短信余量
                sm_percentage = driver.find_element_by_xpath(
                    '//*[@id="stc_packramin"]/div[3]/div/div/span').text  # 短信百分比

                print('短信详情:', sm_details)
                print('短信余量:', sm_surplus)
                print('短信百分比:', sm_percentage)

                break
            except:
                print('资源没获取到')

        return self


if __name__ == '__main__':
    yd = ChinaMobileSpider()
    yd.login()
    yd.get_order_list()
    yd.get_basic_information()
