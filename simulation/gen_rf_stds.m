


% Mohammad Shams <MoShamsCBR@gmail.com>
% June 2023
%
% Scales the receptive fields' width by applying a kernel within a modulation
% window

function rf_stds = gen_rf_stds(x, mod_win, kernel, rf_std, kernel_win, show_win, plot_flag)
rf_means = x;

rf_stds = rf_std .* ones(1,length(rf_means));
rf_stds(mod_win) = rf_stds(mod_win) .* kernel;

if plot_flag
    plot(kernel_win, kernel, '-ok')
    xlabel 'Positions wrt focus of att.'
    ylabel 'Rescale coeff.'
    xlim(show_win)
end
