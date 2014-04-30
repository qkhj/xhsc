# coding:utf-8
__author__ = 'johhny'

from convert_bank_data import Interface_bank_data

class monthly_work():

    def run(self):
        return Interface_bank_data.insert_last_month_intrest()