# coding:utf-8

from flask import Module, session, request, render_template, redirect, url_for
from scapp import app


# 柱状图
@app.route('/Report/bar', methods=['GET'])
def Report_bar():
    return render_template("Report/bar.html")

