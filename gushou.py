#-*-coding:utf8-*-
 
import re
import string
import sys
import os
import urllib
import urllib2
import requests
 
reload(sys) 
sys.setdefaultencoding('utf-8')

def changePage(gushou_url, page_num):
    page_list = []
    for num in range(int(page_num)):
        num = num + 1
        handled_url = re.sub('table/\d+','table/%s'%num,gushou_url)
        page_list.append(handled_url)
    return page_list

def getHtml(url):
    html = requests.get(url).content
    li = re.findall('(<div class="row h130">.*?<div class="row-split">)',html,re.S)
    return li

def getInfo(each):
    info = {}
    info['name'] = re.search('<a href=.*>(.*)</a>',each).group(1)
    info['rate'] = re.search('<span class="ark-value-highlight">\s+(.*)\s+</span>',each).group(1)
    info['scale'] = re.search('<a class="btn btn-.*" data-id="\d+".*>(.*)</a>',each).group(1)
    return info

def printResult(result,data):
    flag = '\xe7\xab\x8b\xe5\x8d\xb3\xe8\xb4\xad\xe4\xb9\xb0'
    if data['scale'] == flag:
        print data['name']
        print data['rate']
        result.append(float(data['rate']))

if __name__ == '__main__':
    gushou_url = 'http://jdd.jr.jd.com/product/table/0-6-0-0-0-0-0-default-1.html'
    #gushou_url = 'http://jdd.jr.jd.com/product/secondary/table/0-6-0-0-0-default-1.html'
    page_num = sys.argv[1]
    result = []
    print 'Start crawling page...'
    page_link = changePage(gushou_url,page_num)
    for url in page_link:
        print 'Handling page:' + url
        content = getHtml(url)
        for each in content:
            data = getInfo(each)
            printResult(result,data)
    print max(result)
