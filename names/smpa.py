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

names = [];  # first last


site = "https://smpa.gwu.edu/full-time-faculty";
req = Request(site, headers=hdr);
html = urlopen(req);
bs = BeautifulSoup(html.read(), 'html.parser');

results = bs.findAll('h3', {'class':'promo-title'})
results = results[:-2]
for result in results:
	names.append(result.a.get_text())

site2 = "https://smpa.gwu.edu/part-time-faculty";
req2 = Request(site2, headers=hdr);
html2 = urlopen(req2);
bs2 = BeautifulSoup(html2.read(), 'html.parser');

#names2 = []
#results2 = bs2.findAll('p');
#for resulttt in results2:
#	result2 = results2.find('strong');
#	for x in result2:
#		names2.append(x.get_text())

#name2 = [x.replace("\xa0", "") for x in names2]
name2 = []
name2.append('Lori Brainard')
name2.append('Jennifer Brinkerhoff')
name2.append('Danny Hayes')
name2.append('Marc Lynch')
name2.append('Melani McAlister')

def store(lastName, firstName):
	cur.execute('INSERT INTO professors (lastName, firstName, school) VALUES' '("%s", "%s", "%s")', (lastName, firstName, "School of Media & Public Affairs"));
	cur.connection.commit();



for na in names:
	store(na.split(' ')[-1], na.split(' ')[0])

for na in name2:
	store(na.split(' ')[-1], na.split(' ')[0])

cur.close();
conn.close();


