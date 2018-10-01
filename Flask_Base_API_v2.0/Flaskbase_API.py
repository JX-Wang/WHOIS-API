#!/usr/bin/env python
# encoding:utf-8

"""
    主程序入口 - WHOIS api
=======================
WHOIS 查询api

version   :   0.1
author    :   @`13
time      :   2017.11.12

version   :   2.0
author    :   @WUD
time      :   2018.8.12

-history version 2.0-

    + 基于python官方的whois库进行的whois查询
    + 辅助数据全部迁移到程序中
    + 批量whois查询
    - 取消使用IP连接whois服务器
    - 所有的数据库相关操作
    ~ 速度以及资源占用的优化

"""


from flask import Flask
from flask import request, g

from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()

import whois
import json

from Setting.static import Static
from get_domain_whois import whois_query, whois_list
from Databases.database_operations import Database

Static.init()
app = Flask("WHOIS api")
app.config.update(DEBUG=True)
DB = Database()


@app.route('/')
def index():
    """index page"""
    _start = "<h1>Whois API Service v1.1 </h1>"
    _start += "<h3>author - h-j-13(@`13)</h3>"
    _start += "<h3>author - WUD(@wangjunx)</h3><br><b4>"
    _start += "<h3>Harbin Institute of Technology at Weihai</h3>"
    _start += "system clk" + str(Static.get_local_time())
    return _start


@app.route('/whois/<domain>')
def whois(domain):
    """使用python自带whois库探测WHOIS"""
    try:
        whois_info = whois.whois(domain)
        print whois_info
        if whois_info:
            return str(whois_info)
    except Exception as e:
        print "whois query error: ", str(e)


@app.route('/WHOIS/<domain>')
def WHOIS(domain, cache={}):
    """获取单一域名的WHOIS数据"""
    domain = str(domain)
    if str(domain).find(':') != -1:  # 指定whois服务器的whois探测
        if cache.has_key(domain):
            return json.dumps(cache[domain], indent=1)
        else:
            whois_server = domain[domain.find(':')+1:]
            domain = domain[:domain.find(':')]
            data = whois_query(domain, whois_server)
            if data.has_key('flag') and data['flag'] > 0:  # 只缓存正常数据
                if len(cache) >= 10000:
                    cache.popitem()
                cache[domain] = data
                return json.dumps(cache[domain], indent=1)
            else:
                return json.dumps(data, indent=1)
    else:  # 没有指定whois服务器请求的查询请求
        if cache.has_key(domain):
            return json.dumps(cache[domain], indent=1)
        else:
            data = whois_query(domain, '')
            if data.has_key('flag') and data['flag'] > 0:  # 只缓存正常数据
                if len(cache) >= 10000:
                    cache.popitem()
                cache[domain] = data
                return json.dumps(cache[domain], indent=1)
            else:
                return json.dumps(data, indent=1)


@app.route('/WHOIS/')
def WHOIS_list():
    """批量获取域名的WHOIS数据"""
    domain_list = request.args.get('domain_list', default='', type=str)
    return whois_list(domain_list.split(';'))


if __name__ == '__main__':
    http_server = WSGIServer(('', Static.API_PORT), app)
    http_server.serve_forever()
