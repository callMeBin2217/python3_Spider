__author__='callMeBin'
#-*-coding:utf-8-*-
'''
目标：学习简单爬取豆瓣人物影集图片(一页)，并保存到文件夹
'''
import urllib
import urllib.request
import re
import os
import time
#获取页面HTML
def getPage():
	try:
		url = r'https://movie.douban.com/celebrity/1018562/photos/'
		headers = {'User-Agent':'Mozilla/4.0(compatible;MSIE 5.5; Windows NT)'}
		request = urllib.request.Request(url,headers=headers)
		response = urllib.request.urlopen(request)
		#print(response.read().decode('utf-8'))
		return response.read().decode('utf-8')
	except urllib.request.URLError as e:
		print(e)
#筛选出图片,返回一个图片集LIST
def getImg(page):
	#注意!网页上显示图片的格式是webp，但是下载下来的html页面里，图片格式就成了.jpg,所以正则需要匹配.jpg
	pattern = re.compile(r'https://.*?.jpg')
	contents = re.findall(pattern,page)
	#print(page)
	#print(contents)
	return contents

#把图片保存到文件夹
def saveToDir(contents):
	#设置图片名
	img = 0
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

