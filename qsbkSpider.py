__author__='callMeBin'
#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import urllib
import urllib.request
import re

#爬去热门嗅事百科段子，包含用户名和文字
class qsbkSpider(object):
	"""docstring for qsbkSpider"""
	def __init__(self,):
		super(qsbkSpider, self).__init__()
		self.pageIndex = 1
		self.user_agent = 'Mozilla/4.0(compatible;MSIE 5.5; Windows NT)'
		#初始化headers
		self.headers = {'User-Agent':self.user_agent}
		#用于存放段子的列表,每一个元素存放一页段子数据
		self.stories = []
		#判断程序是否继续执行
		self.enable = False


	#传入某一页的索引获得页面代码
	def getPage(self,pageIndex):
		try:
			url = r'https://www.qiushibaike.com/hot/page/'+str(pageIndex)
			#构建request请求
			request = urllib.request.Request(url,headers=headers)
			#构建response
			response = urllib.request.urlopen(request)
			#通过response获取页面内容,并对内容进行‘utf-8’解码
			content = response.read().decode('utf-8')
			return content
		except urllib.request.URLError as e:
			if hasattr(e,'reason'):
				print(u'链接糗事百科失败,错误原因',e.reason)
				return None

	#传入某一页内容，返回本页段子列表
	def getPageItems(self,pageIndex):
		pageContent = self.getPage(pageIndex)
		if not pageContent:
			print('页面加载失败...')
			return None
		#编写正则表达式，筛选出用户名和内容
		pattern = re.compile(r'h2>(.*?)</h.*?<div.*?<span>(.*?)</.*?>',re.S|re.M)
		items = re.findall(pattern,pageContent)
		#初始化一个列表，储存每页的段子
		pageLibrary = []
		#遍历符合正则表达式匹配的信息
		for item in items:
			#去掉内容中的<br/>
			replaceBR = re.compile('<br/>')
			text = re.sub(replaceBR,'\n',item[1])
			pageLibrary.append([item[0].strip(),text.strip()])
		return pageLibrary


	#加载并提取页面的内容，加入到全局列表
	def loadPage(self):
		#如果当前未看的页数少于2页，则加载新一页
		if self.enable==True:
			if len(self.stories)<2:
				#获取新的一页
				pageLibrary = self.getPageItems(self.pageIndex)
				#将该页段子存放到全局list中
				if pageLibrary:
					self.stories.append(pageLibrary)
					#获取完之后页码索引+1，表示下次读取当前页的下一页
					self.pageIndex =self.pageIndex+1


	#调用该方法，每次敲回车打印输出一个段子
	def getOneStory(self,pageLibrary,page):
		#遍历每一页段子
		for story in pageLibrary:
			#等待输入
			inputSpace = input()
			#每当输入回车一次，判断一下是否要加载新页面
			self.loadPage()
			#Q判断结束
			if inputSpace.lower()=='q':
				self.enable = False
				return
			print("第%s页\t发布人: %s \n 内容: %s"%(page,story[0],story[1]))


	#程序入口
	def start(self):
		print(u'正在读取糗事百科，按回车查看新段子，q退出')
		#使变量为True，程序正常运行
		self.enable = True
		#先加载一页内容
		self.loadPage()
		#局部变量，控制当前读到第几页
		nowPage = 0
		while self.enable:
			if len(self.stories)>0:
				#从全局list中获取一页的段子
				pageLibrary = self.stories[0]
				#当前读到页数+1
				nowPage=nowPage+1
				#将全局list中第一个元素删除，表示已经取出
				del self.stories[0]
				#输出该页的段子
				self.getOneStory(pageLibrary,nowPage)


spider_qsbk = qsbkSpider()
spider_qsbk.start()
