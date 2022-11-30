import urllib3
import json

KEY = '17ceed59232920002ba149d263762170f0cbea5fd1'
SECRET = 'a82ad172206b48d146a426'
IMWEB_TOKEN_URL = 'https://api.imweb.me/v2/auth'
IMWEB_CATEGORIES_URL = 'https://api.imweb.me/v2/shop/categories'
IMWEB_PRODUCT_URL = 'https://api.imweb.me/v2/shop/products'
IMWEB_INSERT_PRODUCT_URL = 'https://api.imweb.me/v2/shop/products'
IMWEB_SHOWCASE_URL = 'https://api.imweb.me/v2/shop/showcases'

http = urllib3.PoolManager()

class Api:
    # create token
    def request_token(self):
        data = {'key': KEY, 'secret': SECRET}
        response = http.request(
                method='GET', url=IMWEB_TOKEN_URL, fields=data)
        if response.status == 200:
            result = json.loads(response.data.decode('utf8'))
            return result['access_token']
        return ''

    # make header
    def make_header(self):
        token = self.request_token()
        if token:
            header = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'access-token': token,
            }
            return header
        return ''

    # get category
    def categories(self):
        header = self.make_header()
        response = http.request(
                method='GET', url=IMWEB_CATEGORIES_URL, headers=header)
        if response.status == 200:
            result = json.loads(response.data.decode('utf8'))
            print(result)
            return result['data'][0]['list']
        return ''

    # delete product
    def delete_product(self, id):
        IMWEB_PRODUCT_DELETE_URL = IMWEB_PRODUCT_URL + '/' +str(id)
        header = self.make_header()
        response = http.request(
            method = 'DELETE', url=IMWEB_PRODUCT_DELETE_URL, headers=header)
        if response.status == 200:
            result = json.loads(response.data.decode('utf8'))
            print(result)
            return result
        return ''


    # select products
    def products(self):
        header = self.make_header()
        response = http.request(
            method='GET', url=IMWEB_PRODUCT_URL, headers=header)
        if response.status == 200:
            result = json.loads(response.data.decode('utf8'))
            print(result)
            return result['data']
        return ''

    # 상품 등록 badge_type : new(신상품), best(베스트)
    def register_prodect(self, category_name, image_url, title, simple_content, content, badge_type):
        header = self.make_header()
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
        # 아임웹 카테고리 코드 조회 후 dictionary로 변경
        result = self.categories()
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
            result = json.loads(response.data.decode('utf8'))
            print(result)
            return result
        return ''