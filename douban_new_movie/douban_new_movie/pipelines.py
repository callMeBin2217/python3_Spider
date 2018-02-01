# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import sys
import re


class DoubanNewMoviePipeline(object):

	def __init__(self):
		self.file = codecs.open(r'C:/Users/LENOVO/Desktop/aaa/douban_new_movie.json',mode='wb',encoding='utf-8')


	def process_item(self, item, spider):
		line = 'the new movie list:'+'\n'

		#去掉电影名字中的多余标签
		pattern = re.compile(r'<a.*?>|<sp.*?>|</span.*?a>|\\n')
		
		for i in range(len(item['movie_name'])):
			movie_name = {'movie_name':str(item['movie_name'][i]).replace(' ','')}
			movie_name = re.sub(pattern,"",str(movie_name))
			movie_star = {'movie_star':str(item['movie_star'][i])}
			movie_url = {'movie_url':str(item['movie_url'][i])}
			line = line+ json.dumps(movie_name,ensure_ascii=False)
			line = line+ json.dumps(movie_star,ensure_ascii=False)
			line = line+ json.dumps(movie_url,ensure_ascii=False)+'\n'

		line = line + str(len(item['movie_name']))+'\n'+str(len(item['movie_star']))+'\n'+str(len(item['movie_url']))
		self.file.write(line)


	def close_spider(self,spider):
		self.file.close()

