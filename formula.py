# -*- coding:utf-8 -*-
#! python3

# FaceCat-Python-Wasm(OpenSource)
#Shanghai JuanJuanMao Information Technology Co., Ltd 

import math
import requests
import time
from requests.adapters import HTTPAdapter
from facecat import *
import facecat
from ctypes import *
import os

#K线数据转字符串
#datas 数据
def securityDatasToStr(datas):
	result = ""
	for i in range(0, len(datas)):
		data = datas[i]
		result = result + str(data.m_date) + "," + str(data.m_close) + "," + str(data.m_high) + "," + str(data.m_low) + "," + str(data.m_open) + "," + str(data.m_volume) + "\r"
	return result

facecatcpp = cdll.LoadLibrary(os.getcwd() + r"\\facecatcpp.dll")
cdll.argtypes = [c_char_p, c_int, c_double, c_long, c_wchar_p]

#调用C++计算指标
#formula 公式
#datas 数据
def calculateFormula(formula, data):
	recvData = create_string_buffer(1024 * 1024 * 10)
	sendStr = securityDatasToStr(datas)
	facecatcpp.calcFormula(c_char_p(formula.encode('utf-8')), c_char_p(sendStr.encode('utf-8')), recvData)
	return str(recvData.value, encoding="gbk")

#读取指标公式
file0 = open(os.getcwd() + "\\指数平滑异同平均线(MACD).js")
formulaStr = file0.read()
file0.close()

try:
	s = requests.Session()
	s.mount('http://', HTTPAdapter(max_retries=3))
	response = s.get('http://quotes.money.163.com/service/chddata.html?code=0000001', timeout=5)
	text = response.text
	strs = text.split("\r\n")
	strLen = len(strs)
	pos = strLen - 2
	#拼凑数据
	datas = []
	for i in range(0, strLen - 3):
		subStrs = strs[pos].split(",")
		if(len(subStrs) > 8):
			data = SecurityData()
			data.m_date = i
			data.m_close = float(subStrs[3])
			data.m_high = float(subStrs[4])
			data.m_low = float(subStrs[5])
			data.m_open = float(subStrs[6])
			data.m_volume = float(subStrs[11])
			datas.append(data)
		pos = pos - 1
	#计算指标
	result = calculateFormula(formulaStr, datas)
	print(result)
except requests.exceptions.RequestException as e:
	print(e)
