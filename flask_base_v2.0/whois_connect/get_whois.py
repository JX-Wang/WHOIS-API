#! /usr/bin/env python
# coding:utf-8
"""
whois 服务器交互
==============
author  :   wud
date   : 2018.8.30
"""

import socks
import time


class GetWhois:
    """
    server socket connect
    """
    def __init__(self, domain, whois_server):
        """处理whois服务器"""
        # 处理特殊的请求格式
        if whois_server == "whois.jprs.jp":
            self.domain = "%s/e" % domain  # Suppress Japanese output
        elif domain.endswith(".de") and (whois_server == "whois.denic.de" or whois_server == "de.whois-servers.net"):
            self.domain = "-T dn,ace %s" % domain  # regional specific stuff
        elif whois_server == "whois.verisign-grs.com" or whois_server == "whois.crsnic.net":
            self.domain = "=%s" % domain  # Avoid partial matches
        else:
            self.domain = domain
        self.whois_server = whois_server
        self.tcpCliSock = socks.socksocket()
        self.tcpCliSock.settimeout(5)
        pass

    @staticmethod
    def _bool_judge(whois_data):
        """judge result is true or false"""
        return True if (whois_data is None or len(whois_data) < 100) else False

    def get(self):
        """get whois info"""
        whois_data = ''
        for i in range(3):
            whois_data = self.connect()
            if not GetWhois._bool_judge(whois_data):  # 如果数据没有错误
                break
        if whois_data is None or len(whois_data) < 100:
            print "there are some errors during this query!"
        else:  # 数据正常
            return whois_data

    def connect(self):
        """"""
        data_result = ""
        try:
            self.tcpCliSock.connect((self.whois_server, 43))
            self.tcpCliSock.send(self.domain + '\r\n')
        except Exception as e:
            print "error -> ", str(e)
        while True:
            try:
                data_rcv = self.tcpCliSock.recv(1024)
            except Exception as e:
                print "error receive ->", str(e)
                self.tcpCliSock.close()
                return
            if not len(data_rcv):
                self.tcpCliSock.close()
                return data_result
            data_result = data_result + data_rcv


if __name__ == '__main__':
    domain = "yh888.bz"
    server = 'whois.afilias-grs.info.'
    time_start = time.time()
    try:
        whois_result = GetWhois("sina.com", "whois.corporatedomains.com").get()
        if whois_result.find("Registrar WHOIS Server") != -1:
            print "find it!"
        else:
            print "nope"
        print whois_result
    except:
        print "error "
    end_time = time.time()
    print end_time - time_start
