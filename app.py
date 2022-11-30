from time import sleep
from flask import Flask, render_template, jsonify
import json
import urllib3
from api import Api
from tortoise_example import Dao

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
    request_cnt = 0
    for i in result:
        if request_cnt >= 5:
            sleep(1)
            request_cnt = 0
        content = f'<div style="text-align: center;"><h3>[{i["name"]}] - {i["title"]} </h3><h4 style="color: orange;">&#11015; 클릭시 해당 도매사이트로 이동합니다</h4><h4><a href="{i["url"]}" style="text-decoration: underline;"target="_blank">상세보기</a></h4></div>'
        api.register_prodect(i['category_name'], i['img'], i['title'], content, content, i['info'])
        request_cnt += 1

    return result

@app.route('/imweb/regist_product')
async def regist_product():
    result = await dao.products()
    request_cnt = 0
    for i in result:
        if request_cnt >= 5:
            sleep(1)
            request_cnt = 0
        content = f'<div style="text-align: center;"><h3>[{i["name"]}] - {i["title"]} </h3><h4 style="color: orange;">&#11015; 클릭시 해당 도매사이트로 이동합니다</h4><h4><a href="{i["url"]}" style="text-decoration: underline;"target="_blank">상세보기</a></h4></div>'
        api.register_prodect(i['category_name'], i['img'], i['title'], content, content, i['info'])
        request_cnt += 1
    return jsonify(result)

@app.route('/imweb/delete_product/<id>')
def delete_product(id=None):
    result = api.delete_product(id=id)
    return result