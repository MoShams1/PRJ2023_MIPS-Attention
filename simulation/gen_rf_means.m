


% Mohammad Shams <MoShamsCBR@gmail.com>
% June 2023
%
% Shifts the receptive fields by applying a kernel within a modulation
% window

function rf_means = gen_rf_means(x, mod_win, kernel, kernel_win, show_win, plot_flag)
rf_means = x;

probe2focus = kernel_win;
shift = probe2focus .* -kernel;

rf_means(mod_win) = rf_means(mod_win) + shift;

if plot_flag
    plot(kernel_win, kernel, '-ok')
    xlabel 'Positions wrt focus of att.'
    ylabel 'Rcruitment index'
    xlim(show_win)
end