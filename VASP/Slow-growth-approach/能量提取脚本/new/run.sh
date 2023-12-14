#!/bin/bash

rm grad.dat

grep cc REPORT |awk '{print $3}' >xxx
grep b_m REPORT |awk '{print $2}' >fff
paste xxx fff >> grad.dat

sort -n grad.dat >grad_.dat
mv grad_.dat grad.dat
rm xxx
rm fff

python3 - << END
import string
import sys
f='grad.dat'
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

with open ('free_energy.txt', 'w') as f:
    tg=0.0
    # f.write(r[0],tg)
    print(r[0],tg, file=f)
    for i in range(1,len(r)):
        gg=0.5*(r[i]-r[i-1])*(g[i]+g[i-1])
        tg+=gg
        # f.write(r[i],tg)
        print(r[i],tg, file=f)
END
