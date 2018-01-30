#!/user/bin/env python
#encoding=utf-8

'''
目标：
	爬取250条top电影信息进阶版，把数据保存到excel中
'''

import requests
from bs4 import BeautifulSoup
import codecs
import re
#excel需要用到的两个模块
import xlwt
import xlrd
import os

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

	#把数据保存到excel
def saveToExcel(informations):
	i=1
	#创建一个excel
	file_excel = xlwt.Workbook(encoding='utf-8',style_compression=0)
	#新建一个sheet,参数cell_overwrite_ok=True保证数据可以接着写下去
	sheet = file_excel.add_sheet('top250',cell_overwrite_ok=True)
	index = ['电影名称','电影评分','url地址','简介','信息']
	#生成第一行
	for j in range(0,len(index)):
		sheet.write(0,j,index[j])
	#获取数据组的长度
	data_length = len(informations)
	#填充数据
	for item in informations:
		for j in range(0,len(item)):
			sheet.write(i,j,item[j])
		i=i+1	
	file_excel.save(r'C:/Users/SleepAutumnD/Desktop/topMovies250.xlsx')


#程序入口
def main():
	url = BASE_URL
	#SleepAutumnD|LENOVO
	#把250条信息保存到列表中
	pool =[]
	while url:
		data=getPage(url)
		informations,url = getContent(data)
		for item in informations:
			pool.append(item)
	saveToExcel(pool)


if __name__ =='__main__':
	main()