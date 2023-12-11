# -*- coding: utf-8 -*-
# @Time         : 2023/7/25 0025 11:03
# @Author       : Jasonkun
# @FileName     : dos-vaspkit.py
# @Software     : PyCharm
# @Description  ：
"""
# -----------------------------------------

# -----------------------------------------
"""
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator


def read_file(file_name):
    file = open(file_name, "r", encoding='UTF-8')
    line_number = 5
    max_lines = len(open(file_name, 'r').readlines())  # 最大行数，无严格要求，大于可能的数据行数即可
    patten = r'\s+-?\d+\.\d+' * 5
    data = np.zeros((line_number, max_lines))  # 数字对应几列数据
    count = 0
    for b in range(1, max_lines):
        line = file.readline()
        match = re.match(patten, line)
        if match is not None:
            count = count + 1
            match = re.findall(r"[-+]?\d*\.\d+", line)
            for c in range(0, line_number):
                data[c, count] = float(match[c])  # 将每一列的值赋予给data字典
    data_list = data[:, 0:count + 1]  # 切除多余 0 元素,消去首尾相连，即原点坐标
    return data_list


if __name__ == "__main__":
    # 读取文件
    file_path = ''
    file_name_1 = file_path + "PDOS_USER.dat"
    file_path = ''
    file_name_2 = file_path + "PDOS_USER.dat"
    labels = ['Contact Mode', 'Non-Contact Mode']
    c_map = ['orange', 'r', '#5c7bd9']

    # 提取数据
    data_1 = read_file(file_name_1)
    data_2 = read_file(file_name_2)

    # 画图
    figure, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 4), sharex=True)  # 共享x轴

    # data_1
    ax1.fill_between(data_1[0], [x/16 for x in data_1[3]], facecolor=c_map[0], alpha=1, label='Pt-5d')
    ax1.fill_between(data_1[0], [x/16 for x in data_1[4]], facecolor=c_map[0], alpha=1)

    ax1.plot(data_2[0], [x/2 for x in data_1[1]], linestyle='-', linewidth=1, c=c_map[1], label='O-2p')  # 将每一列数据都绘入图中
    ax1.plot(data_2[0], [x/2 for x in data_1[2]], linestyle='-', linewidth=1, c=c_map[1])

    # data_2
    ax2.fill_between(data_2[0], [x/16 for x in data_2[3]], facecolor=c_map[0], alpha=1, label='Pt-5d')
    ax2.fill_between(data_2[0], [x/16 for x in data_2[4]], facecolor=c_map[0], alpha=1)

    ax2.plot(data_2[0], [x/2 for x in data_2[1]], linestyle='-', linewidth=1, c=c_map[1], label='O-2p')
    ax2.plot(data_2[0], [x/2 for x in data_2[2]], linestyle='-', linewidth=1, c=c_map[1])

    ax1.text(-7.8, 3.5, labels[0], va='center')
    ax2.text(-7.8, 3.5, labels[1], va='center')

    # -----d带中心-----
    ax1.plot([-2.649, -2.649], [-4, 4], '--', c=c_map[2], linewidth=1)
    ax1.text(-0.5, -3, '$\mathregular{ε_{d}}$=-2.649 eV', va='center', c=c_map[2])
    ax2.plot([-2.572, -2.572], [-4, 4], '--', c=c_map[2], linewidth=1)
    ax2.text(-0.5, -3, '$\mathregular{ε_{d}}$=-2.572 eV', va='center', c=c_map[2])

    # Y轴标签
    plt.text(-9.2, 5, 'PDOS (states/eV)', va='center', rotation='vertical')
    plt.xlabel('Energy (eV)')

    # 绘图参数
    plt.xlim((-8, 2))  # x轴坐标范围
    ax1.set_ylim((-4, 4))  # y轴坐标范围
    ax2.set_ylim((-4, 4))  # y轴坐标范围
    # 设置坐标间隔
    ax = plt.gca()
    x_major_locator = MultipleLocator(2)
    ax.xaxis.set_major_locator(x_major_locator)
    ax1.legend(frameon=False)  # 显示图例

    # 设置子图间隔 位置
    plt.subplots_adjust(left=0.125,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.2,
                        hspace=0)

    # plt.show()
    plt.savefig('PDOS.tif', bbox_inches='tight', dpi=300, format='tif')  # bbox_inches 设置为紧凑型，去掉白边
