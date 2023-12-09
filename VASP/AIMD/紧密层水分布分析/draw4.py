import xlrd
import numpy as np
import matplotlib.pyplot as plt
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
theta_current = []

theta_current_pos_1 = []
theta_current_pos = []
theta_current_neg = []
theta_current_neg_1 = []
theta_current_zero = []
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
for i in range(len(dist1)):
    if dist1[i]-dist_current < 0.1:
        if cos_theta1[i] > -2:
            theta_current.append(cos_theta1[i])        # 总的
        if 0.707 < cos_theta1[i] < 1.01:
            theta_current_pos_1.append(cos_theta1[i])  # pos_1表示theta范围在：0~45度
        elif 0.2588 < cos_theta1[i] <= 0.707:
            theta_current_pos.append(cos_theta1[i])    # pos表示theta范围在：45~75度
        elif -0.2588 > cos_theta1[i] >= -0.707:
            theta_current_neg.append(cos_theta1[i])    # neg表示theta范围在：105~135度
        elif -0.707 > cos_theta1[i] > -1.01:
            theta_current_neg_1.append(cos_theta1[i])    # neg表示theta范围在：135~180度
        elif 0.2588 >= cos_theta1[i] >= -0.2588:
            theta_current_zero.append(cos_theta1[i])   # zero表示theta范围在：75~105度

    else:
        num_current_pos_1 = len(theta_current_pos_1)   # theta范围在：0~45度的数目
        num_current_pos = len(theta_current_pos)       # theta范围在：45~75度的数目
        num_current_neg = len(theta_current_neg)
        num_current_neg_1 = len(theta_current_neg_1)
        num_current_zero = len(theta_current_zero)
        num_current = len(theta_current)
        if num_current >0:
            frac_neg_1.append(num_current_neg_1 / num_current)
            frac_neg.append(num_current_neg / num_current)
            frac_pos.append(num_current_pos / num_current)
            frac_pos_1.append(num_current_pos_1 / num_current)
            frac_zero.append(num_current_zero / num_current)
        else:
            frac_neg_1.append(0)
            frac_neg.append(0)
            frac_pos.append(0)
            frac_pos_1.append(0)
            frac_zero.append(0)

        if len(theta_current_neg_1) == 0:
            theta_current_neg_1.append(0)
        if len(theta_current_neg) == 0:
            theta_current_neg.append(0)
        if len(theta_current_pos) == 0:
            theta_current_pos.append(0)
        if len(theta_current_pos_1) == 0:
            theta_current_pos_1.append(0)
        if len(theta_current_zero) == 0:
            theta_current_zero.append(0)
        if len(theta_current) == 0:
            theta_current.append(0)

        cos_theta2.append(np.mean(theta_current))           # mean()：求均值
        cos_theta2_neg_1.append(np.mean(theta_current_neg_1))
        cos_theta2_neg.append(np.mean(theta_current_neg))
        cos_theta2_pos.append(np.mean(theta_current_pos))
        cos_theta2_pos_1.append(np.mean(theta_current_pos_1))
        cos_theta2_zero.append(np.mean(theta_current_zero))
        dist2.append(dist_current)

        dist_current = dist1[i]
        theta_current = []
        theta_current_pos_1 = []
        theta_current_pos = []
        theta_current_neg = []
        theta_current_neg_1 = []
        theta_current_zero = []


workbook = xw.Workbook('4-result.xls')
worksheet1 = workbook.add_worksheet("sheet1")
worksheet1.write_row('A1', ['distance/A', 'cos_theta', 'cos_thera_positive_1', 'cos_thera_positive', 'cos_thera_negative', 'cos_thera_negative_1', 'cos_thera_zeros', 'frac_pos_1', 'frac_pos', 'frac_neg', 'frac_neg_1', 'frac_zero'])
worksheet1.write_column('A2', np.array(dist2).reshape(-1,1))
worksheet1.write_column('B2', np.array(cos_theta2).reshape(-1,1))
worksheet1.write_column('C2', np.array(cos_theta2_pos_1).reshape(-1,1))
worksheet1.write_column('D2', np.array(cos_theta2_pos).reshape(-1,1))
worksheet1.write_column('E2', np.array(cos_theta2_neg).reshape(-1,1))
worksheet1.write_column('F2', np.array(cos_theta2_neg_1).reshape(-1,1))
worksheet1.write_column('G2', np.array(cos_theta2_zero).reshape(-1,1))
worksheet1.write_column('H2', np.array(frac_pos_1).reshape(-1,1))
worksheet1.write_column('I2', np.array(frac_pos).reshape(-1,1))
worksheet1.write_column('J2', np.array(frac_neg).reshape(-1,1))
worksheet1.write_column('K2', np.array(frac_neg_1).reshape(-1,1))
worksheet1.write_column('L2', np.array(frac_zero).reshape(-1,1))
workbook.close()

plt.scatter(dist2, cos_theta2, s=0.1)
plt.show()

