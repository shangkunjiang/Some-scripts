#!/bin/bash

runvasp="mpirun -np x executable_path"

# ensure that this sequence of MD runs is reproducible
cp  POSCAR POSCAR.init
cp  INCAR INCAR.init
rseed="\nRANDOM_SEED = 311137787 0 0"
echo -e $rseed >> INCAR


i=1
while [ $i -le 50 ] 
do

  # start vasp
  $runvasp

  # ensure that this sequence of MD runs is reproducible
  rseed=$(grep RANDOM_SEED REPORT |tail -1) 
  cp INCAR.init INCAR
  echo $rseed >> INCAR

  # use the last configuration generated in the previous
  # run as initial configuration for the next run
  cp CONTCAR POSCAR

  # backup some important files
  cp REPORT REPORT.$i
  cp vasprun.xml vasprun.xml.$i

  let i=i+1
done

rm grad.dat

i=1

while [ $i -le 1000 ]
do
  if test -f REPORT.$i
  then
    grep cc REPORT.$i |awk '{print $3}' >xxx
    grep b_m REPORT.$i |awk '{print $2}' >fff
    paste xxx fff >> grad.dat

    rm REPORT.$i
    rm vasprun.xml.$i
  fi
  let i=i+1
done

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
