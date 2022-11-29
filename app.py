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
    return result

@app.route('/imweb/regist_product')
async def regist_product():
    result = await dao.test()
    return jsonify(result)

@app.route('/imweb/delete_product/<id>')
def delete_product(id=None):
    result = api.delete_product(id=id)
    return result
