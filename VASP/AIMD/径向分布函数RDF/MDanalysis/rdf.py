# -*- coding: utf-8 -*-
"""
Created on Thu May  6 11:26:56 2021
@author: Jasonkun
"""
import parser
import MDAnalysis as mda
import MDAnalysis.analysis.rdf
import matplotlib.pyplot as plt  # 作图模块
import numpy as np
from MDAnalysis.core.universe import Universe  # 计算质心或型心

if __name__ == '__main__':
    # -----读取文件-----
    file_path = ""
    data_name = "XDATCAR.pdb"
    data_file_name = file_path + data_name

    u = mda.Universe(data_file_name,)  # 读取lammps数据文件
    # 原子选择语句 
    Pt = u.select_atoms("bynum 204 192 220 208 200 196 216 212 236 224 252 240 232 228 248 244")
    S = u.select_atoms("bynum 188")
   
    print(u)
    print(Pt)
    print(S)
    # cal
    # RDF参数
    rdf = MDAnalysis.analysis.rdf.InterRDF(O_H2O, H_H2O, nbins=300, range=(0, 30), exclusion_block=None, density=False)
    rdf.run()
    # plt.plot(rdf.bins, rdf.rdf)
    # plt.show()
    np.savetxt('rdf-O_H2O-H_H2O.txt', np.column_stack((rdf.results.bins, rdf.results.rdf)))
    # print(活性位密度.bins)
    plt.plot(rdf.bins, rdf.rdf)
    plt.show()
