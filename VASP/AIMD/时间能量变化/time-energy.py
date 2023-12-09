# -*- coding: utf-8 -*-
# @Time         : 2023/7/6 0006 7:52
# @Author       : Jasonkun
# @FileName     : time-energy.py
# @Software     : PyCharm
# @Description  ：
"""
# -----------------------------------------

# -----------------------------------------
"""

# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import os
import subprocess
import sys


if __name__ == "__main__":

    print('')
    OSZICAR_path = os.popen('pwd').read()
    print('Your path is:' + OSZICAR_path)

    if os.path.exists('OSZICAR'):
        child = subprocess.Popen("grep EK OSZICAR > Energy.txt", shell=True)
        print('Energy data is stored in Energy.txt')
        child.wait()

        file_path = OSZICAR_path + ''
        file_name = file_path.replace('\n', '') + "Energy.txt"  # log 文件名

        time = []
        energy = []

        with open(file_name, 'r') as file:
            for line in file:
                line = line.strip()
                words = line.split()
                if len(words) >= 9:
                    time_value = float(words[0])
                    time.append(time_value)

                    energy_value = float(words[8])
                    energy.append(energy_value)
                    

        plt.figure(figsize=(6,3))  # 图片大小
        plt.plot(time, energy)
        plt.xlabel('Time (fs)')
        plt.ylabel('Energy (eV)')
        plt.xlim(xmin=0)
        plt.savefig('energy.tif', bbox_inches='tight', dpi=80, format='tif')
        print('')
        print('Energy.tif Already generated!')
        print('')

    else:
        msg = "Sorry, the file OSZICAR does not exist."
        print(msg)
        sys.exit(1)
