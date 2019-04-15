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


site = "https://elliott.gwu.edu/full-time-faculty";
req = Request(site, headers=hdr);
html = urlopen(req);
bs = BeautifulSoup(html.read(), 'html.parser');
letter = "ABCDEFGHJKLMNPRSTVWYZ";
for i in letter:
	temps = bs.find(id=i).findAll('li');
	for temp in temps:
		names.append(temp.a.get_text());

site2 = "https://elliott.gwu.edu/part-time-faculty";
req2 = Request(site2, headers=hdr);
html2 = urlopen(req2);
bs2 = BeautifulSoup(html2.read(), 'html.parser');
letter2 = "ABCDEFGHJKLMNPQRSTUVWYZ";
for i in letter2:
	temps2 = bs2.find(id=i).findAll('li');
	for temp in temps2:
		names.append(temp.a.get_text());

name = [x.replace("\r\n", "") for x in names];

name.append('Ehrenfreund,Pascale');
name.append('Gordon,Amy');
name.append('Lagadec,Erwan');
name.append('Luu,Ky');
name.append('Marshall,Erwan');
name.append('Nolan,Janne');
name.append('Ollapally,Deepa');
name.append('Orttung,Robert');
name.append('Peyrouse,Sebastien');
name.append('Rabgey,Tashi');
name.append('Spear,Joanna');
name.append('Squassoni,Sharon');
name.append('Teich,Albert');
name.append('Yarr,Linda');
name.append('Zhemukhov,Sufian');

def store(lastName, firstName):
	cur.execute('INSERT INTO professors (lastName, firstName, school) VALUES' '("%s", "%s", "%s")', (lastName, firstName, "Elliott School of International Affairs"));
	cur.connection.commit();

for na in name:
	store(na.split(',',1)[0], na.split(',',1)[1]);




cur.close();
conn.close();