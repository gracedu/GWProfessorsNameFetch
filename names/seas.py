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
names2 = [];


site = "https://www.seas.gwu.edu/faculty-directory";
req = Request(site, headers=hdr);
html = urlopen(req);
bs = BeautifulSoup(html.read(), 'html.parser');

letter = "ABCDEFGHIKLMNOPRSVWYZ";

for i in letter:
	temps = bs.find(id=i).find('ul').findAll('li');
	for temp in temps:
		names.append(temp.a.get_text());

name = [x.replace("\r\n", "") for x in names];  # store all names   last,fist


site2 = "https://www.cs.seas.gwu.edu/faculty";
req2 = Request(site2, headers=hdr);
html2 = urlopen(req2);
bs2 = BeautifulSoup(html2.read(), 'html.parser');

results = bs2.findAll('p', {'style' : 'margin-top: 0px;'});
for result in results:
	temps = result.findAll('strong');
	for temp in temps:
		names2.append(temp.get_text());

names2 = names2[10:];	
names22 = [x.replace("\xa0", " ") for x in names2]; # first,last
names22.append('Benjamin Harvey');
names22.append('Christopher Toombs');
names22.append('Caroll (Kent) Vidrine');

names22.append('Arush Gadkar');
names22.append('Omer Kavaklioglu');
names22.append('Omar Mazzoni');
names22.append('Sina Najmaei');
names22.append('Jerry Wu');
names22.append('Sean Yun');
names22.append('Mohammed Shamma');
names22.append('Saul Torrico');
names22.append('Arzhang Zamani');
names22.append('Yiwen Zhou');
names22.append('Kartik V. Bulusu');
names22.append('Ken P. Chong');
names22.append('Morton H. Friedman');
names22.append('Ashraf Imam');
names22.append('Adam Wickenheiser');

names22.append('Michelle Bailey');
names22.append('D. S. Dodbele');
names22.append('D. Gerk');
names22.append('Olivier Mesnard');
names22.append('M. Naderi');
names22.append('Nikhil Nigam');
names22.append('Bong-Min Paik');
names22.append('R. Cortesi');
names22.append('J. Flemming');
names22.append('M. A. Imam');
names22.append('J. Milgram');
names22.append('E. Naranji');
names22.append('J. K. Soldner');


def store(lastName, firstName):
	cur.execute('INSERT INTO professors (lastName, firstName, school) VALUES' '("%s", "%s", "%s")', (lastName, firstName, "School of Engineering & Applied Science"));
	cur.connection.commit();

for na in name:
	store(na.split(',')[0], na.split(',')[1]);
	
for na in names22:
	store(na.split(' ')[-1], na.split(' ')[0]);


cur.close();
conn.close();
