from base_spider import BaseSpider
import time
from models import *
from lxml import etree

class JdSpider(BaseSpider):

    def __init__(self,sleep_time: int = 3):
        super().__init__(base_url='http://jd.com',login_url='https://passport.jd.com/new/login.aspx', verify_url='https://www.jd.com/',sleep_time=sleep_time)

    def sub_login(self):
        pass

    def get_order_list(self):
        def getData():
            html = self.driver.page_source
            lxml = etree.HTML(html)
            tbodys=lxml.xpath('//table[@class="td-void order-tb"]//tbody')
            for tb in tbodys:
                id=tb.xpath('./@id')[0]
                if id.split('-')[0] != 'tb':
                    continue
                else:
                    id=id.split('-')[-1]
                    timedate = ''.join(tb.xpath('./tr[2]/td/span[2]/text()'))
                    if timedate:
                        shop_name = ''.join(tb.xpath('./tr[2]/td/div/span[1]/a[1]/text()')).strip()  # 店铺名
                        if not shop_name:
                            shop_name = ''.join(tb.xpath('./tr[2]/td/div/span/span/text()')).strip()  # 店铺名
                        trade_name = ''.join(tb.xpath('./tr[3]/td/div/div[2]/div[1]/a/text()')).strip()
                        trade_url = ''.join(tb.xpath('./tr[3]/td/div/div[2]/div[1]/a/@href')).strip()

                        goods_number = ''.join(tb.xpath('./tr[3]/td[1]/div[2]/text()')).strip()

                        addressee = ''.join(tb.xpath('./tr[3]/td[2]/div/span/text()')).strip()
                        try:
                            addr = ''.join(tb.xpath('./tr[3]/td[2]/div/div/div[1]/p[1]/text()')).strip()
                            phone = ''.join(tb.xpath('./tr[3]/td[2]/div/div/div[1]/p[2]/text()')).strip()
                        except:
                            addr = ''
                            phone = ''
                        money = ''.join(tb.xpath('./tr[3]/td[3]/div/span[1]/text()')).strip().replace('¥','')
                        pay_mode = ''.join(tb.xpath('./tr[3]/td[3]/div/span[2]/text()')).strip()
                        status = ''.join(tb.xpath('./tr[3]/td[4]/div/span/text()')).strip()

                    else:
                        timedate = ''.join(tb.xpath('./tr[1]/td/span[2]/text()')).strip()
                        shop_name = ''.join(tb.xpath('./tr[1]/td/div/span[1]/a[1]/text()')).strip()  # 店铺名
                        if not shop_name:
                            shop_name = ''.join(tb.xpath('./tr[1]/td/div/span/span/text()')).strip()  # 店铺名
                        trade_name = ''.join(tb.xpath('./tr[2]/td[1]/div[1]/div[2]/div[1]/a/text()')).strip()
                        trade_url = ''.join(tb.xpath('./tr[2]/td[1]/div[1]/div[2]/div[1]/a/@href')).strip()
                        goods_number = ''.join(tb.xpath('./tr[2]/td[1]/div[2]/text()')).strip()
                        addressee = ''.join(tb.xpath('./tr[2]/td[2]/div/span/text()')).strip()
                        try:
                            addr = ''.join(tb.xpath('./tr[2]/td[2]/div/div/div[1]/p[1]/text()')).strip()
                            phone = ''.join(tb.xpath('./tr[2]/td[2]/div/div/div[1]/p[2]/text()')).strip()
                        except:
                            addr = ''
                            phone = ''
                        money = ''.join(tb.xpath('./tr[2]/td[3]/div/span[1]/text()')).strip().replace('¥','')
                        pay_mode = ''.join(tb.xpath('./tr[2]/td[3]/div/span[2]/text()')).strip()
                        status = ''.join(tb.xpath('./tr[2]/td[4]/div/span/text()')).strip()


                    # print(id,timedate,shop_name,trade_name,goods_number,addressee,addr,phone,money,pay_mode,status)

                    order_model = OrderModel(order_id=id,total_price=money,receiver_name=addressee,receiver_address=addr,receiver_phone=phone,
                                             product_name=trade_name,price=money,product_url=trade_url,status=status,order_time=timedate,
                                             delivery_date='',channel_type=self.__class__.__name__)
                    self.data_list.append(order_model)

            next=lxml.xpath('//*[@id="order02"]/div[2]/div[2]/div[1]/a[3]/@href')
            if next:
                self.driver.find_element_by_xpath('//*[@id="order02"]/div[2]/div[2]/div[1]').click()
                getData()
            print(f'{year}年采集完成！')

        years = [3,2014,2015, 2016, 2017, 2018, 2019, 2020]
        for year in years:
            self.driver.get(f'https://order.jd.com/center/list.action?search=0&d={year}&s=4096')
            getData()

if __name__ == '__main__':
    dd = JdSpider().login_by_cookies()
    dd.get_order_list()
    dd.to_csv()
    dd.save_cookie()
    dd.close()

