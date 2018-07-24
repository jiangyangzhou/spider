#!/root/python
# -*- encoding:utf-8 -*-
import csv
import json
import mysql.connector
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class dataTool():
	def __init__(self,host='127.0.0.1',port='3306',user='root',password='',database=''):
		self.conn=mysql.connector.connect(host=host,port=port,user=user,password=password,database=database)
		self.cursor=self.conn.cursor()

	def saveDictCsv(self,datadicts,filepath,wtype='ab'):
		fileExist=os.path.exists(filepath)
		addHeader=False
		if wtype[0]=='w' or not fileExist:
			addHeader=True
		if fileExist and os.path.getsize(filepath)<5:
			addHeader=True
		with open(filepath, wtype) as f:
			csvW=csv.writer(f,lineterminator='\n')
			if addHeader:
				headers=datadicts[0].keys()
				csvW.writerow(headers)
			for row in datadicts:
				csvW.writerow(row.values())

	def saveDictJson(self,datadicts,filepath,wtype='a+'):
		with open(filepath, wtype) as f:
			for dict in datadicts:
				json.dump(dict, f)
				f.write("\n")

	def savetoSql(self,datadicts,table,method="replace"):
		columns=""
		values=""
		for key in datadicts[0].keys():
			columns+="%s,"%key
		columns=columns.strip(',')
		for dict in datadicts:
			values+="("
			for value in dict.values():
				value="%s"%value
				value=re.sub('\"',"'",value)
				values+='"%s",'%value
			values=values.strip(',')
			values+="),"
		values=values.strip(",")
		self.cursor.execute("%s into %s(%s) values %s;"%(method,table,columns,values))

	def execute(self,command):
		self.cursor.execute(command)
		return self.conn

	def commit(self):
		self.conn.commit()
