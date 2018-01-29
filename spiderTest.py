# -*- coding: utf-8 -*-
import urllib.request
import urllib

#1.尝试模拟百度网盘登录并获取网页内容


#构建账号密码信息dict
values = {'username':'bbh953838','password':'gdfshb95'}
data = urllib.parse.urlencode(values)
#构建header
user_agent = r'Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'
headers = {'User-Agent':user_agent,'Referer':'https://yun.baidu.com/'}
#构建request
#request = urllib.request.Request(r'https://yun.baidu.com/',data)
request = urllib.request.Request(r'https://yun.baidu.com/rest/2.0/membership/user?method=query&reminder=1&channel=chunlei&web=1&app_id=250528&bdstoken=ad51e946113a6756b08022fce7fa8c8d&logid=MTUxNjU4ODg5MDUyMDAuODI5Mzg5Nzc4MjEwODQ1Mw==&clienttype=0',headers=headers)
#构建response
response = urllib.request.urlopen(request)
print(response.read())


#URLError异常处理
try:
	response = urllib.request.urlopen(r'https://yun.baidu.com/rest/2.0/membership/user?method=query&reminder=1&channel=chunlei&web=1&app_id=250528&bdstoken=ad51e946113a6756b08022fce7fa8c8d&logid=MTUxNjU4ODg5MDUyMDAuODI5Mzg5Nzc4MjEwODQ1Mw==&clienttype=0')
except urllib.error.URLError as e:
	print(e.reason)
	print(e.code)
	
#Cookie的使用	
import urllib
import urllib.request
import http.cookiejar
#获取Cookie保存到变量
#声明一个CookieJar对象实例来保存cookie
cookie = http.cookiejar.CookieJar()
#利用urllib.request中HTTPCookieProcessor(cookie)
handler = urllib.request.HTTPCookieProcessor(cookie)
#通过handler来构建opener
opener = urllib.request.build_opener(handler)
#此处的open方法同urllib.request的urlopen方法，也可以传入request
response = opener.open(r'http://www.baidu.com')
for item in cookie:
	print('name = '+item.name)
	print('value = '+item.value)
#保存cookie到文件
filename = 'cookie.txt'
cookie_save = http.cookiejar.MozillaCookieJar(filename)
cookie_save.save(ignore_discard=True,ignore_expires=True)

#从文件中获取Cookie并访问
#创建MozillaCookieJar实例对象
c = http.cookiejar.MozillaCookieJar()
#从文件中读取cookie内容到变量
c.load('cookie.txt',ignore_discard=True,ignore_expires=True)
#创建请求request
req = urllib.request.Request(r'http://www.baidu.com')
#利用urllib.request中build_opener方法创建一个opener
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(c))
rep = opener.open(req)
print(response.read())


#抓取嗅事百科(一页内容)
import urllib
import urllib.request
import re
page = 1
url = r'https://www.qiushibaike.com/hot/page'+str(page)
user_agent = 'Mozilla/4.0(compatible;MSIE 5.5; Windows NT)'
headers = {'User-Agent':user_agent}
try:
	request = urllib.request.Request(url,headers=headers)
	response = urllib.request.urlopen(request)
	content = response.read().decode('utf-8')
	pattern = re.compile(r'h2>(.*?)</h.*?<div.*?<span>(.*?)</.*?>',re.S|re.M)
	items = re.findall(pattern,content)
	pageLibrary=[]
	for item in items:
		pageLibrary.append([item[0].strip(),item[1].strip()])
		print(item[0].strip(),item[1].strip())
		#print(pageLibrary)
except urllib.request.URLError as e:
	if hasattr(e,'code'):
		print(e.code)
	if hasattr(e,'reason'):
		print(e.reason)
		
		
#抓取贴吧一个帖子上的内容（一页内容）
import urllib
import urllib.request
import re
page = 1
baseUrl = r'https://tieba.baidu.com/p/2687476192'
seeLZ = 0
try:
	url = baseUrl+'?see_lz='+str(seeLZ)+'&pn='+str(page)
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)
	content = response.read().decode('utf-8')
	#获取帖子标题
	patternTitle = re.compile(r'<h\d class="core_title_txt.*?>(.*?)</h\d>',re.S)
	resultTitle = re.search(patternTitle,content)
	print(resultTitle.group(1).strip())
	#获取帖子回复数和总页数
	patternNum = re.compile(r'<li class="l_reply_num".*?><span.*?>(.*?)</span.*?<span.*?>(.*?)</span>',re.S)
	resultNum =re.search(patternNum,content)
	print(resultNum.group(1).strip(),resultNum.group(2).strip())
	#获取帖子每层楼内容
	patternContent = re.compile(r'<div id="post_content_.*?">(.*?)</div>',re.S)
	items = re.findall(patternContent,content)
	tool = Tool()
	for item in items:
		print('\n',tool.replace(item),'\n')
except urllib.request.URLError as e:
	if hasattr(e,'reason'):
		print(e.reason)
		
		
		
#处理页面标签类
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
		
