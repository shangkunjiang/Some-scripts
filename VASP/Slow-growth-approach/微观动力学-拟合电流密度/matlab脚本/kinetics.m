clc;
clear all
close all
for i=0:0.01:1.2
    fp=fopen('C:\Users\Jasonkun\Documents\MATLAB\电流密度计算\non-contact\Kinetics-non-contact.txt','a');
    if i==0
        fprintf(fp,'Urhe xo2dl t to2 tooh to toh jk lgj');
        fprintf(fp,'\n');
    end
    U_rhe=i;
    % 正反应 能垒
    dE1=0.07+0.5*(U_rhe-1.23);
    dE2=0.29+0.5*(U_rhe-1.23);
    dE3=0.04+0.5*(U_rhe-1.23);
    dE4=0.03+0.5*(U_rhe-1.23);
    % 逆反应 能垒
    dE_1=0.09-0.5*(U_rhe-1.23);
    dE_2=0.47-0.5*(U_rhe-1.23);
    dE_3=0.33-0.5*(U_rhe-1.23);
    dE_4=0.21-0.5*(U_rhe-1.23);

    % kinetics
    syms t xo2dl to2 tooh toh to k1 k_1 k2 k_2 k3 k_3 k4 k_4 k5 k_5 k6 k_6

    xo2=2.34*10^(-5);
    
    xh2o=1;
    k1=1*10^5;  % O2扩散速率 用以调整电流密度大小
    k_1=1*10^5; % O2扩散速率 用以调整电流密度大小
    k2=10^8*exp(-38.6817*0.15); % O2吸附能垒
    k_2=10^8;   
    k3=1.23*10^(9)*exp(-38.6817*dE1);  %*OOH质子化
    k_3=1.23*10^(9)*exp(-38.6817*dE_1);%*OOH质子化
    k4=1.23*10^(9)*exp(-38.6817*dE2);
    k_4=1.23*10^(9)*exp(-38.6817*dE_2);
    k5=1.23*10^(9)*exp(-38.6817*dE3);
    k_5=1.23*10^(9)*exp(-38.6817*dE_3);
    k6=1.23*10^(9)*exp(-38.6817*dE4);
    k_6=1.23*10^(9)*exp(-38.6817*dE_4);


    y1=k1*xo2-k_1*xo2dl-k2*t*xo2dl+k_2*to2== 0;
    y2=k2*t*xo2dl-k_2*to2-k3*to2+k_3*tooh == 0;
    y3=k3*to2-k_3*tooh-k4*tooh+k_4*xh2o*to == 0;
    y4=k4*tooh-k_4*xh2o*to-k5*to+k_5*toh == 0;
    y5=k5*to-k_5*toh-k6*toh+k_6*xh2o*t == 0;
    y6=t+to2+tooh+toh+to-1 == 0;
    y7=xo2dl>0;
    y8=t<1;


    [xo2dl,t,to2,tooh,toh,to]=solve(y1,y2,y3,y4,y5,y6,y7,y8,xo2dl,t,to2,tooh,toh,to);
    r=k4*tooh-k_4*xh2o*to;
    jk=-4*4*0.2032*r;
    lgj=log10(abs(jk));
    fprintf(fp,'%f ',U_rhe);
    fprintf(fp,'%f ',xo2dl);
    fprintf(fp,'%f ',t);
    fprintf(fp,'%f ',to2);
    fprintf(fp,'%f ',tooh);
    fprintf(fp,'%f ',to);
    fprintf(fp,'%f ',toh);
    fprintf(fp,'%f ',jk);
    fprintf(fp,'%f ',lgj);
    fprintf(fp,'\n');
    fclose(fp);
end
