class OrderModel:
    def __init__(self, order_id, total_price, receiver_name, receiver_address, receiver_phone, product_name, price,
                 product_url, status, order_time, delivery_date, channel_type):
        # 总订单id
        self.order_id = order_id
        # 总价格
        self.total_price = total_price
        # 收货人
        self.receiver_name = receiver_name
        # 收货地址
        self.receiver_address = receiver_address
        # 收货手机号
        self.receiver_phone = receiver_phone
        # 产品名称
        self.product_name = product_name
        # 产品价格
        self.price = price
        # 产品链接
        self.product_url = product_url
        # 订单状态
        self.status = status
        # 下单时间
        self.order_time = order_time
        # 收获时间
        self.delivery_date = delivery_date
        # 渠道类型 ex: dangdang、jd、taobao
        self.channel_type = channel_type
