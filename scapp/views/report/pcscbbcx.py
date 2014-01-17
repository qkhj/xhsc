# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for
from scapp import app


# 批次生成报表查询
@app.route('/Report/pcscbbcx', methods=['GET'])
def Report_pcscbbcx():
    return render_template("Report/pcscbbcx.html")

