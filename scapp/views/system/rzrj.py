# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for, flash

from scapp import app

# 日终日结
@app.route('/System/rzrj', methods=['GET'])
def System_rzrj():
    return render_template("System/rzrj.html")