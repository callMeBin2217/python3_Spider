__author__ = 'callMeBin'
#-*-coding:utf-8-*-

'''
目标：使用selenium+Phantomjs(Firefox)+python3+BeautifulSoup 爬取知乎某一问题下答案的图片
'''
import time
import os
import urllib.request
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#等待页面渲染完成需要的模块
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#鼠标操作类模块
from selenium.webdriver.common.action_chains import ActionChains

class zhihuImageSpider():
	def __init__(self):
		self.BASE_URL = r'https://www.zhihu.com/question/36059311'#爬女神新垣结衣
		self.driver = webdriver.Firefox()
		#设置USER-AGENT
		'''不知道为什么一用phantomJS 就会抛出 'NoneType' object is not subscriptable 异常
			
		'''
		#self.dict_list = dict(DesiredCapabilities.PHANTOMJS)
		#self.dict_list['phantomjs.page.settings.userAgent']=r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
		#self.driver = webdriver.PhantomJS() #初始化PhantomJS



	def getPage(self):
		'''
		由于知乎问题下答案使用下拉滚条动态加载内容，所以先要把滚条
		下拉到底部再一次性获取页面内容
		PS.由于知乎某些问题下回答太多，单单一条JS语句难以到达最底部，加载所有回答
		'''
		#获取网页
		try:
			self.driver.get(self.BASE_URL)
			time.sleep(20)#设置等待时间，等driver完全加载
			#设置JS，滑动到底部
			js = 'var q=document.documentElement.scrollTop=100000000'#自己调，还未找到可行办法，直达底部
			self.driver.execute_script(js)#加载JS
			time.sleep(60)
		except Exception as e:
			print(e)
		return self.driver.page_source


	def getImage(self,data):
		soup = BeautifulSoup(data,'lxml')
		content_list = soup.find('div',attrs={'class':'List'})
		img_list = []
		for item in content_list.find_all('figure'):
			img = item.find('img')['src']
			img_list.append(img)
		print(len(img_list))
		print(img_list)
		return img_list

	def saveToDir(self,contents):
	#设置图片名
		img = 40
		try:
			#文件保存的位置
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
			self.driver.quit()


	#程序入口
	def main(self):
		try:
			page = self.getPage()
			imgs = self.getImage(page)
			self.saveToDir(imgs)
		except Exception as e:
			print(e)
		finally:
			self.driver.quit()
			



spider = zhihuImageSpider()
spider.main()




