__author__='callMeBin'
#encoding=utf-8

'''
目标：利用天眼查查询公司的相关信息
'''

import requests
from bs4 import BeautifulSoup
import re
import codecs

page = 'p1'
BASE_URL = r'https://shaoguan.tianyancha.com/search/'+page+'?key=%E9%9F%B6%E5%85%B3'
print(BASE_URL)

#返回页面内容
def getPage(BASE_URL):
	headers = {'User-Agent':'Mozilla/4.0(compatible;MSIE 5.5; Windows NT)'}
	data = requests.get(BASE_URL,headers=headers)
	dataContent = str(data.content,'utf-8')
	#print(data.encoding)
	#print(str(data.content,'utf-8'))
	return dataContent

#传入页面，筛选Address
def getContentAddress(dataContent):
	#初始化SOUP实例对象
	soup = BeautifulSoup(dataContent,'lxml')
	#找出result-list
	result_list_soup = soup.find('div',attrs={'class':'result-list'})
	#print(result_list_soup)
	




def main():
	getContentAddress(getPage(BASE_URL))


if __name__=='__main__':
	main()