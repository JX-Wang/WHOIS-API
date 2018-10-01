#! /usr/bin/env python
# coding: utf8
"""
Mysql operation
===============
author  :   wud
date    :   2018.9.16
"""
import MySQLdb

mysql_connect = {
    "host": "*",
    "user": "*",
    "passwd": "*",
    "port": *,
    "db": "*",
    "charset": "utf8"
}


class Database:
    """ Database Operations """
    def __init__(self):
        try:
            self.DB = MySQLdb.connect(**mysql_connect)
            self.Cursor = self.DB.cursor()
        except Exception as e:
            print "connect mysql error -> ", str(e)

    def execute(self, sql):
        try:
            self.Cursor.execute(sql)
        except Exception as e:
            print "insert error ->", str(e)

    def commit(self):
        try:
            self.DB.commit()
        except Exception as e:
            print "commit error ->", str(e)


if __name__ == '__main__':
    pass
