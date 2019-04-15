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

names = [];  # last, first
names2 = []; # first last

site = "https://www.law.gwu.edu/full-time-faculty";
req = Request(site, headers=hdr);
html = urlopen(req);
bs = BeautifulSoup(html.read(), 'html.parser');

lastName = bs.findAll('span', {'property':'familyName'});
firstName = bs.findAll('span', {'property':'givenName'});
temp1 = [];
temp2 = [];

for l in lastName:
	temp1.append(l.get_text());

for f in firstName:
	temp2.append(f.get_text());

for x in range(len(firstName)):
	names.append(temp1[x]+temp2[x]);

names.append('Celorio,Rosa')
names.append('DeVigne,Renee')
names.append('Ewert,Elizabeth')
names.append('Fine,Susan')
names.append('Johnson,David')
names.append('Juni,Robin')
names.append('Molinengo,Hank')
names.append('Morrison,Alan')
names.append('Paddock,LeRoy')
names.append('Robinson,Alfreda')
names.append('Schenck,Lisa')
names.append('Sim,Sophia')
names.append('Tillipman, Jessica')
names.append('Whealan,John')

site2 = "https://www.law.gwu.edu/adjunct-faculty";
req2 = Request(site2, headers=hdr);
html2 = urlopen(req2);
bs2 = BeautifulSoup(html2.read(), 'html.parser');

results = bs2.findAll('li');
for result in results:
	names2.append(result.a.get_text())

name2 = names2[81:393]

def store(lastName, firstName):
	cur.execute('INSERT INTO professors (lastName, firstName, school) VALUES' '("%s", "%s", "%s")', (lastName, firstName, "Law"));
	cur.connection.commit();

for na in names:
	store(na.split(',')[0], na.split(',')[1])

for na in name2:
	store(na.split(' ')[-1], na.split(' ')[0])


cur.close();
conn.close();



