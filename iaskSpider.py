__author__='callMeBin'
#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#encoding:utf-8

import urllib
import urllib.request
import re
#解决中文乱码
import sys
import importlib 
importlib.reload(sys) 

'''
目标：
1.实现输入需要询问的问题的关键词，返回前10页所有询问，并保存到txt文档中
2.保存的信息有：问题：问题的链接
'''



class iaskSpider(object):

	def __init__(self,keyWorld):
		#super(iaskSpider,self,).__init__()
		self.pageIndex = 1
		#self.user_agent = 'Mozilla/4.0(compatible;MSIE 5.5; Windows NT)'
		#self.headers = {'User_Agent':user_agent}
		self.enable = False
		self.base_url = r'https://iask.sina.com.cn'
		self.keyWorld = keyWorld
		#url中是不允许出现中文字符的，这时候就改用urllib.parse.quote方法对中文字符进行转换。
		self.searchWord = '/search?searchWord='+urllib.parse.quote(str(keyWorld))
		#初始化一个title
		self.defaultTitle = 'unknown_Title'
		#全局file，用于写入文件
		self.file = None
		#楼层标号，初始为1
		self.floor = 1


	#根据页码获取当页内容,返回内容
	def getPage(self,pageIndex):
		try:
			#https://iask.sina.com.cn/search?searchWord=python&page=1
			url = self.base_url+self.searchWord+'&page='+str(pageIndex)
			print(url)
			request = urllib.request.Request(url)
			response = urllib.request.urlopen(request)
			return response.read().decode('utf-8')
		except urllib.request.URLError as e :
			if hasattr(e,'reason'):
				print(r'链接错误',e.reason)
				return None


	def getContent(self,page):
		patternContent = re.compile(r'<p class="title">[\s\S]*?<a href="(.*?)".*?>[\s\S]*?(.*?)</a',re.S)
		items = re.findall(patternContent,page)
		#储存器
		libaray = []
		#取掉<span>
		replaceSpan  = re.compile(r'<span.*?>|</span>')
		for item in items:
			#item返回的是一个tuple
			new_item1 = re.sub(replaceSpan,"",item[1])
			new_tuple = (item[0],new_item1)
			libaray.append(new_tuple)
		return libaray


	def setFileTitle(self,title):
		'''文件要存放的地址'''
		#path = r'C:/Users/LENOVO/Desktop/'+title+'.txt'
		path=r'C:/Users/SleepAutumnD/Desktop/'+title+'.txt'
		print(path)
		self.file = open(path,'w+')


	def writeData(self,libaray):
		for item in libaray:
			foolLine = '\n'+str(self.floor)+u'=========================='+'\n'
			try:
				self.file.write(foolLine)
				#构造字符串
				to_write = '问题: '+str(item[1]).strip()+'\n'+'url地址: '+self.base_url+str(item[0]).strip()+'\n'
				self.file.write(to_write)
				self.floor +=1
			except IOError as e:
				if hasattr(e,'reason'):
					print(r'链接错误',e.reason)
					return None

	def start(self):
		pageNum = 3 
		title = self.keyWorld
		self.setFileTitle(title)
		try:
			for i in range(1,pageNum+1):
				print('正在写入第'+str(i)+'页数据')
				page = self.getPage(i)
				contents = self.getContent(page)
				self.writeData(contents)
		except IOError as e:
			print(r'写入异常',e.reason)
		finally:
			self.file.close()
			print('写入完成')

ask = 'python'
spider_iask = iaskSpider(ask)
spider_iask.start()

