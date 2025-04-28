import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter as xw
import pandas as pd
import numpy as np
from scipy.interpolate import griddata


def bonds_func(atom_name, atom_num,frame, latvec):
    H_index = atom_name.index('H') # 判断H属于第几个元素
    H_start = sum(atom_num[0:H_index]) # 判断坐标矩阵中，第一个氢原子的位置，注意第一个编号为0


    O_index = atom_name.index('O') # 判断O属于第几个元素
    O_start = sum(atom_num[0:O_index]) # 判断坐标矩阵中，第一个O原子的位置，注意第一个编号为0


    bonds = np.zeros([atom_num[O_index], atom_num[H_index]]) # 行（纵向）表示O，列（横向）表示H，成键为1，未成键为0
    bond_length = np.zeros([atom_num[O_index], atom_num[H_index]])  # 行（纵向）表示O，列（横向）表示H，成键为键长，未成键为0
    for i in range(atom_num[O_index]):
        O = np.array(frame[O_start + i])
        for j in range(atom_num[H_index]):
            H = np.array(frame[H_start+j])
            if np.linalg.norm(H-O) < 1.2:
                bonds[i,j] = 1
                bond_length[i, j] = np.linalg.norm(H-O)
            else:   # 因周期性，还需检验相邻周期的H原子是否与该O原子成键
                H1 = H + latvec[0]
                H2 = H - latvec[0]
                H3 = H + latvec[1]
                H4 = H - latvec[1]
                H5 = H + latvec[0] + latvec[1]
                H6 = H + latvec[0] - latvec[1]
                H7 = H - latvec[0] + latvec[1]
                H8 = H - latvec[0] - latvec[1]
                if np.linalg.norm(H1 - O) < 1.2:
                    bonds[i, j] = 1
                    bond_length[i, j] = np.linalg.norm(H1 - O)
                elif np.linalg.norm(H2 - O) < 1.2:
                    bonds[i, j] = 1
                    bond_length[i, j] = np.linalg.norm(H2 - O)
                elif np.linalg.norm(H3 - O) < 1.2:
                    bonds[i, j] = 1
                    bond_length[i, j] = np.linalg.norm(H3 - O)
                elif np.linalg.norm(H4 - O) < 1.2:
                    bonds[i, j] = 1
                    bond_length[i, j] = np.linalg.norm(H4 - O)
                elif np.linalg.norm(H5 - O) < 1.2:
                    bonds[i, j] = 1
                    bond_length[i, j] = np.linalg.norm(H5 - O)
                elif np.linalg.norm(H6 - O) < 1.2:
                    bonds[i, j] = 1
                    bond_length[i, j] = np.linalg.norm(H6 - O)
                elif np.linalg.norm(H7 - O) < 1.2:
                    bonds[i, j] = 1
                    bond_length[i, j] = np.linalg.norm(H7 - O)
                elif np.linalg.norm(H8 - O) < 1.2:
                    bonds[i, j] = 1
                    bond_length[i, j] = np.linalg.norm(H8 - O)
    bond_length2 = np.zeros([bond_length.shape[0],3])
    for i in range(bond_length.shape[0]):
        id = 0
        for j in range(bond_length.shape[1]):
            if bond_length[i,j] >0:
                bond_length2[i, id]=bond_length[i,j]
                id +=1
    bond_count = np.sum(bonds, axis=1)  # Sum up the bonds for each oxygen atom
    return bonds, bond_length2, bond_count


def oxygen_dist(frame, atom_name, atom_num, latvec):  # 只适用于第一种元素为基底的情况
    O_index = atom_name.index('O')  # 判断O属于第几个元素
    O_start = sum(atom_num[0:O_index])  # 判断坐标矩阵中，第一个O原子的位置，注意第一个编号为0
    O_all = frame[O_start:O_start + atom_num[O_index]]
    sub_all = frame[0:atom_num[0]]

    # 确定基底最上层原子（这里假设最上层原子在z方向的距离在1A之内，而最上层与第二层原子间距离大于1A）
    sub_top_layer = []
    sub_peak = sub_all[:,2].max()
    for i in range(sub_all.shape[0]):
        if abs(sub_all[i][2] -sub_peak) < 1:
            sub_top_layer.append(sub_all[i])
            # 增加相邻周期的基底坐标
            sub_top_layer.append(sub_all[i] + latvec[0])
            sub_top_layer.append(sub_all[i] - latvec[0])
            sub_top_layer.append(sub_all[i] + latvec[1])
            sub_top_layer.append(sub_all[i] - latvec[1])
            sub_top_layer.append(sub_all[i] + latvec[0] + latvec[1])
            sub_top_layer.append(sub_all[i] + latvec[0] - latvec[1])
            sub_top_layer.append(sub_all[i] - latvec[0] + latvec[1])
            sub_top_layer.append(sub_all[i] - latvec[0] - latvec[1])



    # 插值
    xy = np.array(sub_top_layer)[:, :2]
    y = np.array(sub_top_layer)[:, 2]
    dist = np.zeros(O_all.shape[0])  # 确保dist数组正确初始化为零
    for i, O in enumerate(O_all):
        O_xy = O[:2]
        sub_y_eval = griddata(xy, y, O_xy, method='linear')
        if sub_y_eval is not None and not np.isnan(sub_y_eval):  # 检查sub_y_eval是否有效
            dist[i] = abs(sub_y_eval - O[2])
        else:
            # Use nearest method if linear results in NaN
            sub_y_eval = griddata(xy, y, O_xy, method='nearest')
            if sub_y_eval is not None:
                dist[i] = abs(sub_y_eval - O[2])
            else:
                dist[i] = np.nan  # Assign NaN if both methods fail
    return dist


filename = 'XDATCAR-4Pt-H3O+100'
# 将文件数据全部按行读入data
with open(filename,'r') as f:
    data = f.readlines()

# 读取晶格常数,存入latvec内
# 读取原子种类及数量，存入atom_name. atom_num
latvec = np.zeros([3, 3])
for i in range(3):
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

# Initialization for storing coordinates of H3O+ oxygen atoms
H3O_coords = []
H3O_frame_ids = []   #序号从0开始
H3O_atom_ids = []   #序号从0开始

for frame_id in range(frames.shape[0]):
    if frame_id % 100 == 0:
        print(frame_id)
    bonds, bond_length2, bond_count = bonds_func(atom_name, atom_num, frames[frame_id], latvec)
    O_index = atom_name.index('O')
    O_start = sum(atom_num[0:O_index])

    # Filtering oxygen atoms with exactly 3 hydrogen bonds
    for i, count in enumerate(bond_count):
        if count == 3:
            # Get the coordinates of the oxygen atom
            O_coords = frames[frame_id, O_start + i]
            O_global_index = O_start + i  # Global index of the oxygen atom in the frame
            H3O_coords.append(O_coords)
            H3O_frame_ids.append(frame_id)
            H3O_atom_ids.append(O_global_index)

# Writing results to an Excel file
workbook = xw.Workbook('H3O_plus_coordinates.xlsx')
worksheet = workbook.add_worksheet("Oxygen Coordinates")

worksheet.write('A1', 'Frame ID')
worksheet.write('B1', 'Oxygen Atom ID')
worksheet.write('C1', 'X Coordinate')
worksheet.write('D1', 'Y Coordinate')
worksheet.write('E1', 'Z Coordinate')

for i, coord in enumerate(H3O_coords):
    worksheet.write(i + 1, 0, H3O_frame_ids[i])
    worksheet.write(i + 1, 1, H3O_atom_ids[i])
    worksheet.write_row(i + 1, 2, coord)

workbook.close()
print("Finished writing coordinates and indices of H3O+ oxygen atoms.")