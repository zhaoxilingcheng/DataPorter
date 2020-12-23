import json
import requests, time, pandas

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 '
                  'Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '2253',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': '_zcy_log_client_uuid=1fbdbbe0-44f0-11eb-9e4b-37b2d64b36a7; platform_code=zcy; '
              'SESSION=YzM5NzhlNGMtYTAzZC00ZjhhLWJiZDYtNjk5MjdjNmU5NTZl; wsid=10007177075#1608708363328; uid=10008560085; user_type=0202; tenant_code=509900; institution_id=145481266786306; UM_distinctid=1768e7dafe11a6-0eb9614a35fcce-5c173a1b-1fa400-1768e7dafe2319; districtCode=509900; districtName=%E9%87%8D%E5%BA%86%E5%B8%82%E6%9C%AC%E7%BA%A7; acw_tc=76b20ff016087083692826870e62169e78e5df00c5f20dc470fcd623fa955c',
    'Host': 'www.zcygov.cn',
    'Origin': 'https://www.zcygov.cn',
    'Referer': 'https://www.zcygov.cn/item-center-front/publishgoods/prePublish?current=1&categoryType=0&categoryId=6674'
               '&categoryPath=%E6%97%A5%E7%94%A8%E7%99%BE%E8%B4%A7-%E5%B1%85%E5%AE%B6%E6%97%A5%E7%94%A8-%E9%9B%A8%E8%A1%A3',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 ' \
                  'Safari/537.36'
}

get_headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

headers[
    'Cookie'] = '_zcy_log_client_uuid=1fbdbbe0-44f0-11eb-9e4b-37b2d64b36a7; platform_code=zcy; user_type=0202; tenant_code=509900; institution_id=145481266786306; UM_distinctid=1768e7dafe11a6-0eb9614a35fcce-5c173a1b-1fa400-1768e7dafe2319; districtCode=509900; districtName=%E9%87%8D%E5%BA%86%E5%B8%82%E6%9C%AC%E7%BA%A7; acw_tc=76b20ffd16087134636527657e2831219b0aeac56673cb8009199777642c00; SESSION=ZmQ0ODMyNGItN2E4YS00ODZjLWI2YmItYmU2ZDIyOTNjZTAy; wsid=10007177075#1608713473804; uid=10008560085; session_application_code=zcy.product'



def handle(item_id):
    resp = requests.get(f'https://www.zcygov.cn/front/detail/item/{item_id}', headers=get_headers, verify=False)
    time.sleep(2)
    result = json.loads(resp.text)['result']
    item = result['item']
    skus = result['skus']
    for sku in skus:
        for i in sku['fullPrice']:
            sku['fullPrice'][i] = sku['fullPrice'][i] / 100
        sku['fullPriceYuan'] = sku['fullPrice']
    groupedSkuAttributes = result['groupedSkuAttrs']
    params_resp = requests.get(f'https://www.zcygov.cn/front/detail/item/param?itemId={item_id}',
                               headers=get_headers, verify=False)
    time.sleep(2)
    groupedOtherAttributes = json.loads(params_resp.text)['result']
    if 'origin' in item:
        groupedOtherAttributes[0]['otherAttributes'].append({
            "attrKey": "产地",
            "attrVal": json.dumps(item['origin']),
            "group": "通用属性",
            "propertyId": 81973,
            "richInfo": 'false',
            "unit": ""
        })
    form_link = 'https://item.jd.com/100002631638.html#crumb-wrap'
    if 'extra' in item:
        form_link = item['extra']['selfPlatformLink']
    groupedOtherAttributes[0]['otherAttributes'].append({
        "attrKey": "电商平台链接",
        "attrVal": item['extra']['selfPlatformLink'],
        "group": "通用属性",
        "propertyId": 81973,
        "richInfo": 'false',
        "unit": ""
    })
    request_json = {
        "baseGood": {
            "itemDTO": {
                "baseItem": {
                    "item": item,
                    "itemDetail": {
                        "images": result['itemDetail']['images']
                    },
                    "richText": result['itemDetail']['detail'],
                    "skus": skus,
                    "stocks": [
                        {
                            "warehouseCode": "DEFAULT151800904994831_1",
                            "quantity": 1000
                        }
                    ],
                    "groupedSkuAttributes": groupedSkuAttributes,
                    "groupedOtherAttributes": groupedOtherAttributes,
                    "fullItemMainExtDTO": {
                        "itemCode": "",
                        "itemPriceUnit": "元",
                        "itemPriceDesc": "费率"
                    },
                    "fullItemServiceRelDTOS": [],
                    "agCategoryGroupedOtherAttributes": [],
                    "images": {}
                },
                "channelAttrs": [],
                "layer": "28"
            },
            "parts": [],
            "isNewBusiness": 'true'
        },
        "name": item['name'],
        "categoryId": item['categoryId']
    }
    post = requests.post(url='https://www.zcygov.cn/api/goods/draft/channel/create', json=request_json,
                         headers=headers, verify=False)
    post.raise_for_status()
    if not json.loads(post.text)['success']:
        raise Exception(json.loads(post.text)['error'])
    print(post.text)
    time.sleep(2)


if __name__ == '__main__':
    df = pandas.read_csv('./item_id.csv')
    for i in df:
        i['handle'] = True
    for index, row in df.iterrows():
        id_ = row['item_id']
        print(f'当前处理的item_id = {id_}')
        handle(id_)

