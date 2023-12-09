# 使用流程：
将INCAR和POSCAR文件加上 .init 后缀
  1.bash ./run
  2.bash ./fgradSG.sh
  3.python3 integrateForward.py grad.dat > free_enery.txt
