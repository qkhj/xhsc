# coding:utf-8
"""
操作汇总
"""
__author__ = 'johhny'

from convert_bank_data import data_convert
class daily_work():
    def run(self):
        return data_convert.insert_update_data()
