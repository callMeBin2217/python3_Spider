#!/user/bin/env python
#encodding=utf-8

'''
目标：利用requests库和beautifulSoap爬取豆瓣top250电影信息(名字、评分、链接、简介)
需解决问题：
         1.伪装成浏览器，绕过服务器对爬虫的识别
'''

import requests
from bs4 import beautifulSoup4

BASE_URL = r'http://movie.douban.com/top250/'

#返回页面内容
def getPage(url):
	headers = {'User-Agent':'Mozilla/4.0(compatible;MSIE 5.5; Windows NT)'}
	data = requests.get(url,headers=headers).content
	return data

#传入页码，筛选需要的信息
def getContent(data):
	#初始化soup实例对象
	soup = BeautifulSoup4(data)
	#找出ol
	movie_list_soup = soup.find('ol',attrs={'class':'grid_view'})
	#初始化一个用于存放所有电影信息的libaray
	libaray = []
	for item in movie_list_soup:
		#从ol中取出详情
		detail = item.find('div',attrs={'class':'info'})
		#取出名字
		movie_name = detail.find('span',attrs={'class':'title'}).getText()
		#取出评分
		movie_score = detail.find('span',attrs={'class':'rating_num'}).getText()
		#取出链接
		movie_url = detail.find('a').get('href')
		#取出简介
		movie_comment = detail.find('span',attrs={'class':'inq'}).getText()
		#把四项信息组成一个tuple，传入libaray
		data_tuple = (movie_name,movie_score,movie_url,movie_comment)
		libaray.append(data_tuple)

	#进入下一页
	next_page = soup.find('span',attrs={})


def main():
	print(getPage(BASE_URL))

if __name__ =='__main__':
	main()