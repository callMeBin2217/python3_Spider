__author__='callMeBin'
#-*- coding:utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector

from douban_new_movie.items import DoubanNewMovieItem


class DoubanNewMovieSpiderByScrapy(Spider):
	name = "douban_new_movie_spiderByScrapy"

	#允许搜索的范围
	allowed_domains = ["movie.douban.com"]

	#开始搜索的地址
	start_urls = ["https://movie.douban.com/chart"]

	def parse(self,response):
		#初始化一个Selector对象，传入页面html
		sel = Selector(response)
		#print(response.body)
		#把数据保存到items容器中，初始化item对象
		item = DoubanNewMovieItem()
		#xpath获取需要的内容;extract()把返回SelectList对象转成list
		movie_name = sel.xpath("//div[@class='pl2']/a").extract()
		movie_url = sel.xpath("//div[@class='pl2']/a/@href").extract()
		movie_star = sel.xpath("//div[@class='pl2']/div/span[@class='rating_nums']/text()").extract()

		#使用迭代器
		item['movie_name'] = [n for n in movie_name ]
		item['movie_star'] = [n for n in movie_star]
		item['movie_url'] = [n for n in movie_url]

		#每次调用在生成
		yield item
		print(movie_name,movie_url,movie_star)