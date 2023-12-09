import xlrd
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter as xw

xlsx =xlrd.open_workbook('1-result.xls')
sheet = xlsx.sheets()[0]
dist = sheet.col_values(0)[1:]
cos_theta = sheet.col_values(1)[1:]
for i in range(len(cos_theta)):
    if cos_theta[i] == -2:
        cos_theta[i] = -1
    else:
        cos_theta[i] = np.degrees(np.arccos(cos_theta[i]))

temp = np.vstack((np.array(dist), np.array(cos_theta)))
print(temp.shape)
temp = temp[:,temp[1].argsort()]  # 按第一行排序
dist1 = temp[0, :]
cos_theta1 = temp[1, :]

cos_theta2 = cos_theta1[0]
cos_theta_current = cos_theta1[0]
count_atom_current = 0
count_atom = []
count_theta =[]
for i in range(len(cos_theta1)):
    if cos_theta1[i] > -1 and 2.02 <dist1[i] < 4.57:
        if cos_theta1[i] - cos_theta_current < 5:
            count_atom_current += 1
        else:
            count_atom.append(count_atom_current)
            count_theta.append(cos_theta_current)
            count_atom_current = 1
            cos_theta_current = cos_theta1[i]

# 存入数据

workbook = xw.Workbook('2-result.xls')
worksheet1 = workbook.add_worksheet("sheet1")
worksheet1.write_row('A1', ['degree', 'count'])
worksheet1.write_column('A2', np.array(count_theta).reshape(-1,1))
worksheet1.write_column('B2', np.array(count_atom).reshape(-1,1))
workbook.close()

plt.plot(count_theta, count_atom)
plt.show()
