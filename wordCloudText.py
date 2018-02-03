__author__='callMeBin'
#!/usr/bin/env Python
# coding=utf-8
'''
爬取豆瓣神秘巨星评论，生成词云
使用requests,BeautifuSoup,wordCloud,jieba
'''
import re
import requests
import jieba
import numpy as np
import codecs
import matplotlib
from bs4 import BeautifulSoup
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
import pandas as pd
import time
from pandas import Series,DataFrame

#获取材料

#获取网页html
def getPage(pageIndex):
	BASE_URL = r'https://movie.douban.com/subject/26942674/comments?start='+str(pageIndex)+'&sort=new_score&status=P'
	headers = {'User-Agent':'Mozilla/4.0(compatible;MSIE 5.5; Windows NT)','Referer':'https://www.douban.com/','Connection':'keep-alive','Content-Type':'application/x-www-form-urlencoded'}
	cookies = {'Cookie':r'ue="343603146@qq.com"; bid=ZmsJT-NnThE; __yadk_uid=QNpTyMZy9BvgFWoLDQS7EPUpBEJjGCvT; ll="118285"; __guid=236236167.3699603969997323300.1513659402099.4944; ps=y; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1517657801%2C%22https%3A%2F%2Faccounts.douban.com%2Fregister_success%22%5D; _ga=GA1.2.1067068613.1511059876; _gid=GA1.2.873571113.1517657823; _vwo_uuid_v2=54E85FFA35619F83DD84A0E933D9B288|a42b9b84373b2ff34a437920f4181cc3; push_noty_num=0; push_doumail_num=0; ap=1; _pk_id.100001.8cb4=74f57e66a8382434.1511059875.4.1517658431.1513659403.; _pk_ses.100001.8cb4=*; __utmt=1; __utma=30149280.1067068613.1511059876.1517648276.1517655915.12; __utmb=30149280.9.10.1517655915; __utmc=30149280; __utmz=30149280.1517655915.12.9.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.17347'}
	proxies = {'http':'27.19.170.86:8118','http':'121.31.101.119:8123','http':'60.174.74.40:8118'}
	pageData = requests.get(BASE_URL,headers = headers,cookies=cookies,proxies=proxies).content
	return pageData


#获取网页的评论信息
def getContent(pageData):
	soup = BeautifulSoup(pageData,'lxml')
	#找出div列表
	div_data = soup.find('div',attrs={'class':'mod-bd'})
	#初始化一个Libaray保存comment
	libaray = []
	for item in div_data.find_all('div',attrs={'class':'comment-item'}):
		if item:
			comment = item.find('p').getText()
			libaray.append(comment)
	return libaray


#清洗数据并保存到txt中
def clearData():
	new_contents =[]
	new_info =''
	with codecs.open(r'C:/Users/SleepAutumnD/Desktop/secretStar2.txt','w+',encoding='utf-8') as fp:
		for i in range(240,300,20):
			pagedata = getPage(i)
			time.sleep(20)
			content = getContent(pagedata)
			#print(content)
			for item in content:
				#清洗数据,去掉标点符号
				pattern = re.compile(r'[\u4e00-\u9fa5a-zA-Z0-9]')
				new_info = re.findall(pattern,item)
				clear_data = ''.join(new_info)
				#print(clear_data)
				new_contents.append(clear_data)
		#print(len(new_contents))
		#print(new_contents[-1])
		for j in range(0,len(new_contents)):
			try:
				fp.write(new_contents[j])
			except IOError as e:
				print(e.reason)
		fp.close()

'''
-----------------------------------------
制作词云部分
'''
def makeWordCloud():
	with open(r'C:/Users/SleepAutumnD/Desktop/secretStar2.txt','r',encoding='utf-8') as f:
		data = f.read()
	#print(data)
	#使用结巴分词进行中文分词
	segment = jieba.lcut(str(data))
	words_df = DataFrame({'segment':segment})
	#去掉停用词,quoting=3全不引用
	stopwords = pd.read_csv(r'C:/Users/SleepAutumnD/Desktop/stopwords.txt',index_col=False,quoting=3,sep='\t',names=['stopword'],encoding='utf-8')
	words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
	#统计词频
	words_stat = words_df.groupby(by=['segment'])['segment'].agg({'计数':np.size})
	words_stat = words_stat.reset_index().sort_values(by=['计数'],ascending=False)
	#用词云进行显示
	back_img = plt.imread(r'C:/Users/SleepAutumnD/Desktop/color.jpg')
	img_color = ImageColorGenerator(back_img)
	wordcloud = WordCloud(mask=back_img,font_path='simhei.ttf',background_color='white',max_font_size=100,min_font_size=20,random_state=42)
	word_frequence = {x[0]:x[1] for x in words_stat.head(1000).values}


	wordcloud = wordcloud.fit_words(word_frequence)
	plt.axis('off')
	plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0)
	plt.imshow(wordcloud.recolor(color_func=img_color))

def main():
	clearData()
	makeWordCloud()

if __name__ =='__main__':
	main()