#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re

# URL管理器
root_url = 'http://www.xf.gov.cn/network/zfxfxx/index.shtml'

# 网页下载器
def down_html(url):
	user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"
	headers = {"User_Agent": user_agent}
	r = requests.get(url, headers=headers)
	r.encoding = 'utf-8'
	html = r.text
	return html

# 网页解析器
# 首先要从index页中解析提取出详情页链接
index_page_html = down_html(root_url)
detail_urls = []
soup = BeautifulSoup(index_page_html, 'lxml')
for q in soup.select('a.cb'):
	detail_url = q.get('href').replace('./', 'http://www.xf.gov.cn/network/zfxfxx/')
	detail_urls.append(detail_url)

print(detail_urls)
print('从index页中，共提取了%s条详情页链接！'%len(detail_urls))

# 调用下载器和解析器
keys = []
for durl in detail_urls:
	print(durl)  # 每次只取一个详情页url
	detail_page_html = down_html(durl)  # 期望只取一个详情页
	print(len(detail_page_html))  # 所有结果均为一样，说明deail_page_html
	print('\n')
	# # 解析详情页，提取详情页数据
	soup = BeautifulSoup(detail_page_html, 'lxml')
	key = (soup.select('.cb.c14 > span')[0].text)[4:-1]
	# key = re.findall('\d{8}-\d{4}-\d{6}', detail_page_html)
	keys.append(key)

# print(len(keys[0]))
print(keys)

