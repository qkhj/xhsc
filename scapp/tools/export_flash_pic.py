# coding:utf-8
from flask import make_response
import base64

#导出flash图片(base64格式)
class export_flash_pic():

    def export(self, imageData,filename):
		imgData = base64.b64decode(imageData)
		#return send_file(io.BytesIO(imgData))
		response = make_response(imgData)
		response.headers['Content-Type'] = 'image/jpeg'
		response.headers['Content-Disposition'] = 'attachment; filename='+filename+'.jpg'
		return response

