这个文件提取的内容涉及到traj_nvt_300K.lammpstrj文件中格式的差异，请按需要修改。

在IN文件中可以设定traj_nvt_300K.lammpstrj文件输出的格式
eg：
dump dmAll all custom 1000 traj_nvt_300K.lammpstrj id mol type x y z vx vy vz
dump_modify dmAll sort id
