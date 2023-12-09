import xlrd  # xlrd读excel，xlwt是写excel
import numpy as np   # 数学函数包
import matplotlib.pyplot as plt  #绘图库
import xlsxwriter as xw

xlsx =xlrd.open_workbook('1-result.xls')
sheet = xlsx.sheets()[0]
dist = sheet.col_values(0)[1:]
cos_theta = sheet.col_values(1)[1:]

temp = np.vstack((np.array(dist), np.array(cos_theta)))
print(temp.shape)
temp = temp[:,temp[0].argsort()]  # 按第一行排序
dist1 = temp[0, :]
cos_theta1 = temp[1, :]

dist_current = dist1[0]
count_atom_current = 0
count_atom_current_pos_1 = 0
count_atom_current_pos = 0
count_atom_current_neg = 0
count_atom_current_neg_1 = 0
count_atom_current_zero = 0
cos_theta2 = []
cos_theta2_pos_1 = []
cos_theta2_pos = []
cos_theta2_neg = []
cos_theta2_neg_1 = []
cos_theta2_zero = []
frac_pos_1 = []
frac_pos = []
frac_neg = []
frac_neg_1 = []
frac_zero = []
dist2 = []
count_atom = []
count_atom_pos_1 = []
count_atom_pos = []
count_atom_neg = []
count_atom_neg_1 = []
count_atom_zero = []
for i in range(len(dist1)):
    if dist1[i]-dist_current < 0.1:
        if cos_theta1[i] > -2:
            count_atom_current += 1
            if 0.707 < cos_theta1[i] < 1.01:
                count_atom_current_pos_1 += 1
            elif 0.2588 < cos_theta1[i] <= 0.707:
                count_atom_current_pos += 1
            elif -0.2588 > cos_theta1[i] >= -0.707:
                count_atom_current_neg += 1
            elif -0.707 > cos_theta1[i] > -1.01:
                count_atom_current_neg_1 += 1
            elif 0.2588 >= cos_theta1[i] >= -0.2588:
                count_atom_current_zero += 1


    else:
        dist_current = dist1[i]
        count_atom.append(count_atom_current)
        count_atom_pos_1.append(count_atom_current_pos_1)
        count_atom_pos.append(count_atom_current_pos)
        count_atom_neg.append(count_atom_current_neg)
        count_atom_neg_1.append(count_atom_current_neg_1)
        count_atom_zero.append(count_atom_current_zero)
        dist2.append(dist_current)

        count_atom_current = 1
        if 0.707< cos_theta1[i] < 1.01:
            count_atom_current_pos_1 = 1
            count_atom_current_pos = 0
            count_atom_current_neg_1 = 0
            count_atom_current_neg = 0
            count_atom_current_zero = 0
        elif 0.2588 < cos_theta1[i] <= 0.707:
            count_atom_current_pos_1 = 0
            count_atom_current_pos = 1
            count_atom_current_neg = 0
            count_atom_current_zero = 0
        elif -0.2588 > cos_theta1[i] >= -0.707:
            count_atom_current_pos_1 = 0
            count_atom_current_pos = 0
            count_atom_current_neg = 1
            count_atom_current_neg_1 = 0
            count_atom_current_zero = 0
        elif -0.707 > cos_theta1[i] > -1.01:
            count_atom_current_pos_1 = 0
            count_atom_current_pos = 0
            count_atom_current_neg = 0
            count_atom_current_neg_1 = 1
            count_atom_current_zero = 0
        elif 0.2588 >= cos_theta1[i] >= -0.2588:
            count_atom_current_pos_1 = 0
            count_atom_current_pos = 0
            count_atom_current_neg = 0
            count_atom_current_neg_1 = 0
            count_atom_current_zero = 1
        else:
            count_atom_current_pos_1 = 0
            count_atom_current_pos = 0
            count_atom_current_neg = 0
            count_atom_current_neg_1 = 0
            count_atom_current_zero = 0

workbook = xw.Workbook('3-result.xls')
worksheet1 = workbook.add_worksheet("sheet1")
worksheet1.write_row('A1', ['distance/A', 'all', 'pos_1', 'pos', 'neg', 'neg_1', 'zero'])
worksheet1.write_column('A2', np.array(dist2).reshape(-1,1))
worksheet1.write_column('B2', np.array(count_atom).reshape(-1,1))
worksheet1.write_column('C2', np.array(count_atom_pos_1).reshape(-1,1))
worksheet1.write_column('D2', np.array(count_atom_pos).reshape(-1,1))
worksheet1.write_column('E2', np.array(count_atom_neg).reshape(-1,1))
worksheet1.write_column('F2', np.array(count_atom_neg_1).reshape(-1,1))
worksheet1.write_column('G2', np.array(count_atom_zero).reshape(-1,1))
workbook.close()

plt.scatter(dist2, count_atom, s=0.1)
plt.show()