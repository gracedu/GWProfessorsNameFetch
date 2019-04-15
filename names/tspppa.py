#!/usr/bin/env python
#coding:utf-8

from urllib.request import Request, urlopen 
from bs4 import BeautifulSoup 
import pymysql
import re

conn = pymysql.connect(host='localhost', user='root', passwd=None, db='mysql');
cur = conn.cursor();
cur.execute('USE profv');
hdr = {'User-Agent': 'Mozilla/5.0'};

names = [];


site = "https://tspppa.gwu.edu/faculty-directory";
req = Request(site, headers=hdr);
html = urlopen(req);
bs = BeautifulSoup(html.read(), 'html.parser');

letter = "ABCDIKLMNPRSTVWY"

for i in letter:
	temps = bs.find(id=i).find('ul').findAll('li');
	for temp in temps:
		names.append(temp.a.get_text());



site2 = "https://tspppa.gwu.edu/affiliated-faculty-directory";
req2 = Request(site2, headers=hdr);
html2 = urlopen(req2);
bs2 = BeautifulSoup(html2.read(), 'html.parser');
letter2 = "ABDFKLMNPRSWY"
for i in letter2:
	temps = bs2.find(id=i).find('ul').findAll('li');
	for temp in temps:
		names.append(temp.a.get_text());




name = [x.replace("\r\n", "") for x in names];  # store all names, last,first

def store(lastName, firstName):
	cur.execute('INSERT INTO professors (lastName, firstName, school) VALUES' '("%s", "%s", "%s")', (lastName, firstName, "Trachtenber School of Public Policy & Public Administration"));
	cur.connection.commit();

for na in name:
	store(na.split(',')[0], na.split(',')[1]);




cur.close();
conn.close();