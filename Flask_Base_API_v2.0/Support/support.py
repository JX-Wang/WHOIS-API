#! /usr/bin/env python
# encoding:utf-8

"""
WHOIS服务器以及对应的IP
====================
author @wud
date @2018.8.12
"""

import MySQLdb

dict = {}

db = MySQLdb.connect("10.245.146.37", "root", "platform","whois_support", charset="utf8")
cursor = db.cursor()
sql = "select Pounycode, whois_addr from whois_tld_addr"
cursor.execute(sql)
results = cursor.fetchall()
#print results
for result in results:
    #print result
    print result[1]
    result[1] = str(result[1])
    try:
        flag = result[1].index(",")
        result[1] = result[1][:flag]
        print result[1]
    except:
        pass
    dict[result[0]] = result[1]

#for key in dict:
    #print '"' + key + '"' + ": " + '"' + str(dict[key]) + '",'