#! /usr/bin/env python
# coding:utf8
"""
SQL generator
===============
author  :   WUD
date    :   2018.9.16
"""
from WhoisData.domain_status import get_status_value


class SQL:
    """sql generator"""
    def __init__(self):
        pass

    @staticmethod
    def insert_whois(whois_dict):
        whois_dict['details'] = whois_dict['details'].replace("\\", "").replace("'", " \\'").replace('"', ' \\"')
        whois_dict['domain_status'] = get_status_value(";".join(whois_dict['domain_status']))
        SQL = """INSERT IGNORE `{table}` set """.format(table='domain_whois')
        SQL += """`domain` = '{Value}', """.format(Value=whois_dict['domain'])
        SQL += """`flag` = {Value}, """.format(Value=whois_dict['flag'])
        SQL += """`tld` = '{Value}', """.format(Value=whois_dict['tld'])
        SQL += """`top_whois_server` = '{Value}', """.format(Value=whois_dict['top_whois_server'])
        SQL += """`domain_status` = '{Value}', """.format(Value=whois_dict['domain_status'])
        SQL += """`sponsoring_registrar` = '{Value}', """.format(Value=whois_dict['sponsoring_registrar'])
        SQL += """`sec_whois_server` = '{Value}', """.format(Value=whois_dict['sec_whois_server'])
        SQL += """`reg_name` = '{Value}', """.format(Value=whois_dict['reg_name'])
        SQL += """`reg_phone` = '{Value}', """.format(Value=whois_dict['reg_phone'])
        SQL += """`reg_email` = '{Value}', """.format(Value=whois_dict['reg_email'])
        SQL += """`org_name` = '{Value}', """.format(Value=whois_dict['org_name'])
        SQL += """`name_server` = '{Value}', """.format(Value=";".join(whois_dict['name_server']))
        SQL += """`creation_date` = '{Value}', """.format(Value=whois_dict['reg_date'])
        SQL += """`expiration_date` = '{Value}', """.format(Value=whois_dict['expir_date'])
        SQL += """`update_date` = '{Value}',  """.format(Value=whois_dict['updated_date'])
        SQL += """`details` = '{Value}' """.format(Value=whois_dict['details'])
        # print SQL
        return SQL
