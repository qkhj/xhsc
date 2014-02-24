# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for,make_response
from scapp import app
from scapp.tools.export_flash_pic import export_flash_pic

# 柱状图
@app.route('/Report/bar', methods=['GET'])
def Report_bar():
    return render_template("Report/bar.html")

@app.route('/Report/flash/export_pic',methods=['GET','POST'])
def Export_pic():
	imageData = request.form['imageData']
	exp = export_flash_pic()
	return exp.export(imageData,'myimg')
	

