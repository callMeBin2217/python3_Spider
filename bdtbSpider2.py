__author__='callMeBin'
#!/usr/bin/env python3
#-*- coding:utf-8 -*-


'''百度贴吧爬虫进阶版：
    从贴吧主页开始---->通过关键词----->关键词贴吧----->首页所有URL合集------>分别爬取URL集合(形成文件)
    使用beautifulSoap,requests
'''
import re
from bs4 import BeautifulSoup
import urllib
import requests
import urllib.request

#爬取贴吧帖子（标题和各楼层内容）

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

#百度贴吧帖子类
class bdtbSpider(object):
	"""传入基础地址，是否只看楼主参数"""
	def __init__(self, baseUrl,seeLz):
		#super(bdtbSpider, self,).__init()
		self.baseUrl = baseUrl
		self.seeLz = '?see_lz'+str(seeLz) #0:否；1：是
		self.tool = Tool()
		#初始化一个title
		self.defaultTitle = 'unknown_Title'
		#全局file，用于写入文件
		self.file = None
		#楼层标号，初始为1
		self.floor = 1

	#传入页码，获取当前页码的html页面
	def getPage(self,pageNum):
		try:
			#构建url
			url = self.baseUrl+self.seeLz+'&pn='+str(pageNum)
			#初始化request对象
			request = urllib.request.Request(url)
			#初始化response对象
			response = urllib.request.urlopen(request)
			#返回该页面html内容
			return response.read().decode('utf-8')
		except urllib.request.URLError as e:
			if hasattr(e,'reason'):
				print(r'连接错误:',e.reason)
				return None


	#获取帖子的标题
	def getTitle(self):
		pageNum = 1
		content = self.getPage(pageNum)
		#正则表达式筛选标题
		patternTitle = re.compile(r'<h\d class="core_title_txt.*?>(.*?)</h\d>',re.S)
		resultTitle = re.search(patternTitle,content)
		#返回标题
		if resultTitle:
			return resultTitle.group(1).strip()
		else:
			return self.defaultTitle

	#获取帖子总页数，总回复数（没什么用，但是也把他用正则筛选出来了~）
	def getNum(self):
		content = self.getPage(1)
		#正则表达式筛选总页数
		patternNum = re.compile(r'<li class="l_reply_num".*?><span.*?>(.*?)</span.*?<span.*?>(.*?)</span>',re.S)
		resultNum = re.search(patternNum,content)
		#返回总页数
		if resultNum:
			return resultNum.group(2).strip()
		else:
			return None

	#获取当前页面每层楼的内容,传入页面内容html,返回内容集合
	def getCurrentPageContent(self,content):
		patternContent = re.compile(r'<div id="post_content_.*?">(.*?)</div>',re.S)
		items = re.findall(patternContent,content)
		#初始化一个内容图书馆list，用于存放每一页的内容
		contentLibarary = []
		for item in items:
			#将文本进行去除标签处理
			new_content = self.tool.replace(item)+'\n'
			#把处理后的文本放进contentLibarary
			contentLibarary.append(new_content)
		return contentLibarary

	#新内容知识，保存信息到文本
	
	#设置文本标题，把帖子标题作为文本标题
	def setFileName(self,title):
			path = r'C:/Users/LENOVO/Desktop/aaa/'+title+'.txt'
			self.file = open(path,"w+",encoding='utf-8')

	#向文件写入每一楼信息
	def writeData(self,contentLibarary):
		for item in contentLibarary:
			#楼之间分隔符
			foolLine = '\n'+str(self.floor)+u"-----------------------"+'\n'
			try:
				self.file.write(foolLine)
				self.file.write(item)
				self.floor +=1
			except IOError as e:
				if hasattr(e,'reason'):
					print(r'连接错误:',e.reason)
					return None

	#程序入口
	def start(self):
		pageNum = self.getNum()
		title = self.getTitle()
		self.setFileName(title)
		if pageNum==None:
			print('URL失效')
			return None
		try:
			print('该帖子共'+str(pageNum)+'页')
			#循环加载所有页面
			for i in range(1,int(pageNum)+1):
				print('正在写入第'+str(i)+'页数据')
				page = self.getPage(i)
				contents = self.getCurrentPageContent(page)
				self.writeData(contents)
		except IOError as e:
			print('写入异常',e.reason)
		finally:
			self.file.close()
			print('写入任务完成')



#贴吧首页类
class bdtbSpider2():

	def __init__(self):
		self.BASE_URL = r'http://tieba.baidu.com/f?ie=utf-8'
		self.GOUZHAO_URL = r'https://tieba.baidu.com'

	#获取贴吧首页HTML
	def getPage(self,keyWord):
		url = self.BASE_URL+'&kw='+urllib.parse.quote(str(keyWord))
		data = requests.get(url).content
		return data

	#获取贴吧首页信息(帖子标题和链接)
	def getContent(self,data):
		soup = BeautifulSoup(data,'lxml')
		#初始化一个全局list保存
		libaray = []
		#保存今日话题
		try:
			topic_span = soup.find('span',attrs={'class':'listThreadTitle inlineBlock'})
			if topic_span :
				topic_title = topic_span.find('a').getText().strip()
				topic_url = r'https:'+topic_span.find('a').get('href')
				topic_data = (topic_title,topic_url)
				libaray.append(topic_data)
			#找出ul
			tieba_list = soup.find('ul',attrs={'class':'threadlist_bright j_threadlist_bright'})
			#保存置顶的
			top_list = tieba_list.find('ul',attrs={'class':'thread_top_list'})
			if top_list :
				for item in top_list.find_all('li',attrs={'class':' j_thread_list thread_top j_thread_list clearfix'}):
					#detail = item.find('div',attrs={'class':'threadlist_title pull_left j_th_tit '})
					title = item.find('a',attrs={'class':'j_th_tit '}).getText()
					url = self.GOUZHAO_URL+item.find('a',attrs={'class':'j_th_tit '}).get('href')
					new_data = (title,url)
					libaray.append(new_data)
			#保存非置顶
			for item in tieba_list.find_all('li',attrs={'class':' j_thread_list clearfix'}):
				title = item.find('a',attrs={'class':'j_th_tit '}).getText()
				url = self.GOUZHAO_URL+item.find('a',attrs={'class':'j_th_tit '}).get('href')
				new_data = (title,url)
				libaray.append(new_data)

			return libaray
		except Exception as e:
			print(e)



	def start(self):
		key_word = input()
		page = self.getPage(key_word)
		libaray = self.getContent(page)
		for item in libaray:
			spider = bdtbSpider(item[1],0)
			spider.start()
			




spider_bdtb2 = bdtbSpider2()
spider_bdtb2.start()
