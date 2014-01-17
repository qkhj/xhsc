# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for, flash

from scapp import app

# 接口配置
@app.route('/System/jkpz', methods=['GET'])
def System_jkpz():
    return render_template("System/jkpz.html")