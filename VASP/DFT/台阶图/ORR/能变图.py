# -*- coding: utf-8 -*-
# @Time         : 2023/5/15 0015 21:18
# @Author       : Jasonkun
# @FileName     : 能变图1.2.py
# @Software     : PyCharm
# @Description  ：
"""
# -----------------------------------------

# -----------------------------------------
"""
import numpy as np
import matplotlib.pyplot as plt


def linear_interp(xco, yco):
    x0, x1 = xco[0] + label_length / 2, xco[1] - label_length / 2
    y0, y1 = yco[0], yco[1]
    xfi = np.linspace(x0, x1, 51)
    yfi = np.linspace(y0, y1, 51)
    return xfi, yfi


def add_mep(x, y, label_color, **kwargs):
    # Length, width of lines and labels
    line_width = 1.0
    label_width = 1.5

    assert len(x) == len(y)
    # assert len(x) == len(y) == len(label_color)
    react_coord = np.array(x)
    energy = np.array(y)
    energy = energy - energy[0]
    # Draw the line connecting all images
    react_coord_fi = np.array([])
    energy_fi = np.array([])
    for i in range(energy.size - 1):
        xfi, yfi = linear_interp(react_coord[i:i + 2], energy[i:i + 2])
        react_coord_fi = np.append(react_coord_fi, xfi)
        energy_fi = np.append(energy_fi, yfi)
    axes.plot(react_coord_fi, energy_fi, linewidth=line_width, **kwargs)
    # Add energy levels
    for i, coord in enumerate(react_coord):
        label_x = np.array([coord - label_length / 2, coord + label_length / 2])
        label_y = np.array([energy[i], energy[i]])
        axes.plot(label_x, label_y, linewidth=label_width, color=label_color)
    # 在横线上显示数值
    # for i in x[1:-1]:   # 不显示两端数据
    #     plt.text(x[i] - 0.23, y[i] + 0.005, '%.2f'%y[i])

    # Adjusting the figures
    axes.set_xlabel("Reaction coordinate", fontsize="large")
    axes.set_ylabel("Free Energy (eV)", fontsize="large")

    plt.xticks(x, ['$\mathregular{O_{2}}$', '*OOH', '*O', '*OH', '$\mathregular{H_{2}O}$'])
    # Legend
    axes.legend(edgecolor="w")
    # Save the figure
    fig.tight_layout()
    plt.savefig('Figure.tif', bbox_inches='tight', dpi=300, format='tif')


if __name__ == "__main__":
    # 画图
    fig, axes = plt.subplots(figsize=(5, 4))
    color = ['r', '#4e62ab', '#479db4', '#87d0a5', '#fcb96a']
    # Axes and spines settings
    ymin = -2.0
    ymax = 2.0

    label_length = 0.5

    x = [0, 1, 2, 3, 4]
    # 可以增加Y的数量 画多个台阶
    y = {'Pure-Pt(111)': [0, -0.1033, -0.2034, -0.4584, 0, color[0]]  # 台阶位置
         }
    for y_key, y_values in y.items():
        add_mep(x, y_values[0:-1], label_color=y_values[-1], color=y_values[-1], linestyle="--", label=y_key)
