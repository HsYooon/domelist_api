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
            print(result)
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