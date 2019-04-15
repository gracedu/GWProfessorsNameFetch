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


site = "https://gspm.gwu.edu/faculty";
req = Request(site, headers=hdr);
html = urlopen(req);
bs = BeautifulSoup(html.read(), 'html.parser');

letter = "ABCDEFGHIKLMNOPRSTVWZ"

for i in letter:
	temps = bs.find(id=i).find('ul').findAll('li');
	for temp in temps:
		names.append(temp.a.get_text());

name = [x.replace("\r\n", "") for x in names];  # store all names, last,first

def store(lastName, firstName):
	cur.execute('INSERT INTO professors (lastName, firstName, school) VALUES' '("%s", "%s", "%s")', (lastName, firstName, "The Graduate School of Political Management"));
	cur.connection.commit();

for na in name:
	store(na.split(',')[0], na.split(',')[1]);




cur.close();
conn.close();
