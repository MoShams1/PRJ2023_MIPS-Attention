


% Mohammad Shams <MoShamsCBR@gmail.com>
% June 2023
%
% Calculates the illusory shift emerged from modulated receptive fields

function cal_illusory_shift(test_positions, response_mat, focus, show_win, plot_flag)

pos_cntr = 0;
for probe_pos = test_positions
    pos_cntr = pos_cntr+1;
    % population response to a flash at probe_pos
    probe_response = response_mat(:,probe_pos)';
    % probe position estimated by the population
    x_positions = 1:size(response_mat,2);
    ill_pos = sum(x_positions .* probe_response) / sum(probe_response);
    % illusory mislocalization of the probe
    shifts(pos_cntr) = ill_pos-probe_pos;
end

if plot_flag
    colors = lines(7);
    color = colors(7,:);
    plot(test_positions-focus, shifts, 'color',color,'LineWidth',1.5)
    line(show_win, [0 0], 'color','k', 'linestyle','--')
    xlabel 'Probe position wrt focus of att.'
    ylabel 'Illusory shift'
    xlim(show_win)
    y_lim = ylim;
    ylim(y_lim)
    line([0 0], y_lim,'color','k','linestyle','--')
end