#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 12:21:27 2017

@author: Song
"""
import requests
from bs4 import BeautifulSoup
import codecs

class UrlManager(object):
	def __init__(self):
		print('进入URL管理器处理url集合！')
		self.new_urls = set() # 未抓取的urls
		self.old_urls = set() # 已抓取的urls

	def has_new_url(self):
		'''判断是否有未抓取的urls'''
		return self.new_url_size() != 0  # 返回True或False

## 问题：类中函数调用，在定义之前，可以吗？为什么？

	def get_new_url(self):
		'''从未抓取url集合获得：取一个url,同时将此url转到已抓取集合中'''
		new_url = self.new_urls.pop()  # 通过集合pop方法获得一个url
		self.old_urls.add(new_url)  # set的add()方法存储抓取过的url
		return new_url

	def add_new_url(self, url):
		'''将新的单个url添加到未抓取的url集合中'''
		if url is None:  # 空判断
			return
		if url not in self.new_urls and url not in self.old_urls:  # 查重判断
			self.new_urls.add(url)

	def add_new_urls(self, urls):
		'''将新的urls添加到未抓取的urls集合中'''
		if urls is None or len(urls) == 0:
			return
		for url in urls:
			self.add_new_url(url)

	def new_url_size(self):
		return len(self.new_urls)

	def old_url_size(self):
		return len(self.old_urls)

class HtmlDownloader(object):
	'''实现请求，返回响应'''
	print('进入下载器下载网页！')
	def download(self, url):
		if url is None:
			return None
		user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"
		headers = {"User_Agent":user_agent}
		r = requests.get(url, headers=headers)
		if r.status_code==200:
			print('所请求的网页编码为：{}'.format(r.encoding))
			r.encoding='utf-8'
			return r.text  # 问题：为什么不返回r.content
		return None # 这一句有什么作用？

class HtmlParser(object):
	def __init__(self):
		print('进入网页解析器解析网页！')

	def parser(self, page_url, html_content):
		result = []
		data = {}
		if  page_url is None or html_content is None:
			return
		# soup = BeautifulSoup(page_url,'lxml',from_encoding='utf-8')
		soup = BeautifulSoup(html_content,'lxml')  # 这里要解析的应该是，requests返回的r.text。
		# print('Soup的结果为：%s'%soup.select('a.cb'))
		# print(len(soup.select('a.cb')))  # 列表长度为10，可以循环得到值。
		for q in soup.select('a.cb'):
			title = q.text
			new_urls = q.get('href').replace('./', 'http://www.xf.gov.cn/network/zfxfxx/')
			data = {'title':title,'new_urls':new_urls}
			result.append(data)
			# return title, new_urls  # 这里只返回了一次，返回一次后循环就结了。
		return result

	def _get_new_urls(self, page_url, soup):
		'''获得从root_url中提取的url'''
		pass

	def _get_new_data(selfs, page_url, soup):
		'''从提取的链接中获得数据'''
		pass

class DataOutput(object):

	def __init__(self):
		print('进入数据存储器存储数据！')
		self.datas=[]

	def store_data(self, data):
		if data is None:
			return
		self.datas.append(data)

	def output_html(self):
		for data in self.datas:
			print(data)  # 传入过来的data是列表，要想全部打印，必须循环
			with codecs.open('letters.html', 'a', encoding='gbk') as fout:
				fout.write("<html>")
				fout.write("<body>")
				fout.write("<table width='95%' cellspacing='3' cellpadding='3' border='1'>")
				fout.write("<thead>")
				fout.write(
					"<td style='line-height:15px; height:28px;font-size:14px;padding-top:10px;padding-bottom:10px' align='center'>标题</td>")
				fout.write(
					"<td style='line-height:15px; height:28px;font-size:14px;padding-top:10px;padding-bottom:10px' align='center'>链接</td>")
				fout.write("</thead>")
				for data in data:
					fout.write("<tr>")
					fout.write(
						"<td style='line-height:15px; height:28px;font-size:14px;padding-top:10px;padding-bottom:10px' align='center'>%s</td>" %
						data['title'])  # 这里数据预置方式出错！
					fout.write(
						"<td style='line-height:15px; height:28px;font-size:14px;padding-top:10px;padding-bottom:10px' align='left'><a href=%s>%s</td>" % (
						data['new_urls'], data['new_urls']))
					fout.write("</tr>")
				fout.write("</table>")
				fout.write("</body>")
				fout.write("</html>")

class SpiderMan(object):

	def __init__(self):
		self.manager = UrlManager()
		self.downloader = HtmlDownloader()
		self.parser = HtmlParser()
		self.output = DataOutput()

	def crawl(self, root_url):
		# 入口URL, start_url
		self.manager.add_new_url(root_url)
		new_url = self.manager.get_new_url()
		html = self.downloader.download(new_url)  # 返回html = r.text
		print(self.parser.parser(new_url, html))
		data = self.parser.parser(new_url, html)  # 解析器传回urls:href和data:title元组
		self.output.store_data(data)  # 存储器存储data,注意这里只存储了data
		print('已经抓取%s个链接' % self.manager.old_url_size())
		self.output.output_html()

if __name__=="__main__":
	spider_man = SpiderMan()
	spider_man.crawl('http://www.xf.gov.cn/network/zfxfxx/index.shtml')
