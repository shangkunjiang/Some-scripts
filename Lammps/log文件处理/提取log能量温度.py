# -*- coding:utf-8 -*-
import re
import prettytable as pt
import matplotlib.pyplot as plt
import numpy as np
import sys


def draw(label: str, unit: str, datanumber: int, number: int, color: str):
    ax = plt.subplot(number)
    ax.plot(time, data[datanumber], color=color, label=label)
    font = {'family': 'Times New Roman',
            'weight': 'normal',
            'size': 20,
            }
    plt.xlabel('step', font)
    plt.ylabel(label + '(' + unit + ')', font)
    plt.legend()


if __name__ == "__main__":
    file_name = "log.lammps"  # log 文件名
    f = open(file_name, "r", encoding='UTF-8')
    jump_step = 0  # 需要跳过的step数，主要用于忽略势能最小化或弛豫产生的输出数据
    max_lines = len(open(file_name, 'r').readlines())  # 最大行数，大于可能的数据行数即可

    line_number = 0
    line_data = ''

    lines = f.readlines()
    for line_temp in lines:
        if "thermo_style" in line_temp:
            line_data = line_temp
    line_data = line_data.split()
    print(line_data)
    line_number = len(line_data)
    print(line_number)
    line_number = line_number - 2  # 排除前两列
    # 输出列属性
    table = pt.PrettyTable()
    table.align = 'c'
    table.valign = 'm'
    table.field_names = ["line", "type"]
    for i in range(1, line_number+2):
        table.add_row([str(i), line_data[i]])
    print(table)

    patten = r'\s+' + '[-?0-9\-\+\.eE]+\s+' * line_number

    data = np.zeros((line_number, max_lines))  # 数字对应几列数据

    f = open(file_name, "r", encoding='UTF-8')
    count = -1
    for i in range(1, max_lines):
        line = f.readline()
        # print(line)
        if re.match(r'(Total wall)', line) is not None:
            break
        match = re.match(patten, line)
        if match is not None:
            # print(match.groups()) # 这里的data数据点与log文件中顺序对应
            count = count + 1
            match = re.findall(r"([-?0-9+.eE]+)", line)
            # match = re.findall(r"([-?0-9\-\+\.eE]+)", line)
            for i in range(line_number):
                data[i, count] = float(match[i])
            if data[0, count] <= jump_step:
                count = -1
    data = data[:, 0:count]  # 切除多余 0 元素
    time = data[0] * 10  # fs
    # fig = plt.figure()
    plt.figure(figsize=(15, 10), dpi=80)  # 图片大小
    draw(line_data[3], 'K', 1, 221, 'y')  # 图片标签，单位，data[],图片位置，图片颜色
    draw(line_data[4], 'g/cm^3', 2, 222, 'r')
    draw(line_data[8], 'KJ', 6, 223, 'b')
    draw(line_data[9], 'KJ', 7, 224, 'g')

    plt.show()
