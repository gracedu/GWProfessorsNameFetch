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


site5 = "https://business.gwu.edu/faculty-directory";
req5 = Request(site5, headers=hdr);
html5 = urlopen(req5);
bs5 = BeautifulSoup(html5.read(), 'html.parser');

letter = "ABCDEFGHJKLMNOPRSTVWXYZ";

for i in letter:
	temps = bs5.find(id=i).find('ul').findAll('li');
	for temp in temps:
		names.append(temp.a.get_text());
	
name = [x.replace("\r\n", "") for x in names];  # store all names

def store(lastName, firstName):
	cur.execute('INSERT INTO professors (lastName, firstName, school) VALUES' '("%s", "%s", "%s")', (lastName, firstName, "Business"));
	cur.connection.commit();

for na in name:
	store(na.split(',',1)[0], na.split(',',1)[1]);




cur.close();
conn.close();