#!/usr/bin/env python
#coding:utf-8

from urllib.request import Request, urlopen 
from bs4 import BeautifulSoup 
import pymysql
import re

conn = pymysql.connect(host='localhost', user='root', passwd=None, db='mysql');
cur = conn.cursor();
cur.execute('USE profv');

# corcoran full time faculty
site = "https://corcoran.gwu.edu/full-time-faculty";
hdr = {'User-Agent': 'Mozilla/5.0'};
req = Request(site, headers=hdr);
html = urlopen(req);
bs = BeautifulSoup(html.read(), 'html.parser');

results1 = bs.body.find(id='page').find(id='main').find(id='content').find(id='block-system-main').find(id='HELLO').find('div', {'class' : 'view-content'}).findAll('div', class_=re.compile('^views-row'));
names = [];  # names store all falculty names
for result in results1:
	temp = result.find(class_='headline-spotlight with-image').find(class_='copy-wrapper').h3.find('a').get_text();
	names.append(temp);

# corcoran part time faculty
site2 = "https://corcoran.gwu.edu/part-time-faculty";
req2 = Request(site2, headers=hdr);
html2 = urlopen(req2);
bs2 = BeautifulSoup(html2.read(), 'html.parser');

results2 = bs2.body.find(id='page').find(id='main').find(id='content').find(id='block-system-main').find(id='HELLO').find('div', {'class' : 'view-content'}).findAll('div', class_=re.compile('^views-row'));
for result in results2:
	temp = result.find(class_='headline-spotlight with-image').find(class_='copy-wrapper').h3.find('a').get_text();
	names.append(temp);

# corcoran Continuing Education Faculty
site3 = "https://corcoran.gwu.edu/continuing-education-faculty";
req3 = Request(site3, headers=hdr);
html3 = urlopen(req3);
bs3 = BeautifulSoup(html3.read(), 'html.parser');

results3 = bs3.body.find(id='page').find(id='main').find(id='content').find(id='block-system-main').find(id='HELLO').find('div', {'class' : 'view-content'}).findAll('div', class_=re.compile('^views-row'));
for result in results3:
	temp = result.find(class_='headline-spotlight with-image').find(class_='copy-wrapper').h3.find('a').get_text();
	names.append(temp);

# corcoran Distance Education Faculty
site4 = "https://corcoran.gwu.edu/distance-education-faculty";
req4 = Request(site4, headers=hdr);
html4 = urlopen(req4);
bs4 = BeautifulSoup(html4.read(), 'html.parser');

results4 = bs4.body.find(id='page').find(id='main').find(id='content').find(id='block-system-main').find(id='HELLO').find('div', {'class' : 'view-content'}).findAll('div', class_=re.compile('^views-row'));
for result in results4:
	temp = result.find(class_='headline-spotlight with-image').find(class_='copy-wrapper').h3.find('a').get_text();
	names.append(temp);



def store(lastName, firstName):
	cur.execute('INSERT INTO professors (lastName, firstName, school) VALUES' '("%s", "%s", "%s")', (lastName, firstName, "Corcoran School of the Arts & Design"));
	cur.connection.commit();


for name in names:
	store(name.split(' ')[-1], name.split(' ',1)[0]);

cur.close();
conn.close();