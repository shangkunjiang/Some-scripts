"""
# -----------------------------------------
1.control 提取数据
# -----------------------------------------
"""


import numpy as np
from functions import bonds_func, water_direction, oxygen_dist  # 从function模块中导入import后面的几个函数，这几个函数已经定义好了
import matplotlib.pyplot as plt
import xlsxwriter as xw

filename = 'XDATCAR'
# 将文件数据全部按行读入data
with open(filename,'r') as f:
    data = f.readlines()

# 读取晶格常数,存入latvec内
# 读取原子种类及数量，存入atom_name. atom_num
latvec = np.zeros([3, 3])
for i in range(3):   # i指第i行
    if len(data[i].strip()) > 0: # 判断是否为空行，如果不是空行，则后面三行为晶胞参数
        for j in range(3):
            latvec[j]=data[i + j + 1].split()
        atom_name = data[i+4].split()
        atom_num = [int(x) for x in data[i+5].split()]
        break

# 读取数据帧数,存入fr_num
for i in reversed(range(len(data))):
    if 'Direct configuration=' in data[i]:
        fr_num = int(data[i].split()[2])
        break

# 将data分隔为每一帧的坐标数据，存入frames
k = -1
fr_id = -1
frames = np.zeros([fr_num, sum(atom_num), 3])
for i in range(len(data)):
    if 'Direct configuration=' in data[i]:
        k = 0
        fr_id += 1
    elif k > -1:
         temp_frac = [float(x) for x in data[i].split()] # 将该行以浮点数据形式存入temp_frac
         frames[fr_id, k, :] = np.dot(temp_frac,latvec)     #转换为笛卡尔坐标
         k += 1

cos_theta_all = []
distance_all = []
frame_id_all = []
for i in range(frames.shape[0]):
    if i % 100 == 0:
        print(i)
    bonds = bonds_func(atom_name, atom_num, frames[i], latvec)
    cos_theta = water_direction(frames[i], atom_name, atom_num, bonds)
    distance = oxygen_dist(frames[i], atom_name, atom_num, latvec)
    frame_id = np.ones_like(cos_theta)*i

    cos_theta_all.append(cos_theta)
    distance_all.append(distance)
    frame_id_all.append(frame_id)

print(distance_all)

workbook = xw.Workbook('1-result.xls')
worksheet1 = workbook.add_worksheet("sheet1")
worksheet1.write_row('A1', ['distance/A', 'cos_theta', 'frame_id'])
worksheet1.write_column('A2', np.array(distance_all).reshape(-1,1))
worksheet1.write_column('B2', np.array(cos_theta_all).reshape(-1,1))
worksheet1.write_column('C2', np.array(frame_id_all).reshape(-1,1))

plt.scatter(distance_all, cos_theta_all, s=0.1)   # s表示大小
plt.show()



