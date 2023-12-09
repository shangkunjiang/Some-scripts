import numpy as np
from scipy.interpolate import griddata   # 插入非结构化D-D数据


def bonds_func(atom_name, atom_num,frame, latvec):
    H_index = atom_name.index('H') # 判断H属于第几个元素
    H_start = sum(atom_num[0:H_index]) # 判断坐标矩阵中，第一个氢原子的位置，注意第一个编号为0


    O_index = atom_name.index('O') # 判断O属于第几个元素
    O_start = sum(atom_num[0:O_index]) # 判断坐标矩阵中，第一个O原子的位置，注意第一个编号为0


    bonds = np.zeros([atom_num[O_index], atom_num[H_index]]) # 行（纵向）表示O，列（横向）表示H，成键为1，未成键为0
    for i in range(atom_num[O_index]):
        O = np.array(frame[O_start + i])
        for j in range(atom_num[H_index]):
            H = np.array(frame[H_start+j])
            if np.linalg.norm(H-O) < 1.2:
                bonds[i,j] = 1
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
                elif np.linalg.norm(H2 - O) < 1.2:
                    bonds[i, j] = 1
                elif np.linalg.norm(H3 - O) < 1.2:
                    bonds[i, j] = 1
                elif np.linalg.norm(H4 - O) < 1.2:
                    bonds[i, j] = 1
                elif np.linalg.norm(H5 - O) < 1.2:
                    bonds[i, j] = 1
                elif np.linalg.norm(H6 - O) < 1.2:
                    bonds[i, j] = 1
                elif np.linalg.norm(H7 - O) < 1.2:
                    bonds[i, j] = 1
                elif np.linalg.norm(H8 - O) < 1.2:
                    bonds[i, j] = 1
    return bonds


def water_direction(frame, atom_name, atom_num, bonds):  # 水的方向

    z_vec = np.array([0, 0, 1.0])  # z方向的向量 （这个向量是后面数据处理的参比吗？）

    H_index = atom_name.index('H')  # 判断H是第几个元素
    H_start = sum(atom_num[0:H_index])  # 判断坐标矩阵中，第一个氢原子的位置，注意第一个编号为0
    H_all = frame[H_start:H_start+atom_num[H_index]]


    O_index = atom_name.index('O')  # 判断O属于第几个元素
    O_start = sum(atom_num[0:O_index])  # 判断坐标矩阵中，第一个O原子的位置，注意第一个编号为0
    O_all = frame[O_start:O_start + atom_num[O_index]]

    cos_theta = -2.0*np.ones([atom_num[O_index]])
    for i in range(bonds.shape[0]):
        if sum(bonds[i]) == 2: # 如果该O原子与H原子的成键数为2
            H_center = np.dot(bonds[i],H_all) / 2   # dot函数用于获取两个元素的乘积
            water_vec = H_center - O_all[i]
            cos_theta[i] = np.dot(z_vec, water_vec) / (np.linalg.norm(z_vec) * (np.linalg.norm(water_vec)))

    return cos_theta


def oxygen_dist(frame, atom_name, atom_num, latvec):  # 只适用于第一种元素为基底的情况

    O_index = atom_name.index('O')  # 判断O属于第几个元素
    O_start = sum(atom_num[0:O_index])  # 判断坐标矩阵中，第一个O原子的位置，注意第一个编号为0
    O_all = frame[O_start:O_start + atom_num[O_index]]

    sub_index = atom_name.index('Pt')  # 判断Pt属于第几个元素
    sub_start = sum(atom_num[0:sub_index])  # 判断坐标矩阵中，第一个Pt原子的位置，注意第一个编号为0
    sub_all = frame[sub_start:sub_start + atom_num[sub_index]]

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
    dist = np.empty([O_all.shape[0]])
    for i in range(O_all.shape[0]):
        O = O_all[i]
        O_xy = O[:2]
        sub_y_eval = griddata(xy, y, O_xy)
        dist[i] = abs(sub_y_eval - O[2])
    return dist

