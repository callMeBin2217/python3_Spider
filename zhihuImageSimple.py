__author__ = 'callMeBin'
#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import urllib
import re
import os
import time
'''
实现简单爬取知乎问题下图片，只是获取了初始化的20张图片，之后的图片是JS加载，需要以后学习
本次目的是巩固BeautifulSoup的运用
'''
def getPage(): 
	url =  'https://www.zhihu.com/question/59408786'
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
	r = requests.get(url, headers=headers).content
	return r

def getImg(data):
	soup = BeautifulSoup(data,'lxml')
	content_list = soup.find('div',attrs={'class':'List'})
	img_list = []
	for item in content_list.find_all('figure'):
		img = item.find('img')['src']
		img_list.append(img)
	return img_list

def saveToDir(contents):
	#设置图片名
	img = 40
	try:
		path = r'C:/Users/LENOVO/Desktop/img1/'
		#判断文件是否存在
		if not os.path.isdir(path):
			os.makedirs(path)
		#urlretrieve() 方法直接将远程数据下载到本地。
		for item in contents:
			paths = path + str(img) + '.jpg'
			time.sleep(3)
			urllib.request.urlretrieve(item,paths)
			img=img+1
	except Exception as e:
		print(e)

#程序入口
def start():
	page = getPage()
	imgs = getImg(page)
	saveToDir(imgs)

start()