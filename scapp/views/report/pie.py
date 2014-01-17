# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for
from scapp import app

# 饼图
@app.route('/Report/pie', methods=['GET'])
def Report_pie():
    return render_template("Report/pie.html")

