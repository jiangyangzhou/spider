#!/root/python
# -*- encoding:utf-8 -*-
import re
import requests
import random
import time
from lxml import etree
import json
import csv
rooturl="http://weibo.com/login.php"
cookie={'_T_WM':'b5616f8e25e1402fe0916a237ee583c8','SCF':'Aj0ZZShNHW8HB5a9fUynDouuSm37NzRmhCpLMH6G7Sov3VvkBo6kPnyrS7sXNpAdOvdiLwFtcR1GSDMEfqIeOO8.','SUB':'_2A250uP7hDeRhGeBP6VsY9ifJyDiIHXVUQoKprDV6PUJbkdBeLVDGkW1NvQTdSGNRUOtcdoLDnosR50lW9g..','SUHB':'0sqBpT1MGOpWjo','M_WEIBOCN_PARAMS':'featurecode%3D20000320%26lfid%3D102803_ctg1_8999_-_ctg1_8999_home%26luicode%3D20000174%26uicode%3D20000174',' H5_INDEX':'3','H5_INDEX_TITLE':'puti%E5%B0%8F%E5%8F%AF%E7%88%B1','SSOLoginState':'1505529521'}
header = { 'Connection' : 'keep-alive',  'User-Agent' :  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0' }


def req(url,header):
    try:
        response=requests.get(url,headers=header,cookies=cookie)
    except:
        time.sleep(100)
        try:
            response = requests.get(url, headers=header, cookies=cookie)
        except:
            time.sleep(300)
            response = requests.get(url, headers=header, cookies=cookie)
    t = random.random()
    time.sleep(t)
    return etree.HTML(response.content)

def gainweibo(id,header):
    rootUrl="http://weibo.cn/u/"+id
    page=0
    while(True):
        page+=1
        print "page:",page
        userUrl=rootUrl+"?page=%d"%page
        try:
            selector=req(userUrl,header)
        except IndexError as e:
            print e,"all of the weibos have been downloaded"
            break
        print type(selector)
        for n in range(10):
            dict={'ifreweet':0,'reweetFrom':"",'reweetContent':"",'reweetContent':"",'re@sb':"",'topic':"",'content':"",'_@sb':"","attiNum":"","repostNum":"","commentNum";"",'time':""}
            mxpath="//div[contains(@id,'M_')]"
            try:
                selector=selector.xpath(mxpath)[n]
            except IndexError as e:
                print e,"NO.%d"%n
                if n!=0:
                    break
                else:
                    return
            if u'转发了' in selector.xpath('div[1]/span[1]/text()')[0]:
                dict['ifreweet'] = 1
                try:
                    dict['reweetFrom'] = selector.xpath('div[1]/span[1]/a[1]')[0].text
                except IndexError as e:
                    print IndexError, e
                try:
                    dict['reweetContent'] = "".join(selector.xpath('div[1]/span[2]')[0].xpath('string(.)'))
                    dict['re@sb'] = "".join(selector.xpath('div[1]/span[2]/a[contains(@href,"/n/")]/text()'))
                    dict['topic'] = "".join(selector.xpath('div[1]/span[2]/a[contains(text(),"#")]/text()'))
                except:
                    dict['reweetContent'] = ""
                con = 'div/span[contains(text(),"%s")]/parent::*' % u'转发理由'
                dict['content'] = "".join(selector.xpath(con + '/text() | ' + con + '/a[contains(@href,"/n/")]/text()|' + con + '/a[contains(text(),"#")]/text()'))
                dict['_@sb'] = "".join(selector.xpath(con + '/a[contains(@href,"/n/")]/text()'))
                dict['topic'] += "".join(selector.xpath(con + '/a[contains(text(),"#")]/text()'))
                dict['attiNum']= selector.xpath('div/'s)
                dict['repostNum']= selector.xpath(div)
                dict['commentNum']= selector.xpath(con + '/a[contains(text(),"#")]/text()'))
                dict['time'] = selector.xpath('div/span[@class="ct"]')[0].text
            else:
                con = 'div[1]/span[@class="ctt"]'
                dict['content'] = "".join(selector.xpath(con + '/text()|' + con + '/a[contains(@href,"/n/")]/text()|' + con + '/a[contains(text(),"#")]/text()'))
                dict['_@sb'] = "".join(selector.xpath(con + '/a[contains(@href,"/n/")]/text()'))
                dict['topic'] = "".join(selector.xpath(con + '/a[contains(text(),"#")]/text()'))
                dict['time'] = selector.xpath('div/span[@class="ct"]')[0].text
            print dict
            with open(id + "weibo.json", "a") as f:
                json.dump(dict, f)
                f.write("\n")
                

def gainAttigroup(uid):
    rootUrl = "https://weibo.cn/attgroup/change?rl= 0&cat=user&uid=%s&page=1"%uid
    # rootUrl = "http://weibo.cn/attgroup/change?cat=user&uid=%s"%uid
    page = 0
    attigroup=[]
    while (True):
        page += 1
        print "page:", page
        userUrl = rootUrl + "&page=%d" % page
        selector = req(userUrl, header)
        mxpath = '//div[@class="c"]/form[@method="post"]/div/input[@name="uidList"]'
        try:
            att = selector.xpath(mxpath)[0].attrib['value']
        except IndexError as e:
            print e, "all of the attgroup have been downloaded"
            break
        atti=att.split(",")
        attigroup+=atti
    with open("att%s"%uid+".csv","wb") as csvf:
        csvW=csv.writer(csvf)
        csvW.writerow(attigroup)
    return attigroup

def main(initId):
    idlist=gainAttigroup(initId)
    print idlist
    for id in idlist:
        gainweibo(id,header)

main("2247657845")

