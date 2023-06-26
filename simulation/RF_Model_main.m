


% Mohammad Shams <MoShamsCBR@gmail.com>
% June 2023
%
% A receptive-field based model to explain attention-induced position shifts



clc
clear
close all


% ###############################################

% Model parameters

% receptive field standard deviation
rf_std = 2;

% maximum scaling factor (e.g., 1 means no change; .5 shrink 50%; 1.5
% expand 50%
max_scale_factor = .4;

% kernel half-width
khw = 30;

% balance index (e.g., 1 means fully balanced and 0.5 means one side is
% half size of the other side.
bal_index = 1;

% ###############################################

amp1 = bal_index;
x_coeff1 = .2;
x_off1 = 1;
rk1 = gen_half_exp((-khw:-1), x_off1, x_coeff1, amp1);

amp2 = 1;
x_coeff2 = -x_coeff1;
x_off2 = -x_off1;
rk2 = gen_half_exp((1:khw), x_off2, x_coeff2, amp2);

% shift kernel
recruit_kernel = [rk1, 0, rk2];

% scale kernel
scale_kernel = (max_scale_factor-1) * [rk1, 0, rk2] + 1;

% kernel window
kernel_win = (-khw:khw);

x = 1:1:1000;
focus = 500;  % focal point of attention

mod_win = kernel_win + focus;

figure('Units','normalized','OuterPosition',[.5 .1 .4 .8])
show_win = [-50 50];
% generate RF means
subplot(4,1,1)
plot_flag = true;
rf_means = gen_rf_means(x, mod_win, recruit_kernel, kernel_win, show_win, plot_flag);
% generate RF widths
subplot(4,1,2)
plot_flag = true;
rf_stds = gen_rf_stds(x, mod_win, scale_kernel, rf_std, kernel_win, show_win, plot_flag);
% generate RF response matrix
subplot(4,1,3)
plot_flag = true;
response_mat = gen_rf_response_mat(x, rf_means, rf_stds, focus, show_win, plot_flag);
% calculate the illusory shifts
subplot(4,1,4)
plot_flag = true;
test_positions = focus-99:focus+100;
cal_illusory_shift(test_positions, response_mat, focus, show_win, plot_flag)
