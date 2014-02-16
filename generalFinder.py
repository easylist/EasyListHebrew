import sys
import re

class Filter(object):
    def __init__(self,fil,typ,domain):
        self.filter=fil
        self.typ=typ
        self.domain=domain

    def __str__(self):
        return ','.join(sorted(self.domain))+self.typ+self.filter

regex=re.compile(r"^([a-zA-Z0-9-.]+)(#{2}[#.]?)(.*)",re.MULTILINE)
regex2=re.compile(r"^([a-zA-Z0-9-.]+[,][a-zA-Z0-9-.,]+)(#{2}[#.]?)(.*)",re.MULTILINE)

with open ('EasyListHebrew.txt') as f:
    l=f.read()

one= regex.findall(l)
general= regex2.findall(l)

dic_res={}
for lst in general:
    dic_res[lst[1]+lst[2]]=Filter(lst[2],lst[1], lst[0].split(','))
for lst in one:
    key=lst[1]+lst[2]
    if key in dic_res:
        dic_res[key].domain.append(lst[0])
    else:
        dic_res[key]=Filter(lst[2],lst[1], [lst[0],])
#print all keys with the same vlas
sor=sorted([x for x in dic_res.values() if len(x.domain)>1],key=lambda x:x.typ + x.filter)
for val in sor:
    print val
    
print '\nfilters to delete:'
filters=[(x.typ,x.filter) for x in sor]
for o in one:   
    if (o[1],o[2]) in filters:
        print ''.join(o)