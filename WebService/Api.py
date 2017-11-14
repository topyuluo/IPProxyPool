# -*- coding:utf-8 -*-

from  flask import  Flask , jsonify ,request
from DB.DBClientFactory import DBClientFactory
from Utils.Logger import Logger
from Utils.Constants import dbName , validatePool
from Utils.ReadConfigUtil import ReadConfigUtil

logger = Logger('web').getLog()
web_port = ReadConfigUtil().getInt('WebApi' , 'port')
app = Flask(__name__)

api_list = {
    'get': 'get an usable proxy',
    'refresh': 'refresh proxy pool',
    'get/num': 'num need less than 10 ',
    'getcount':'return proxy count num ',
    'delete?proxy=122.11.3.1:8080':'delete an unable proxy'
}
db = DBClientFactory(dbName , validatePool ).createDB()
@app.route('/')
def hello():
    return jsonify(api_list)

@app.route('/get/')
def get_one():
    proxy = db.get()
    dict = {'proxy':proxy}
    return jsonify(dict)

@app.route('/get/<int:num>')
def get_more(num):
    list = []
    intnum = int(num)
    if intnum >10:
        return '请求数量过多,数量小于10！'
    for n in range(intnum):
        proxy = db.get()
        list.append(proxy)
    info = {
        'proxy':list
    }
    return jsonify(info)

# @app.route("/refresh")
# def refresh():
#     schedule = ProxyRefreshSchedule()
#     schedule.validate_proxy()

@app.route('/delete/', methods=['GET'])
def delete():
    proxy = request.args.get('proxy')
    print( proxy)
    db.remove(proxy)
    return 'success'


@app.route('/getcount')
def getcount():
    count = db.getcount()
    dict = {'num':count}
    return jsonify(dict)

def run():
    logger.info('[Api.py] Run Success !')
    app.run(host='0.0.0.0' ,port= web_port)

if __name__ == '__main__':
    run()

