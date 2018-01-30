# python3_Spider
学习python3也有一段时间了，最近通过学习用python3来写爬虫代码来练手，日后也会持续不断上传自己写的爬虫代码，希望大家可以相互学习
-----------------------

Learn Python3 also have a period of time, recently by learning to write Python3 code to practiced, the future will continue to upload their own code to write the crawler, I hope you can learn from each other



--------------
2018.1.26
上传了三个文件:spiderTest.py  /qsbkSpider.py(爬取嗅事百科热门) /bdtbSpider.py(爬取百度贴吧帖子内容)


-------------------
2018.1.29
上传新的项目iaskSpider.py(爬取爱问知识人)
解决：传入中文参数进url出现乱码问题；（url中是不允许出现中文字符的，这时候就改用urllib.parse.quote方法对中文字符进行转换。）
      优化正则表达式对内容的筛选

-------------------------
2018.1.30
上传新项目 movie250Spider.py(爬取豆瓣top250电影信息)
使用方法：requests,BeautifuSoap,codecs
注意：使用codecs 换行符'\n'会失效，需要用'\r\n'