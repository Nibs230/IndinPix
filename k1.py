import requests
import csv
from bs4 import BeautifulSoup
import re 
import copy
def Find(string): 
    regexp = re.compile(r'http://www.espncricinfo.com')
    if regexp.search(string):
        return True
    else:
        regexp = re.compile(r'http://(.+?)cricinfo.com')
        if regexp.search(string):
            return True
        else:
            return False
    
def num(string):

    m = re.search('player/(.+?).html', string)
    if m:
        found = m.group(1)
    return found
def csum(l):
    for i in range(1,len(l)):
        l[i]=l[i-1]+l[i]
    l.reverse()
    return l
        
result= requests.get("https://en.wikipedia.org/wiki/List_of_One_Day_International_cricketers")
src = result.content
soup = BeautifulSoup(src, 'lxml')
l1 =soup.find_all("small")
a1=[]
for i in l1:
    k=i.find_all("a")
    a1.append(k)
a2=[]
for i in a1:
    for j in i:
        temp = [j.get_text(),j.get("href")]
        a2.append(temp)
        
 #removing players who have played in more than one team
seen = set()
result1 = []
for item in a2:
    if item[1] not in seen:
        seen.add(item[1])
        result1.append(item)


k=[]
c=[]
for t in result1:
    cric= requests.get("https://en.wikipedia.org"+t[1])
    cont =cric.content
    sp=BeautifulSoup(cont, 'lxml')
    div=sp.find_all("a")
    i=1
    for o in div:
        try:
            if Find(o.get("href")) and (len(t)<3):
                t.append(num(o.get("href")))
        except:
            continue
    try:
        cric= requests.get("http://stats.espncricinfo.com/ci/engine/player/"+t[2]+".html?class=11;template=results;type=allround")
        cont =cric.content
        sp=BeautifulSoup(cont, 'lxml')
        t.pop()
        t.pop()
        data=[]
        columns = sp.findAll('td', text = re.compile('year+'))
        for i in columns:
            rows=i.parent
            h=rows.findAll('td')
            jol=h[4].get_text()
            if jol.strip()[-1]=="*":
                jol=jol[:-1]
            try:
                jol=float(jol)
            except:
                jol=0
            data.append(jol)
        k1=copy.deepcopy(data)
        data.reverse()
        k1=csum(k1)
        temp=copy.deepcopy(t)
        t.extend(data)
        temp.extend(k1)
        k.append(t)
        c.append(temp)
    except:
        continue
    
with open("runs.csv", "w+") as f:
    writer = csv.writer(f)
    writer.writerow(("Player Name",2019,2018,2017,2016,2015,2014,2013,2012,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000,1999))
    writer.writerows(k)
with open("cummulified.csv", "w+") as f:
    writer = csv.writer(f)
    writer.writerow(("Player Name",2019,2018,2017,2016,2015,2014,2013,2012,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000,1999))
    writer.writerows(c)
