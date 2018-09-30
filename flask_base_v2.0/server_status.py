#! /usr/bin/env python
# coding:utf-8
"""
server status check
====================
author @ wud
date   @ 2018.8.17
ver 0.1
"""

import schedule
import json
import requests
import time
# 第三方库
from Email.Email import SendEmail
from Log.log import Log

Log.init()
log = Log.logger


class ServerStatus:
    """domain status check"""
    def __init__(self):
        self.dic_name = "server_dic.json"
        self.file = file(self.dic_name)
        self.IP_dic = json.load(self.file)
        self.IP_dic = self.IP_dic['IP']
        self.timeout = 1  # 超时设定为1s
        self.file_name = "effective_ApiNode.txt"  # 有效API子节点文件

    def monitor(self):
        """status monitor"""
        schedule.every(2).hours.do(self._server_status_check)
        log.info("##########monitor service start###########")
        while True:
            schedule.run_pending()
            time.sleep(1)

    def get_query(self, server_addr):
        """send get request to confirm server status"""
        # comma_index = server_addr.find(",")
        # server = server_addr[:comma_index]
        # port = server_addr[comma_index+1:]
        query_text = "http://" + str(server_addr)

        try:
            self.query = requests.get(query_text, timeout=self.timeout)
            if self.query.status_code != 200:  # 如果访问的api返回状态值不为200，则将此api视为失效
                #  print "API error"
                log.error("API server connect")
            elif self.query.status_code == 200:
                # log.info("API normal -" + str(query_text))
                return server_addr

        except Exception as e:
            log.error("API Error -" + str(e))
            return "xxxxx " + server_addr + " xxxxx"

    def send_unavailable_serverlist(self, unavaliable_serverlist):
        """send unavailable server list to manager"""
        send = SendEmail()
        send.send(unavaliable_serverlist)

    def _server_status_check(self):
        """check server status"""
        try:
            self.f = open(self.file_name, 'w')
        except Exception as e:
            log.error("open file failed ->" + str(e))
            print "open file failed -> ", str(e)
        unavailable_serverlist = []  # 失效的API子节点
        for server_addr in self.IP_dic:
            server_address = self.IP_dic[server_addr]
            effective_server = self.get_query(server_address)  # 判断有效的API节点
            if effective_server.find('x') >= 0:  #
                # print effective_server
                unavailable_server = effective_server
                unavailable_serverlist.append(unavailable_server)
            else:
                print >> self.f, effective_server  # 只存入有效的server地址
                pass

        self.f.close()

        if unavailable_serverlist:  # 存在失效的API结点时选择发送邮件
            self.send_unavailable_serverlist(unavailable_serverlist)
        else:
            pass


if __name__ == '__main__':
    S = ServerStatus()
    print S._server_status_check()

