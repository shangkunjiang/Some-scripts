#!/usr/bin/python

import string
import sys

f=sys.argv[1]

f=open(f,'r')

r=[]
g=[]

for line in f.readlines():
  line = line.split()
  num=len(line)
  # print(line)
  if len(line)==2:
    r.append(float(line[0]))
    g.append(float(line[1]))
 
f.close()

tg=0.0
print(r[0],tg)
for i in range(1,len(r)):
  gg=0.5*(r[i]-r[i-1])*(g[i]+g[i-1])
  tg+=gg
  print(r[i],tg)
