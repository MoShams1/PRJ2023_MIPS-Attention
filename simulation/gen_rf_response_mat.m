


% Mohammad Shams <MoShamsCBR@gmail.com>
% June 2023
%
% Generates a matrix of [spatial unit response] x [x positions]
% Each unit is modeled with a Gaussian.
% Each row contains the unit's response across all x positions.

function response_mat = gen_rf_response_mat(x, rf_means, rf_stds, focus, show_win, plot_flag)

color = [.6 .6 .6];

% generate response of each spatial unit (receptive field)
i_rf = 0;
for irf = rf_means
    i_rf = i_rf+1;
    mu = rf_means(i_rf);
    sigma = rf_stds(i_rf);
    response_mat(i_rf,:) = gaussmf(x,[sigma mu]);
end

if plot_flag
    plot(x-focus,response_mat','color',color)
    xlabel 'Positions wrt focus of att.'
    ylabel 'Unit response'    
    xlim(show_win)
end