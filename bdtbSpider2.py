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
				topic_url = topic_span.find('a').get('href')
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


	#获取帖子里的html
	def getPosts(self):
		pass
	#获取帖子里的信息
	def getPostContent(self):
		pass

	def start(self):
		key_word = input()
		page = self.getPage(key_word)
		libaray = self.getContent(page)
		for item in libaray:
			print(item[0],item[1])



spider_bdtb2 = bdtbSpider2()
spider_bdtb2.start()
