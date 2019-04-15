#!/usr/bin/env python
#coding:utf-8

from urllib.request import Request, urlopen 
from bs4 import BeautifulSoup 
import pymysql
import re

conn = pymysql.connect(host='localhost', user='root', passwd=None, db='mysql');
cur = conn.cursor();
cur.execute('USE profv');


site = "https://gsehd.gwu.edu/directory";
hdr = {'User-Agent': 'Mozilla/5.0'};
req = Request(site, headers=hdr);
html = urlopen(req);
bs = BeautifulSoup(html.read(), 'html.parser');
names = [];



result = bs.find(class_='view-content');

temp1 = result.find(class_='views-row-odd views-row-first w3-row w3-padding').find(class_='w3-col l2').div.a.get_text();
names.append(temp1);

temp2 = result.findAll(class_='views-row-odd w3-row w3-padding');
for temp in temp2:
	names.append(temp.find('a').get_text());

temp3 = result.findAll(class_='views-row-even w3-row w3-padding');
for temp in temp3:
	names.append(temp.find('a').get_text());

temp4 = result.find(class_='views-row-odd views-row-last w3-row w3-padding').find(class_='w3-col l2').div.a.get_text();
names.append(temp4);

def store(lastName, firstName):
	cur.execute('INSERT INTO professors (lastName, firstName, school) VALUES' '("%s", "%s", "%s")', (lastName, firstName, "Graduate School of Education and Human Development"));
	cur.connection.commit();

for na in names:
	store(na.split(',',1)[0], na.split(',',1)[1]);

cur.close();
conn.close();

