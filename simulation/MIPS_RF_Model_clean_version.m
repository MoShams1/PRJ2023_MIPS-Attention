


% Mohammad Shams <MoShamsCBR@gmail.com>
% June 2023



clc
clear
close all



% ###############################################

% key model parameters

rf_std = 5;
recruit_win = (-30:30);


A1=-.5;
mu1=0;
std1=12;

A2=0;
mu2=5;
std2=3;

A3=0;
mu3=-7;
std3=3;

rf_stds_coeff = A1 * exp(-(recruit_win - mu1).^2 / (2 * std1^2)) + ...
A2 * exp(-(recruit_win - mu2).^2 / (2 * std2^2)) + ...
A3 * exp(-(recruit_win - mu3).^2 / (2 * std3^2)) + 1;
% -----------------------------------------------

% recruit kernel

A1=10;
mu1=5;
std1=3;

A2=-A1;
mu2=-mu1;
std2=std1;

recruit_kernel = A1 * exp(-(recruit_win - mu1).^2 / (2 * std1^2)) + ...
A2 * exp(-(recruit_win - mu2).^2 / (2 * std2^2));


% ###############################################

recruit_win_sz = length(recruit_win);  % >>> MUST BE AN ODD INTEGER
assert(mod(recruit_win_sz,2)==1)

x = 1:1000;
att_foc = length(x)/2;  % focal point of attention
rf_centers = x;
rf_stds = rf_std*ones(length(rf_centers));

% test range
probe_poss = att_foc-99:att_foc+100;


figure('Units','normalized','OuterPosition',[.5 .1 .35 .8])
hold on

% plot the spatial profile of the illusory shift


% attention
plot_rf_dist = 1;
rf_means = rf_centers;

win = att_foc-(recruit_win_sz-1)/2:att_foc+(recruit_win_sz-1)/2;

% plot the recruit kernel
subplot(4,1,1)
kernel_x = win-att_foc;
plot(kernel_x, recruit_kernel, 'ko-', 'linewidth',1)
line([kernel_x(1) kernel_x(end)], [0 0], 'color','k', 'linestyle','--')
pbaspect([1 .25 1])
xlabel 'Kernel wrt focus of attention'
ylabel 'RF-center shift mag.'

% plot the std kernel
subplot(4,1,2)
plot(kernel_x, rf_stds_coeff, 'ko-', 'linewidth',1)
line([kernel_x(1) kernel_x(end)], [1 1], 'color','k', 'linestyle','--')
pbaspect([1 .25 1])
xlabel 'Kernel wrt focus of attention'
ylabel 'RF-width rescale coeff.'

rf_means(win) = rf_means(win) - recruit_kernel;
rf_stds(win) = rf_stds(win).*rf_stds_coeff;

response_mat = gen_rf_response_mat(x, rf_means, rf_stds);

estimate_probe_pos(x, rf_means, rf_stds, att_foc, probe_poss, recruit_win,...
    'r', plot_rf_dist)


