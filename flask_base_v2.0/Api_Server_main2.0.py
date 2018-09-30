#! /usr/bin/env python
# coding:utf-8
"""
whois client API server
=======================
author @ wud
date   @ 2018.8.17
ver 0.1

author @ wud
date   @ 2018.9.15
ver 2.0
"""

import requests
import random
import multiprocessing
from flask import Flask
# import gevent
from gevent import monkey
from gevent.pywsgi import WSGIServer
from Log.log import Log

monkey.patch_all()
app = Flask("WHOIS SERVICE API")
app.config.update(DEBUG=True)

file_name = "effective_ApiNode.txt"
_port = 8048
Log.init()
log = Log.logger


def start():
    """API start"""
    _start = "API Server start\n"
    _start += "* For Whois Query\n"
    _start += "* wud@WangJunxiong\n"
    http_server = WSGIServer(('', _port), app)
    http_server.serve_forever()


@app.route('/')
def index():
    """Index page"""
    _index = "<h1>WHOIS SERVICE API VER 0.1</h1>"
    _index += "<h3>Author - Wangjunx@WUD </h3>"
    _index += "<h3>Harbin Institute Of Technology At Weihai</h3>"
    _index += "<h5>Cyberspace Security</h5>"
    return _index


@app.route('/WHOIS/<domain>')
def whois(domain):
    """Get domain whois"""
    file_path = file_name
    f = open(file_path, 'r')
    server_list = f.readlines()
    server = server_list[random.randint(0, len(server_list)-1)][:-1]
    f.close()
    if server.find('\r') > 0:
        server = server[:server.find('\r')]
    else:
        server = server
    text = "http://" + str(server) + "/WHOIS/" + domain
    log.info(str(text))
    whois_get = requests.get(text)
    whois_dict = whois_get.text
    return whois_dict


@app.route('/check')
def check():
    """Get server status.

       but we this instance we do not need now.

    """


if __name__ == '__main__':
    from server_status import ServerStatus
    S = ServerStatus()
    API_process = multiprocessing.Process(target=start, name="API SERVICE")
    API_process.start()
    monitor_process = multiprocessing.Process(target=S.monitor, name="Monitor service")
    monitor_process.start()

