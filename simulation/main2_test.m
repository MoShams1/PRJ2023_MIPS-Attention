


% Mohammad Shams <MoShamsCBR@gmail.com>
% June 2023



clc
clear
close all



% ###############################################

% key model parameters

% receptive field standard deviation
rf_std = 5;
% kernel window
kernel_win = (-60:60);
% shift kernel
recruit_kernel = ...
    [exp(((kernel_win(1) : -1) + 1) * .1) * .5, ...
    0, ...
    exp(-((1 : kernel_win(end)) - 1) * .04)];
% scale kernel
scale_factor = .2;
scale_kernel = ...
    (scale_factor-1) * ...
    [exp(((kernel_win(1) : -1) + 1) * .1) * .5, ...
    0, ...
    exp(-((1 : kernel_win(end)) - 1) * .04)] + 1;

% ###############################################

assert(mod(length(kernel_win),2)==1, ...
    'The size of the modulation window is not an odd integer.')

x = 1:.5:1000;
focus = 500;  % focal point of attention

mod_win = kernel_win + focus;

figure('Units','normalized','OuterPosition',[.5 .1 .25 .8])
% generate RF means
subplot(4,1,1)
plot_flag = true;
rf_means = gen_rf_means(x, mod_win, recruit_kernel, kernel_win, plot_flag);
% generate RF widths
subplot(4,1,2)
plot_flag = true;
rf_stds = gen_rf_stds(x, mod_win, scale_kernel, rf_std, kernel_win, plot_flag);
% generate RF response matrix
subplot(4,1,3)
plot_flag = true;
response_mat = gen_rf_response_mat(x, mod_win, rf_means, rf_stds, focus, plot_flag);
% response_mat = response_mat ./ sum(response_mat,2);
% calculate the illusory shifts
subplot(4,1,4)
plot_flag = true;
test_positions = focus-99:focus+100;
cal_illusory_shift(test_positions, response_mat, focus, kernel_win, plot_flag)
