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

def changePage(piaoju_url, page_num):
    page_list = []
    for num in range(int(page_num)):
        num = num + 1
        handled_url = re.sub('page=\d+','page=%s'%num,piaoju_url)
        page_list.append(handled_url)
    return page_list

def getHtml(url):
    html = requests.get(url).content
    form = re.findall('(<form.*?</form>)',html,re.S)[0]
    li = re.findall('(<li>.*?</li>)',form,re.S)
    return li

def getInfo(each):
    info = {}
    info['name'] = re.search('<h3 class="bill-goods-name">(.*)<span.*>',each).group(1)
    info['rate'] = re.search('<span>(.*)<b class="income-precent">(\d.*)<i>',each).group(2)
    info['dura'] = re.search('<b class="bill-normal">(\d.*)<i>天</i></b>',each).group(1)
    info['scale'] = re.search('<div class="process-num">(\d+).</div>',each).group(1)
    return info

def printResult(result,data):
    flag = data['scale']
    limit = data['dura']
    if flag != '100' and limit < '300':
        print data['name']
        print data['rate']
        print data['dura']
        result.append(float(data['rate']))

if __name__ == '__main__':
    piaoju_url = 'http://bill.jr.jd.com/buy/list.htm?n=0&t=0&s=0&o=0&from=&page=0'
    page_num = sys.argv[1]
    result = []
    print 'Start crawling page...'
    page_link = changePage(piaoju_url,page_num)
    for url in page_link:
        print 'Handling page:' + url
        content = getHtml(url)
        for each in content:
            data = getInfo(each)
            printResult(result,data)
    print max(result)
