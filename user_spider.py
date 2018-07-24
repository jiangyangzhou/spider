# -*- encoding:utf-8 -*-
import requests
from lxml import etree
import json
import mysql.connector
import gc
import time
import random
from WeiboReq import reqW
from saveInfo import dataTool
import pandas as pd
import csv
import re
import jieba

#It is a spider of weibo.cn 
#It provide several func to crawl some info of weibo user.

wreq=reqW()
#if you want to save data into database, specify your database here
dataW=dataTool(host='rm-uf6bnk6xg09atw4m6o.mysql.rds.aliyuncs.com',port='3306',user="username",password="password",database="weibo")
#dataW=dataTool(host='DESKTOP-755U1LH',port='3306',user="admin",password="",database="weiboD")
def gainUserInfo(uid):       #获取用户信息上传到表userinfo
    infoUrl="https://weibo.cn/%s/info"%uid
    mainUrl="https://weibo.cn/u/%s"%uid
    udict={"uid":uid,"name":"","basicInfo":"","qualify":"","area":"","sex":"","label":"","birthday":"","follows":'',"fans":'','weibonum':'',"ifcrawl":"0"}
    d={u'昵称':'name',u'认证':'qualify',u'性别':'sex',u'生日':'birthday',u"标签":"label",u'认证信息':'qualify',u'地区':'area',u"简介":"basicInfo"}
    selector,html=wreq.perfectReq(infoUrl)
    basicInfo=selector.xpath("//body/div[6]/text()")
    if not basicInfo:
        print "basicInfo:",req
    for info in basicInfo:
        print info
        i=info.split(":")
        if i[0]==u'标签':
            break
        if u'认证信息' in i[0] or i[0]==u'达人':
            continue
        try:
            udict[d[i[0]]]=",".join(i[1:])
        except KeyError as e:
            print e
    label=selector.xpath("//div[6]/a/text()")
    print label
    udict["label"]=",".join(label[:-1])
    selector=wreq.perfectReq(mainUrl)[0]
    mxpath="//div[@class='u']/div[1]"
    try:
        udict['weibonum']=selector.xpath(mxpath+'/span[1]/text()')[0].split('[')[1].split(']')[0]
        udict['follows']=selector.xpath(mxpath+'/a[1]/text()')[0].split('[')[1].split(']')[0]
        udict['fans']=selector.xpath(mxpath+'/a[2]/text()')[0].split('[')[1].split(']')[0]
    except IndexError as e:
        print "微博主页",e
        print wreq.perfectReq(infoUrl)[1].content
    #dataW.savetoSql([udict],table="userinfo",method="replace")
    dataW.saveDictCsv([udict],"data/ndata/governuinfo.csv")
    dataW.commit()
    print "gainUserInfo of %s"%uid
    print udict
    return udict

def gainRepost(weiboId):
    rootUrl="https://weibo.cn/repost/"+weiboId
    page=0
    xpath="//div[@class='pms']/following-sibling::div[@class='c']"
    fullPage = "//div[@class='pa']/form/div/input[1]"
    selector,html = wreq.perfectReq(rootUrl)
    print html.content
    fullPage = selector.xpath(fullPage)[0].attrib['value']
    fullPage = int(fullPage)
    while True:
        if fullPage>page:
            break
        Dicts=[]
        page+=1
        print "gain repost of %s,page%s"%(weiboId,page)
        url=rootUrl+"?page=%d"%page
        if page!=1:
            (selector,html),selector = wreq.perfectReq(url,varifyXpath=xpath)
        selector=selector.xpath(xpath)
        try:
        	a=selector[0].xpath('a[1]')[0]
        except IndexError as e:
        	print html.content
        	print e,"page%s,exist"%page
        	break        	
        for n in range(10):
            repostDict = {"reUid": "", "nickName": "", "content": "", "time": "", "cfrom": ""}
            try:
                reUid=selector[n].xpath('a[1]')[0].attrib['href']
                print reUid
            except IndexError:
                print 
                if n!=0:
                    continue
                else:
                    break
            repostDict['reUid']=reUid.strip('/')
            '''if '/u/' in reUid:
                repostDict['reUid']=reUid.strip('/u/')
            else:
                print "oh,no!!!!!!!!!!!!!!!!!"
                userUrl="https://weibo.cn"+reUid
                userSel,h=wreq.perfectReq(userUrl)
                repostDict['reUid']=userSel.xpath('//div[@class="u"]/div[1]/a[1]')[0].attrib['href'].split('/')[1]'''
            repostDict['nickName']=selector[n].xpath('a[1]/text()')[0]
            repostDict['content']="".join(selector[n].xpath('text()| a[contains(@href,"/n/")]/text()| a[contains(text(),"#")]/text()'))
            try:
                tstr=selector[n].xpath('span[@class="ct"]/text()')[0]
            except IndexError as e:
                if n!=0:
                    continue
                else:
                    break
            repostDict['time']=gettime(tstr)
            try:
                repostDict['cfrom']=tstr.split(u'来自')[1]
            except IndexError:
                repostDict['cfrom']=""
            print Dicts
            Dicts.append(repostDict)
        dataW.saveDictCsv(Dicts, filepath="./repost/%s.csv" % weiboId)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
def gainUidlist(url,maxpage=50):
    uidlist=[]
    udicts=[]
    for page in range(maxpage):
        print "gainUidlist page=%s:"%(page+1)
        userUrl = url + "&page=%d" % (page+1)
        selector,html = wreq.perfectReq(userUrl)
        print html.content
        mxpath = '//div[@class="c"]/form[@method="post"]/div/input[@name="uidList"]'
        try:
            uid = selector.xpath(mxpath)[0].attrib['value']
        except IndexError as e:
            print e, "all of the uid have been downloaded"
            return udicts
        uids=uid.split(",")
        uidlist+=uids
        print uids
        for i in range(len(uids)):
            uxpath = '//table[%s]//td[2]'%(i+1)
            udict={"uid":uids[i],"name":"","fans":'',"area":""}
            udict["name"] = selector.xpath(uxpath+"/a[1]/text()")[0]
            print udict['name']
            infoStr=selector.xpath(uxpath+"/text()")[0]
            print [infoStr]
            try:
                udict['fans']=re.findall(u'^粉丝(.*?)人',infoStr)[0]
            except IndexError:
                pass
            try:
                udict["area"]=" ".join(infoStr.split(u'\xa0')[1:]).strip()
            except IndexError:
                pass
            udicts.append(udict)
    return udicts

def gainAttigroup(uid,maxpage=300):    #获取用户关注的人，存入uncrawlinfo    
    rootUrl = "https://weibo.cn/attgroup/change?rl= 0&cat=user&uid=%s"%uid
    print "get %s attigroup:"%uid
    attigroup= gainUidlist(rootUrl,maxpage)
    dataW.saveDictCsv(attigroup,filepath="./data/userinfo%suserinfo.csv"%uid)
    dataW.saveintoSql(attigroup,table="userinfo",method="replace")
    dataW.commit()
    return Attigroup

def searchUser(keyword,maxpage=50,namePattern=''):
    keywordq=urllib.quote(keyword)
    url="https://weibo.cn/search/user/?keyword=%s&sort=108"%keywordq
    ulist=gainUidlist(url,maxpage)
    if namePattern:
        newulist=[]
        for user in ulist:
            if re.match(namePattern,user['name']):
                newulist.append(user)
        ulist=newulist
    dataW.saveDictCsv(ulist,filepath="./searchUser/%s.csv"%keyword)
    dataW.savetoSql(ulist,table="uncrawlinfo",method="replace")
    dataW.commit()
    return ulist

def gainnewId(initId):   #获取一波关注的人，作为爬虫起点
    gainAttigroup(initId)
    dataW.cursor.execute("select uncrawlinfo.uid from uncrawlinfo inner join userinfo on uncrawlinfo.uid <> userinfo.uid")
    uidlist=saveW.cursor.fetchall()
    print uidlist
    for u in uidlist:
        try:
            if int(gainUserInfo(u[0])['follows'])<500:
                gainAttigroup(u[0])
        except:
            pass
    dataW.commit()

def GetUserInfo():
    dataW.cursor.execute("select distinct uncrawlinfo.uid from uncrawlinfo inner join userinfo on uncrawlinfo.uid <> userinfo.uid;")
    uidlist = dataW.cursor.fetchall()
    for u in uidlist:
        gainUserInfo(u[0])
        dataW.cursor.execute("delete from uncrawlinfo where uid=%s" %u)
    dataW.commit()


def gettime(tstr):
    current=time.localtime(time.time())
    wtime= tstr.split(u'\xa0来自')[0].strip()
    print [wtime]
    if u"分钟前"in tstr:
        minute=int(tstr.split(u'分钟前')[0])
        t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-minute*60))
    elif re.match("^%s"%u'今天',wtime):
        date = time.strftime('%Y-%m-%d', current)
        ctime=wtime.split(u'今天')[1].strip()
        t=date+' '+ctime
    elif tstr[:2]==u'20':
        t=wtime
    else:
        datelist=wtime.split()[0]
        try:
            mouth=datelist.split(u'月')[0]
        except:
            print "tstr",tstr
        day=datelist.split(u'月')[1].split(u'日')[0]
        t="%s"%current[0]+'-'+mouth+'-'+day+' '+wtime.split()[1]
    return t


def gainweibo(id,maxPage,table=0):
    rootUrl="http://weibo.cn/u/%s"%id
    page=0
    wtime=["",""]
    flagFirst=True
    allweibo=[]
    while(page<maxPage):
        page+=1
        print "id:%s,page:%s"%(id,page)
        userUrl=rootUrl+"?page=%d"%page
        selector =wreq.perfectReq(userUrl,varifyXpath=mxpath)[0]
        dicts=[]
        for n in range(10):
            mxpath="//div[contains(@id,'M_')]"
            try:
                selector=selector.xpath(mxpath)[n]
            except IndexError as e:
                print e,"NO.%d"%n
                if n!=0:
                    break
                else:
                    return wtime
            dict= {'uid':id,'ifreweet':0,'reweetFrom':"",'reweetContent':"",'reatsb':"",'topic':"",'content':"",'atsb':"",'attiNum':"",'repostNum':"",'commentNum':"",'time':"",'cfrom':"",'weiboid':''}
            dict['weiboid']=selector.attrib["id"][2:]
            if re.match("^%s"%u'转发了',selector.xpath('div[1]/span[1]/text()')[0]):
                dict['ifreweet'] = 1
                try:
                    dict['reweetFrom'] = selector.xpath('div[1]/span[1]/a[1]')[0].text
                except IndexError as e:
                    print IndexError, e,":ReweetFrom delete!"
                try:
                    dict['reweetContent'] = "".join(selector.xpath('div[1]/span[2]')[0].xpath('string(.)'))
                    dict['reatsb'] = "".join(selector.xpath('div[1]/span[2]/a[contains(@href,"/n/")]/text()'))
                    dict['topic'] = "".join(selector.xpath('div[1]/span[2]/a[contains(text(),"#")]/text()'))
                except:
                    dict['reweetContent'] = ""
                con = 'div/span[contains(text(),"%s")]/parent::*' % u'转发理由'
                dict['content'] = "".join(selector.xpath(con + '/text() | ' + con + '/a[contains(@href,"/n/")]/text()|' + con + '/a[contains(text(),"#")]/text()'))
                dict['atsb'] = "".join(selector.xpath(con + '/a[contains(@href,"/n/")]/text()'))
                dict['topic'] += "".join(selector.xpath(con + '/a[contains(text(),"#")]/text()'))
                try:
                    dict['attiNum'] = selector.xpath(con+'/a[contains(text(),"%s")]/text()' % u'赞')[0].split("[")[1].split(']')[0]
                    dict['repostNum']= selector.xpath(con+'/a[contains(text(),"%s")]/text()'%u'转发[')[0].split("[")[1].split(']')[0]
                    dict['commentNum']= selector.xpath(con+'/a[contains(text(),"%s")]/text()'%u'评论[')[0].split("[")[1].split(']')[0]
                except IndexError as e:
                    try:
                        dict['attiNum'] = selector.xpath(con+'/span[contains(text(),"%s")]/text()' % u'赞')[0].split("[")[1].split(']')[0]
                    except IndexError as e:
                        dict["attiNum"]= ""
                tstr=selector.xpath('div/span[@class="ct"]')[0].text
                dict['time'] =gettime(tstr)
                try:
                    dict['cfrom']=tstr.split(u'来自')[1]
                except IndexError:
                    dict['cfrom']=""
            else:
                con = 'div[1]/span[@class="ctt"]'
                dict['content'] = "".join(selector.xpath(con + '/text()|' + con + '/a[contains(@href,"/n/")]/text()|' + con + '/a[contains(text(),"#")]/text()'))
                dict['atsb'] = "".join(selector.xpath(con + '/a[contains(@href,"/n/")]/text()'))
                dict['topic'] = "".join(selector.xpath(con + '/a[contains(text(),"#")]/text()'))
                try:
                    dict['attiNum'] = selector.xpath('div/span[contains(text(),"%s")]/text()' % u'赞')[0].split("[")[1].split(']')[0]
                except IndexError:
                    dict['attiNum'] = selector.xpath('div/a[contains(text(),"%s")]/text()' % u'赞')[0].split("[")[1].split(']')[0]
                dict['repostNum'] = selector.xpath('div/a[contains(text(),"%s")]/text()' % u'转发')[0].split('[')[1].split(']')[0]
                dict['commentNum'] = selector.xpath('div/a[contains(text(),"%s")]/text()' % u'评论')[0].split("[")[1].split(']')[0]
                tstr = selector.xpath('div/span[@class="ct"]')[0].text
                dict['time'] = gettime(tstr)
                try:
                    dict['cfrom'] = tstr.split(u'来自')[1]
                except IndexError:
                    dict['cfrom']=""
            if page==1 and flagFirst and u"置顶" not in selector.xpath('div[1]/span[1]/text()'):
                wtime[0]=dict['time']
                flagFirst=False
            wtime[1]=dict['time']
            dicts.append(dict)
        dataW.saveDictCsv(dicts,"weiboOfshanghai.csv",wtype='a')
        if table!=0:
            dataW.savetoSql(datadicts=dicts,table=table,method='replace')
            dataW.commit()
        if page%100==0:
            time.sleep(2)
        allweibo.append(dicts)
    return allweibo

def gainWeiboAll(begin=0,end=10):
    dataW.execute("select uid,weibonum from userInfo where qualify regexp'.*教育官微.*' order by uid;" )
    userlist=dataW.cursor.fetchall()
    userlist=userlist[begin:end]
    print userlist
    i=0
    u=0
    for user in userlist:
        u=u+1
        try:
            dataW.execute("create table college (uid bigint,weiboid varChar(20),ifreweet int,reweetFrom varchar(50), reweetContent varchar(1000), reatsb varchar(300),topic varchar(100),content varchar(1000), atsb varchar(200),attiNum int, repostNum int ,commentNum int, time datetime, cfrom varchar(50),primary key(uid,weiboid));")
        except:
            pass
        gainweibo(user[0],maxPage=100000,table="college")
        print user[0]
        dataW.execute("UPDATE userInfo set ifcrawl=1 where uid=%s"%user[0])
        dataW.commit()
        time.sleep(5)
        if u%20==0:
            i=i+1

def main(initId):
    #gainnewId(initId)
    #gainweibo(initId)
    GetUserInfo()
    gainWeiboAll(0,100)
    #print searchUser('大学',namePattern=u".*(大学)$")
    dataW.commit()


'''
with open('data/users_all.txt','rb') as f:
    user = f.readlines()
    data="["+",".join(user)+"]"
userinfo=pd.read_json(data)
for index, row in userinfo.iterrows():
    weibo = gainweibo(row['user_id'],maxPage=1)
'''
'''
#main("5476301864")
gainRepost('G5cte48T9')
wdf = pd.read_csv("./datak/wangfeng_2018_2_22.csv")
#gainweibo()
weiboId = wdf.weiboid
for wid in weiboId:
    print type(wid)
#   print wid
    gainRepost(wid)
'''
#gainAttigroup('1739746697')


userDf = pd.read_csv("government.csv")
user_id = userDf['uid'].tolist()
user_id = map(lambda x:'%s'%x,user_id)
print user_id
for uid in user_id:
    gainUserInfo(uid)




