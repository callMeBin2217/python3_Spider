__author__='callMeBin'
#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import urllib
import urllib.request
import re


'''
目标：
1.实现输入需要询问的问题的关键词，返回前10页所有询问，并保存到txt文档中
2.保存的信息有：问题：问题的链接
'''


#工具类Tool，用于把内容中的各种标签去掉，保留最原始的文字
class Tool():
	#去除img标签，7空位长空格
	removeImg = re.compile(r'<img.*?>| {7}|')
	#去除超链接标签
	removeAddr = re.compile(r'<a.*?>|</a>')
	#把换行标签换位\n
	replaceLine = re.compile(r'<tr>|<div>|</div>|</p>')
	#将表格制表<td>换位\t
	replaceTD = re.compile(r'<td>')
	#把段落开头换位\n加两个空格
	replacePara = re.compile(r'<p.*?>')
	#将换行符号或多换行符换为\n
	replaceBR = re.compile(r'<br>*')
	#将其他标签剔除
	removeExtraTag = re.compile(r'<.*?>')
	def replace(self,x):
		x = re.sub(self.removeImg,"",x)
		x = re.sub(self.removeAddr,"",x)
		x = re.sub(self.replaceLine,"\n",x)
		x = re.sub(self.replaceTD,"\t",x)
		x = re.sub(self.replacePara,"\n  ",x)
		x = re.sub(self.replaceBR,'\n',x)
		x = re.sub(self.removeExtraTag,"",x)
		return x.strip()



class iaskSpider(object):

	def __init__(self,keyWorld):
		#super(iaskSpider,self,).__init__()
		self.pageIndex = 1
		#self.user_agent = 'Mozilla/4.0(compatible;MSIE 5.5; Windows NT)'
		#self.headers = {'User_Agent':user_agent}
		self.enable = False
		self.base_url = r'https://iask.sina.com.cn'
		self.keyWorld = keyWorld
		self.searchWord = '/search?searchWord='+str(keyWorld)
		self.tool = Tool()
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
			request = urllib.request.Request(url)
			response = urllib.request.urlopen(request)
			return response.read().decode('utf-8')
		except urllib.request.URLError as e :
			if hasattr(e,'reason'):
				print(r'链接错误',e.reason)
				return None


	def getContent(self,page):
		patternContent = re.compile(r'<p class="title">[\s\S]*?<a href=(.*?)>[\s\S]*?(.*?)</a',re.S)
		items = re.findall(patternContent,page)
		#储存器
		libaray = []
		for item in items:
			#new_content = self.tool.replace(item)+'\n'
			libaray.append(item)
		return libaray


	def setFileTitle(self,title):
		path = r'C:/Users/LENOVO/Desktop/'+title+'.txt'
		print(path)
		self.file = open(path,'w+')


	def writeData(self,libaray):
		for item in libaray:
			foolLine = '\n'+str(self.floor)+u'=========================='+'\n'
			try:
				self.file.write(foolLine)
				to_write = '问题:'+str(item[1]).strip()+'url地址:'+str(item[0]).strip()+'\n'
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

