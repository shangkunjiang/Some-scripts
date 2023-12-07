import numpy as np
import math


# 求两原子的距离


# 定义计算最小距离的函数
def calculate_min_distance(atom1, atom2, latvec):
    min_distance_atom1_atom2 = float('inf')  # 初始化为无限大
    for atom1_i in (atom1, atom1 + latvec[0], atom1 - latvec[0], atom1 + latvec[1], atom1 - latvec[1],
                    atom1 + latvec[0] + latvec[1], atom1 + latvec[0] - latvec[1],
                    atom1 - latvec[0] + latvec[1], atom1 - latvec[0] - latvec[1]):

        for atom2_i in (atom2, atom2 + latvec[0], atom2 - latvec[0], atom2 + latvec[1], atom2 - latvec[1],
                        atom2 + latvec[0] + latvec[1], atom2 + latvec[0] - latvec[1],
                        atom2 - latvec[0] + latvec[1], atom2 - latvec[0] - latvec[1]):
            distance_atom1_atom2_i = np.linalg.norm(atom2_i - atom1_i)
            # print(distance_atom1_atom2_i)
            if distance_atom1_atom2_i < min_distance_atom1_atom2:
                min_distance_atom1_atom2 = distance_atom1_atom2_i

    return min_distance_atom1_atom2


# 读取文件
filename = 'D:/data/DMM/vasp-data/AIMD/0.2/shujuchuli/find-structure/XDATCAR'  # 注意斜杠方向

# 保存数据的文件
save_file_name = "D:/data/DMM/vasp-data/AIMD/0.2/shujuchuli/find-structure/Pt31-O40-dis"  # 文件名
save_file = open(save_file_name, "w", encoding='UTF-8')

# 将文件数据全部按行读入data
with open(filename, 'r') as f:
    data = f.readlines()

# 读取晶格常数,存入latvec内
# 读取原子种类及数量，存入atom_name. atom_num
latvec = np.zeros([3, 3])
for i in range(3):  # i指第i行
    if len(data[i].strip()) > 0:  # 判断是否为空行，如果不是空行，则后面三行为晶胞参数
        for j in range(3):
            latvec[j] = data[i + j + 1].split()
        atom_name = data[i + 4].split()
        atom_num = [int(x) for x in data[i + 5].split()]
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
        temp_frac = [float(x) for x in data[i].split()]  # 将该行以浮点数据形式存入temp_frac
        frames[fr_id, k, :] = np.dot(temp_frac, latvec)  # 转换为笛卡尔坐标
        k += 1

# 计算两原子之间的距离

atom_num_1 = 30  # 要求距离的的两个原子序号，这里序号从1开始，VESTA中序号从1开始
atom_num_2 = 39
result = []
for frame in frames:
    atom1 = frame[atom_num_1 - 1]
    atom2 = frame[atom_num_2 - 1]

    min_distance_atom1_atom2 = calculate_min_distance(atom1, atom2, latvec)

    result_row = min_distance_atom1_atom2
    result.append(result_row)

for item in result:
    print('%.5f\t' % (item))
    save_file.write('%.5f\t' % (item) + '\n')

save_file.close()
