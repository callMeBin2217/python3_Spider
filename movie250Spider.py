#!/user/bin/env python
#encoding=utf-8

'''
目标：利用requests库和beautifulSoap爬取豆瓣top250电影信息(名字、评分、链接、简介)
需解决问题：
         1.伪装成浏览器，绕过服务器对爬虫的识别
'''

import requests
from bs4 import BeautifulSoup
import codecs
import re

BASE_URL = r'http://movie.douban.com/top250/'

#返回页面内容
def getPage(url):
	headers = {'User-Agent':'Mozilla/4.0(compatible;MSIE 5.5; Windows NT)'}
	data = requests.get(url,headers=headers).content
	return data

#传入页码，筛选需要的信息
def getContent(data):
	#初始化soup实例对象
	soup = BeautifulSoup(data,'lxml')
	#找出ol
	movie_list_soup = soup.find('ol',attrs={'class':'grid_view'})
	#初始化一个用于存放所有电影信息的libaray
	libaray = []
	for item in movie_list_soup.find_all('li'):
		#从ol中取出详情
		detail = item.find('div',attrs={'class':'info'})
		#取出名字
		movie_name = detail.find('span',attrs={'class':'title'}).getText()
		#取出评分
		movie_score = detail.find('span',attrs={'class':'rating_num'}).getText()
		#取出链接
		movie_url = detail.find('a').get('href')
		#取出简介,有些没有简介，需要做非空判断
		if detail.find('span',attrs={'class':'inq'}) != None:
			movie_comment = detail.find('span',attrs={'class':'inq'}).getText()
		else:
			movie_comment = 'None Comment'
		#取出上映时间、发行国家、电影类型、导演等
		movie_info = detail.find('p',attrs={'class':""}).getText().strip()
		movie_info = movie_info.replace("<br>","")

		#把四项信息组成一个tuple，传入libaray
		data_tuple = (movie_name,movie_score,movie_url,movie_comment,movie_info)
		libaray.append(data_tuple)

	#进入下一页
	next_page = soup.find('span',attrs={'class':'next'}).find('a')
	if next_page:
		#返回libaray和下一页的url
		return libaray,BASE_URL+next_page.get('href')
	return libaray,None


#程序入口
def main():
	url = BASE_URL
	with codecs.open(r'C:/Users/LENOVO/Desktop/topMovies250.txt','w+',encoding='utf-8') as fp:
		while url:
			data = getPage(url)
			informations,url = getContent(data)
			for item in informations:
				info_str = "电影名称: %s \r\n电影评分: %s \r\n地址: %s \r\n简介: %s \r\n%s \r\n"%(item[0],item[1],item[2],item[3],item[4])
				try:
					fp.write(info_str+'\r\n')
				except IOError as e:
					print(e.reason)
		fp.close()


if __name__ =='__main__':
	main()