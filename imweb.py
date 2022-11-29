import os
import logging
from time import sleep
from urllib import response
import urllib3
import json
import re
import math
from datetime import datetime, timedelta
from urllib.parse import urlencode

KEY = '17ceed59232920002ba149d263762170f0cbea5fd1'
SECRET = 'a82ad172206b48d146a426'
IMWEB_TOKEN_URL = 'https://api.imweb.me/v2/auth'
IMWEB_CATEGORIES_URL = 'https://api.imweb.me/v2/shop/categories'
IMWEB_PRODUCT_URL = 'https://api.imweb.me/v2/shop/products'
IMWEB_INSERT_PRODUCT_URL = 'https://api.imweb.me/v2/shop/products'
IMWEB_SHOWCASE_URL = 'https://api.imweb.me/v2/shop/showcases'

http = urllib3.PoolManager()


# 토큰 생성
def request_token():
    data = {'key': KEY, 'secret': SECRET}
    response = http.request(
            method='GET', url=IMWEB_TOKEN_URL, fields=data)
    if response.status == 200:
        result = json.loads(response.data.decode('utf8'))
        print(result)
        return result['access_token']
    return ''

# 헤더 생성
def make_header():
    token = request_token()
    if token:
        header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'access-token': token,
        }
        return header
    return ''

# 기획전 조회
def showcase():
    header = make_header()
    response = http.request(
            method='GET', url=IMWEB_SHOWCASE_URL, headers=header)
    if response.status == 200:
        print(json.loads(response.data.decode('utf8')))

# 카테고리 조회
def categories():
    header = make_header()
    response = http.request(
            method='GET', url=IMWEB_CATEGORIES_URL, headers=header)
    if response.status == 200:
        result = json.loads(response.data.decode('utf8'))
        print(result)
        return result['data'][0]['list']
    return ''

# 상품 삭제
def delete(id):
    IMWEB_PRODUCT_DELETE_URL = IMWEB_PRODUCT_URL + '/' +str(id)
    header = make_header()
    response = http.request(
        method = 'DELETE', url=IMWEB_PRODUCT_DELETE_URL, headers=header)
    if response.status == 200:
        result = json.loads(response.data.decode('utf8'))
        print(result)


# 상품 조회
def products():
    header = make_header()
    response = http.request(
        method='GET', url=IMWEB_PRODUCT_URL, headers=header)
    if response.status == 200:
        result = json.loads(response.data.decode('utf8'))
        print(result)
        return result['data']
    return ''

# 상품 등록 badge_type : new(신상품), best(베스트)
def register_prodect(category_name, image_url, title, simple_content, content, badge_type):
    header = make_header()
    '''
    {'IT/디지털': 's202110266ac024654e5f9',
     '종합': 's2022112744dcfd7303c71',
     '식품': 's202211272c11491fce9e7',
     '헬스케어/뷰티': 's202211272d2fa89b7a78f',
     '산업': 's202211279d64a3a0c7a66',
     '애완': 's2022112725caf84a54e73',
     '디지털/가전': 's20221127d1a14776da386',
     '완구/유아': 's202211273d24eb8b62d55',
     '의류': 's20221127cdf309de4dbab',
     '신발/잡화': 's202211275847a45e520ad',
     '자동차': 's20211203acab339fa5773',
     '생활': 's2021120390a3eb54d802c',
     '인테리어/소품': 's202211276b2e6087ef1b3'}
    '''
    result = categories()
    category = {}
    for i in result:
        category[i['name']] = i['code']
    print(category)

    is_badge_new = False
    is_badge_best = False
    is_badge_md = False
    is_badge_hot = False
    origin = '상세정보 참조'
    maker = '상세정보 참조'
    brand = '상세정보 참조'

    for i in badge_type:
        if i == '11':
            is_badge_new = True
        if i == '12':
            is_badge_best = True

    print("is_badge_new: " + str(is_badge_new))
    print("is_badge_best: " + str(is_badge_best))

    data = {
        'categories':[category[category_name]],
        #'showcase' : ['c202112036b270300a476b'],
        'images' : [image_url],
        'name' : title,
        'simple_content' : simple_content,
        'content' : content,
        'use_mobile_prod_content' : True,
        'mobile_content' : content,
        'prod_status' : 'sale',
        'prod_type' : 'normal',
        #'subscribe_group_code' : '',
        #'subscribe_period' : 120,
        'is_badge_new' : is_badge_new,
        'is_badge_best' : is_badge_best,
        'is_badge_md' : is_badge_md,
        'is_badge_hot' : is_badge_hot,
        'origin' : origin,
        'maker' : maker,
        'brand' : brand,
        'seo_title' : title,
        'seo_description' : title,
        'seo_access_bot' : True,
        'price' : 0,
        'price_org' : 0,
        'price_tax' : False,
        'price_none' : True,
        #'prodinfo' : [],
        'give_point_type' : 'common',
        'give_point_value_type' :'percent',
        #'give_point_value' : 0,
        #'product_discount_options' : [],
        #'period_discount_data' : [],
        'use_pre_sale' : False,
        #'pre_sale_start_date' : '',
        #'pre_sale_end_date' : '',
        'weight' : 0,
        # 자체 상품 코드'custom_prod_code' : '1a1',
        #'pay_product_name' : '',
        #'event_words' : '',
        #'naver_category' : '',
        #'condition' : '',
        'product_flag' : '도매',
        'order_made' : False,
        'parallel_import' : False,
        'import_flag' : False,
        'is_culture_benefit' : False,
        'minimum_purchase_quantity' : 1,
        'member_maximum_purchase_quantity' : 100,
        'optional_limit_type' : 'relative',
        'optional_limit' : 100,
        'use_unipass_number' : 'N',
        'adult' : False,
        #'display' : [],
        'stock_use' : False,
        'stock_unlimit' : False,
        #'stock_no_option' : 1000,
        'sku_no_option' : 'T1',
        #'options' : [],
    }
    json_body = json.dumps(data).encode('utf-8')
    response = http.request(
        method='POST', url=IMWEB_INSERT_PRODUCT_URL, body=json_body, headers=header)
    if response.status == 200:
        print(json.loads(response.data.decode('utf8')))

    return ''

# 연속된 상품 삭제(시작 번호, 끝번호)
def delete_products(start_id, end_id):
    request_count = 0
    for i in range(start_id, end_id+1):
        if request_count >= 5:
            sleep(1)
            request_count = 0
        delete(i)
        request_count += 1

def main():
    delete_products(103, 103)
    content = '<div style="text-align: center;"><h3>[카유니아] - 상품이름 </h3><h4 style="color: orange;">&#11015; 클릭시 해당 도매사이트로 이동합니다</h4><h4><a href="www.naver.com" style="text-decoration: underline;"target="_blank">상세보기</a></h4></div>'
    register_prodect('자동차', 'https://bowmall.co.kr/data/goods/1/2021/03/792_temp_16157701678838large.jpg',
    '카이프 친환경 반려묘 사막화 미끄럼방지 다용도 매트',content,content,
    ['12'])
    #register_prodect()
    #delete_products(13,43)
    #products()
    #insert_post()


if __name__ == "__main__":
    main()