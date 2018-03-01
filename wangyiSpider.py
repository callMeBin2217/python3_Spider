__author__='callMeBin'
#-*-coding:utf-8-*-

'''
目标：爬取网易云音乐上某首歌的评论
'''

import os 
import base64
import time
from Crypto.Cipher import AES
import json
import requests
import chardet
import sys
import codecs
import getpass
import time
import ipPool

class EncrypUtil():
	def __init__(self):
		pass

	def createSecretKey(self,size=16):
		return (''.join(map(lambda xx:(hex(ord(xx))[2:]),str(os.urandom(size)))))[0:size]

	def aesEncrypt(self,text,secKey):
		pad = 16-len(text)%16
		text = text + pad*chr(pad)
		encryptor = AES.new(secKey,2,'0102030405060708')
		ciphertext = encryptor.encrypt(text)
		ciphertext = base64.b64encode(ciphertext)
		return ciphertext

	def rsaEncrypt(self,text,pubKey,modulus):
		text = text[::-1]
		tempHex = codecs.encode(text.encode('utf-8'),'hex')
		rs = int(tempHex,16)**int(pubKey,16)%int(modulus,16)
		return format(rs,'x').zfill(256)

	def timeStamp(self,timeNum):
		time_stamp = float(timeNum/1000)
		time_array = time.localtime(time_stamp)
		reTime = time.strftime("%Y-%m-%d %H:%M:%S",time_array)
		return reTime


class wangyiSpider(object):
	def __init__(self,id):
		#初始化一个commentList用于保存爬取下来的评论
		self.commentList = []
		self.count =1
		self.sys_name = getpass.getuser()
		self.modulus = r'00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
		self.nonce = r'0CoJUm6Qyw8W8jud'
		self.pubKey = '010001'
		self.encryptUtil = EncrypUtil()
		self.secKey = self.encryptUtil.createSecretKey(16)
		#先生成16位密钥，进行RSA加密
		self.encSecKey = self.encryptUtil.rsaEncrypt(self.secKey,self.pubKey,self.modulus)
		#需要爬取的音乐ID
		self.musicId = id
		self.BASE_URL = r"http://music.163.com/weapi/v1/resource/comments/R_SO_4_%d/"%int(self.musicId)
		self.headers = {
			'Host':'music.163.com',
			'Connection':'keep-alive',
			'Content-Length':'484',
			'Cache-Control':'max-age=0',
			'Origin':'http://music.163.com',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
			'Content-Type':'application/x-www-form-urlencoded',
			'Accept':'*/*',
			'DNT':'1',
			'Accept-Encoding':'gzip,deflate',
			'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
			'Cookie':r'__e_=1515631791549; _ntes_nnid=c88c078d22d8515e624ea4e5db7e2e0d,1515631791598; _ntes_nuid=c88c078d22d8515e624ea4e5db7e2e0d; __gads=ID=db5bcf91a4f4474a:T=1516954068:S=ALNI_MbOfciBUKkaPIihHY6CmzO6fTs5vQ; UM_distinctid=161318220f3496-0d23e92b7b7267-5d4e211f-1fa400-161318220f4711; vjuids=9a46435bb.16131822360.0.62cca3f22db48; vjlast=1516954068.1516954068.30; vinfo_n_f_l_n3=fd7c70cc0e58e199.1.0.1516954067832.0.1516954082832; usertrack=ezq0pVp4IaO0pxVxA0tGAg==; _ga=GA1.2.351628758.1517822370; JSESSIONID-WYYY=hnxY2pR6PfhsTnvYKsjgOdIb4XXuFXtDpVyOiGe8iVw4vrgoJcDYiPVnXk8%5Cu29chSP2XVv6%5C9Qf6T%2F9TNQmNsT6DoElf0UPS%2BFoaP1QRolC45d88oucu%2FGS7oAKERqGciUuAvnrRarmStKllmOvyXNI7e0hfC1nTq6Gc7%2BXoPz49d3I%3A1519350498491; _iuqxldmzr_=32; MUSIC_U=0cecdd66b7edc1a91bb1bf394983168904b6ac3c81dfa30e5c9ea3645572f5be938cc46fb4118388590e94fdac8a9bd1a70b41177f9edcea; __remember_me=true; __csrf=c60b017314ee4a58a6bbbe654fe004e7; __utma=94650624.351628758.1517822370.1519346959.1519346959.1; __utmb=94650624.13.10.1519346959; __utmc=94650624; __utmz=94650624.1519346959.1.1.utmcsr=so.com|utmccn=(referral)|utmcmd=referral|utmcct=/link'

		}



	#获取评论
	def getComment(self,offset):  
		text= {
			'username':'',
			'password':'',
			'rememberLogin':'true',
			'offset': offset
		}
		text = json.dumps(text)
		#进行两次AES加密
		encText = self.encryptUtil.aesEncrypt(self.encryptUtil.aesEncrypt(text,self.nonce).decode('utf-8'),self.secKey)
		data = {
			'params':encText,
			'encSecKey':self.encSecKey
		}
		ipSpider = ipPool()
		ipList = ipSpider.getIpList(ipSpider.getPage())
		recq = requests.post(self.BASE_URL,headers=self.headers,data=data,proxies=ipSpider.get_random_ip(ipList))
		jsonData = recq.json()
		if jsonData.get('msg',"")=="":
			self.saveToFile(jsonData) #保存到文件
			return int(jsonData['total'])
		else:
			recq = requests.post(self.BASE_URL,headers=self.headers,data=data,proxies=ipSpider.get_random_ip(ipList))


	#保存评论到文件
	def saveToFile(self,jsonData):
		try:
			for c in jsonData['comments']:
				#构造tuple 保存评论数和点赞数
				tempTuple = (c['content'].strip(),c['likedCount'])
				self.commentList.append(tempTuple)
		except Exception as e:
			with codecs.open(r'C:/Users/'+self.sys_name+'/Desktop/wyComment2.txt','w+',encoding='utf-8') as fp:
				for i in self.commentList:
					print('正在写入第 '+str(self.count)+' 条信息')
					fp.write(i[0]+'  '+str(i[1])+'\r\n ')
					self.count+=1
			print(e)

	

	def process(self,offset):
		if offset == -1:
			return
		off = offset
		total = self.getComment(off)
		print('评论的总数: '+str(total))
		if total <10000:
			while off<total:
				off +=10
				time.sleep(1)
				self.getComment(off)
		else:
			while off<=10000:
				off +=10
				time.sleep(2)
				self.getComment(off)

		with codecs.open(r'C:/Users/'+self.sys_name+'/Desktop/wyComment2.txt','w+',encoding='utf-8') as fp:
			for i in self.commentList:
				print('正在写入第 '+str(self.count)+' 条信息')
				fp.write(i[0]+'  '+str(i[1])+'\r\n ')
				self.count+=1


#默认歌曲‘白色球鞋’
def main(id='65546'):
	spider = wangyiSpider(id)
	spider.process(1)

if __name__ == '__main__':
	id = '468513829'
	main(id)




