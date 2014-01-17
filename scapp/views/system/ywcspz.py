# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for, flash
from scapp import app

# 业务参数配置
@app.route('/System/ywcspz', methods=['GET'])
def System_ywcspz():
    return render_template("System/ywcspz.html")