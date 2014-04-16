# coding:utf-8
__author__ = 'johhny'

from scapp import app
from scapp.models.credit_data.sc_stock import SC_Stock
from scapp.tools import json_encoding
import urllib2
import json

@app.route('/report/print_stock/<int:loan_apply_id>', methods=['GET'])
def print_stock(loan_apply_id):
    data=SC_Stock.query.filter_by(loan_apply_id=loan_apply_id).all()

    req = urllib2.Request('http://192.168.0.250:8080/restWS/rest/Service/sc_stock')

    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(data,encoding=json_encoding,ensure_ascii=False))
    print response
    return None
