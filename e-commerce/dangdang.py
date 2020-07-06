from base_spider import BaseSpider
import re
import json
from models import *

class DangDangSpider(BaseSpider):

    def __init__(self, sleep_time: int = 3):
        super().__init__(base_url='http://dangdang.com', login_url='https://login.dangdang.com/signin.aspx',
                         verify_url='http://www.dangdang.com/', sleep_time=sleep_time)

    def sub_login(self):
        driver = self.driver
        mask_close = driver.find_element_by_xpath('//*[@id="J_loginMaskClose"]')
        if mask_close:
            mask_close.click()
        scan = driver.find_element_by_xpath('//*[@id="J_loginDiv"]/div[1]/div[1]/a[1]')
        scan.click()
        scan_image_url = driver.find_element_by_xpath('//*[@id="J_qrcodeImg"]').get_attribute('src')

    def run(self):
        self.get_order_list()

    def get_order_list(self):
        page = 1
        while True:
            print(f'当前爬取第{page}页')
            self.driver.get(f'http://myhome.dangdang.com/myOrder/list?searchType=1&statusCondition=0&timeCondition=4'
                            f'&pageCurrent={page}')
            html = self.driver.page_source
            match = re.findall('var info=eval\((.*)\)', html)
            data = json.loads(match[0])
            total = data['pageInfo']['total']
            page_size = data['pageInfo']['pageSize']
            data_list = data['orderList']
            print(f'爬取订单数量为{len(data_list)}')
            for i in data_list:
                order = i['order']
                products = i['products']
                for product in products:
                    order_model = OrderModel(
                        order_id=order['orderId'],
                        total_price=order['totalPrice'],
                        receiver_name=order['receiverName'],
                        receiver_address=order['receiverAddress'],
                        receiver_phone=order['urgeReceiverMobile'],
                        product_name=product['productName'],
                        price=product['salePrice'],
                        product_url=product['productSnapshotUrl'],
                        status=order['orderViewStatus'],
                        order_time=order['orderCreationDate'],
                        delivery_date=order['deliveryDate'],
                        channel_type=self.__class__.__name__)
                    self.data_list.append(order_model)
            if total <= page * page_size:
                print(f'查询完毕, 总数量为{total}')
                break
            page = page + 1
            self.sleep()
        return self


if __name__ == '__main__':
    dd = DangDangSpider()
    dd.start()

