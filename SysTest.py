#! /usr/bin/env python
# coding:utf-8
"""
API_sys 系统检测程序
=====================
date    :   2018.8.28
author  :   WUD
"""

import MySQLdb
import requests

import gevent
from gevent import monkey
monkey.patch_all()

import time
import multiprocessing


connect = {
    'host': "42.236.62.58",
    'user': 'root',
    'passwd': "hitwh@dns#58",
    'port': 36666,
    'charset': "utf8",
    'db': "beijing_whowas"
}

domain_list = []
flag_dic = {
    0: 0,
    1: 0,
    -29: 0,
    -2: 0,
    10: 0,
    -1: 0,
    -3: 0,
    -13: 0,
    -11: 0,
    -15: 0,
    -5: 0,
    -4: 0,
    -99: 0,
    -98: 0
}


class TEST:
    """Sys Test Class"""
    def __init__(self):
        try:
            self.DB = MySQLdb.connect(**connect)
            self.Cursor = self.DB.cursor()
        except Exception as e:
            print "connect error -> ", str(e)

    def get_domain(self):
        for i in range(1, 11):
            sql = "select domain from domain_" + str(i) + " WHERE whois_flag = 1 limit 96"
            self.Cursor.execute(sql)
            info = self.Cursor.fetchall()
            for domain in info:
                try:
                    domain_list.append(domain[0])
                except Exception as e:
                    print "append error ->", str(e)
                    pass

    def get_whois(self, domain):
        #  self.success = 0
        # for domain in domain_list:
        url = "http://localhost:8048/WHOIS/" + str(domain)
        try:
            self.result = requests.get(url, timeout=5)
        except Exception as e:
            f = open("Timeout_domain", 'w')
            print >>f, domain
            f.close()
        print url
        try:
            whois_dic = str(self.result.text)
            whois_dic = eval(whois_dic)
            self.flag = whois_dic["flag"]
            flag_num = flag_dic[self.flag]
            flag_dic[self.flag] = flag_num + 1
        except:
            print "error"
            pass
        # print result.text

    def time_test(self):
        print "start"
        time.sleep(10)
        print time.time()

    def gevent(self):
        for i in range(12):
            task = []
            for j in range(80):
                task.append(gevent.spawn(self.get_whois, domain_list[i*80 + j]))
            gevent.joinall(task)

    def main(self):
        time_start = time.time()
        self.get_domain()
        # self.get_whois()
        self.gevent()
        time_end = time.time()
        return time_end - time_start


if __name__ == '__main__':

    T = TEST()
    print T.main()
    for i in flag_dic:
        print i, ":", flag_dic[i]

