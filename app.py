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
    print("__3_______________________")
    result = await dao.products()
    print("__1_______________________")
    print(result)
    print("__2_______________________")
    request_cnt = 0
    for i in result:
        if request_cnt >= 5:
            sleep(1)
            request_cnt = 0
        content = f'<div style="text-align: center;"><h3>[{i["name"]}] - {i["title"]} </h3><h4 style="color: orange;">&#11015; 클릭시 해당 도매사이트로 이동합니다</h4><h4><a href="{i["url"]}" style="text-decoration: underline;"target="_blank">상세보기</a></h4></div>'
        api.register_prodect(i['category_name'], i['img'], i['title'], content, content, i['info'])
        request_cnt += 1
    return 'hey~'

@app.route('/imweb/delete_product')
def delete_product():
    start_id = 112
    end_id = 123
    
    request_count = 0
    for i in range(start_id, end_id+1):
        if request_count >= 5:
            sleep(1)
            request_count = 0
        api.delete_product(id=i)
        request_count += 1
    return 'result'