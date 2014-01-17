# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for
from scapp import app


# 客户
@app.route('/Report/kh', methods=['GET'])
def Report_kh():
    return render_template("Report/kh.html")

