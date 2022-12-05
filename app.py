from time import sleep
from flask import Flask, g, render_template, jsonify
import json
import urllib3
from api import Api
from dao import Dao

app = Flask(__name__)

# Auto reload 반영을 위한 처리
config = {
    "DEBUG": True
}
app.config.from_mapping(config)

http = urllib3.PoolManager()

api = Api()
dao = Dao()

@app.route('/')
@app.route('/<name>')
def hello(name=None):
     return render_template('hello.html', name=name)

@app.route('/imweb/categories')
def categories():
    result = api.categories()
    return result

@app.route('/imweb/regist_product')
async def regist_product():
    products = await dao.products()
    print(f'total products count : {len(products)}')
    print(f'{products}')
    request_cnt = 0
    product_cnt = 0
    for i in products:
        if product_cnt % 100 == 0:
            print(f"products count : {product_cnt}")
            sleep(5)
        if request_cnt >= 5:
            sleep(1)
            request_cnt = 0
        content = f'<div style="text-align: center;"><h3>[{i["name"]}] - {i["title"]} </h3><h4 style="color: orange;">&#11015; 클릭시 해당 도매사이트로 이동합니다</h4><h4><a href="{i["url"]}" style="text-decoration: underline;"target="_blank">상세보기</a></h4></div>'
        api.register_prodect(i['category_name'], i['img'], i['title'], content, content, [i['info']])
        request_cnt += 1
        product_cnt += 1
    return 'hey~'

@app.route('/imweb/delete_product')
@app.route('/imweb/delete_product/<start>/<end>')
def delete_product(start=None, end=None):
    request_count = 0
    for i in range(int(start), int(end)+1):
        if request_count >= 5:
            sleep(1)
            request_count = 0
        api.delete_product(id=i)
        request_count += 1
    return 'result'

@app.route('/imweb/update_product')
def update_product():
    api.update_product()
    return 'update'

# @app.before_request
# def before():
#     g.token = "0a13d3cc6a45c4029c31d8b0bbcfa2c6"
#     if g.token:
#         print("get token")
#         return
#     else :
#         # 헤더 생성
#         g.token = api.request_token()
#         print(g.token)
#         print("token exist")
#         return