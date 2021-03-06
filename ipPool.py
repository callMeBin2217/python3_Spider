__author__='callMeBin'
#-*-coding:utf-8-*-

'''
目标：爬取 国内高匿免费HTTP代理网页首页IP，构建自用IP代理池
http://www.xicidaili.com/nn/
'''
import requests
from bs4 import BeautifulSoup
import random

class ipPool(object):
	def __init__(self):
		self.base_url = r'http://www.xicidaili.com/nn/'
		self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    	}
		self.ipList=[]


	#获取首页所有内容
	def getPage(self):
		req = requests.get(self.base_url,headers=self.headers)
		#print(req.text)
		return req.text


	#使用beautifulSoup获取所需内容
	def getIpList(self,data):
		soup = BeautifulSoup(data,'lxml')
		tr_list = soup.find_all('tr')
		for i in range(1,len(tr_list)):
			info_tr = tr_list[i]
			#print(info_tr)
			info_td = info_tr.find_all('td')
			tempUrl = str.lower(info_td[5].text)+'://'+info_td[1].text+':'+info_td[2].text
			#print(tempUrl)
			tempInfo = (str.lower(info_td[5].text),tempUrl) #返回样例 (http,http://192.168.1.1:80)
			#ipList.append(tempInfo)
			#print(ipList)
			self.ipList.append(tempInfo)
		return self.ipList

		#随机返回一个Ip
	def get_random_ip(self,ipList):
		pro = random.choice(ipList)
		proxies=pro[1]
		return proxies



if __name__ == '__main__':
	spider = ipPool()
	page = spider.getPage()
	ipList=spider.getIpList(page)
	print(ipList)
	proxies = spider.get_random_ip(ipList)
	print(proxies)






