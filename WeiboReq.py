#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import requests
import random
import time
from lxml import etree
import re
class reqW():
    def __init__(self):
        self.headers = [{'Connection' : 'keep-alive','User-Agent':'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 61.0.3163.79Safari/537.36'},
                        {'Connection' : 'keep-alive','User-Agent':'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 61.0.3163.79Safari/537.36'},
                        {'Connection' : 'keep-alive','User-Agent':'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 61.0.3163.79Safari/537.36'},
                        {'Connection' : 'keep-alive','User-Agent':'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 61.0.3163.79Safari/537.36'},
                        {'Connection' : 'keep-alive','User-Agent':'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 61.0.3163.79Safari/537.36'}
                       ]
        self.cookies=[  {"_T_WM":"102feabf068dfc36073296e58f1946c8","SCF": 'AuvJ4hbvhwqqxCYwomHh0Kn52lrYapRh6ZYNZQD2MOBgRaE3DaouZfQdb_htBgkzL33LW9Rlg9fM3hXgtTepdfc.','SUB': '_2A253lssmDeRhGeBN41IV9CjEzjiIHXVVeNVurDV6PUJbkdBeLRfbkW1NRA8WfwCQi7CvJo5v7AjciADbAeiGB09w','SUHB': '0h1Jz1Yg-yY1BR','SSOLoginState': '1519565686'},                    #17191870692----xu481597
                        {'_T_WM': 'b3d6b0d05a6d336191c8f4d40e8b0704','SCF': 'Ao09WjoQq4AVW_ZxSG7XBaeKZwPEvSSRsa84IdKdTLVQhidVyiUtz-QyXAtEeyKmCpXjcV53PW4QAT70oi6ClNs.','SSOLoginState': '1519566336','SUB': '_2A253ls2vDeRhGeBN41EX-SnEwz6IHXVVeNPnrDV6PUJbkdBeLUjxkW1NRA90_JvDzKcSls-pHoylJk5HSWVj2WpT','SUHB': '0Ryq8EZ9wYQ-mi'},           #17131205240----xu486427
                        {"_T_WM":"00790437a6eb0d223f9d570ca661e5a2",'SCF': 'AjipfxI-t_rL1lHmh1XZwl8Bltnvf1jd7_x02sMeCaRc7s4lJEd5AmeuUG_ek5bJ1rR2HUKWRzHVRxqsjfUQkko.','SUB':'_2A253gSMDDeRhGeBP6VsY9ifJyDiIHXVUik1LrDV6PUJbktBeLWmmkW1NRXn_9lgndBEy2nsWQ8k3LkN1GF0xr5ZT','SUHB': '0wn1TpP5k0v1b_','SSOLoginState':'1518687059'},
                        {'_T_WM':'56383890c2e79bfa4d924a34acb94273','SCF': 'Asn4XdIFrvB_WjwZA_9aHjnreMXBY1g04ZefNZ0_M8BQWXin5zXqlFe7zCpwO0Z2VfCVgCfNHYdx39Zc_DtF9QY.','SSOLoginState': '1519566644','SUB': '_2A253ls9kDeRhGeBN41EX8CnMyTmIHXVVeNEsrDV6PUJbkdBeLUb4kW1NRAhkpj1Wp0Kfvl_3YbKNjXh4sEuJBI1Q','SUHB': '0M2FfgK1-A0QlP'},                      {"T_WM":"713a36875bfd30d68000b550a17494c3","SCF":"AjM23mn1ND1iZCYAU0HYPVnjqb8xSftxL1zZXnsJ2Bf3xCUZcE6b-n80dQBYYvemDhi5r5enh00uVskNIQ-2Fwc.","SUB":"_2A253H9rgDeRhGeBN41EX-SnEwz6IHXVU4-aorDV6PUJbkdBeLXb3kW1NRA90_IufU7ImEe0Wbaa6WPJ3GKl1bvgy","SUHB":"0XDlA4xj9iDeWT","SSOLoginState":"1511762608"},
                        {"_T_WM":"9e3e3c6c8bd1cc3fbf34cbbda3942f9c","SCF":"Amkl50mwJxAPxhncIcr31LkpaERI3L0qtig60a7on41Ephz5E4ciQ5lN3bYeD48sBQ7Joh_PtLrsB1Ma_CPWrjI.","SUB":"_2A253H9vlDeRhGeBN41EX8CnMyTmIHXVU4-WtrDV6PUJbkdBeLXDxkW1NRAhkpjJi_3C8TU1tA5utUEyWY6TmHZHI","SUHB":"0oUokfmR8fVd-V", "SSOLoginState":"1511762869"}
                     ]
        self.hid=0

    def req(self,url,header,cookie,ifreload):
        try:
            response = requests.get(url, headers=self.headers[self.hid], cookies=self.cookies[self.hid])
            if ifreload:
                newUrl = re.findall('location.replace\(\"(.*?)\"\)', response.content, re.S)[0]
                if newUrl:
                    print "newUrl:%s"%newUrl
                    return req(newUrl,header,cookie,ifreload)
            htree = etree.HTML(response.content)
            time.sleep(random.random()/2.0)
        except:
            self.hid=(self.hid+1)%4
            try:
                response = requests.get(url, headers=self.headers[self.hid], cookies=self.cookies[self.hid])
                htree=etree.HTML(response.content)
            except:
                time.sleep(5)
                self.hid=(self.hid+1)%4
                response = requests.get(url, headers=self.headers[self.hid], cookies=self.cookies[self.hid])
                htree=etree.HTML(response.content)
        return htree,response

    def perfectReq(self,url,varifyXpath='',varifyRe='',ifreload=False):
        print "hid is:%s"%self.hid    #hid:账号序号
        for i in range(20):
            try:
                response=self.req(url,self.headers[self.hid],self.cookies[self.hid],ifreload)
                if varifyXpath:
                    v=response[0].xpath(varifyXpath)[0]
                    return response,v
                if varifyRe:
                    v=re.findall(varifyRe,response[1].content)[0]
                return response
            except etree.XMLSyntaxError as e:
                self.hid=(self.hid+1)%4
                print e
                time.sleep(20*(i+1))
            except IndexError as e:
                print e
                self.hid=(self.hid+1)%4
                time.sleep(10*(i))

