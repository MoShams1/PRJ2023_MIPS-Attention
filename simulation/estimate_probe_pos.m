
function estimate_probe_pos(x, rf_centers, rf_stds, att_foc, probe_poss, recruit_win, ...
    color, plot_rf_dist)

mksz = 10;

% RF distribution in the absence of attention
rf_cntr = 0;
for irf = rf_centers
    rf_cntr = rf_cntr+1;
    y_mat(rf_cntr,:) = gaussmf(x,[rf_stds(rf_cntr), rf_centers(rf_cntr)]);
end

% y_mat = y_mat./sum(y_mat,2);

subplot(4,1,3)
if plot_rf_dist
    col_gray = [.6 .6 .6];
    plot(x,y_mat','color',col_gray)
end
xlabel 'x positions'
ylabel 'Unit response'
xlim([recruit_win(1) recruit_win(end)] + att_foc)
pbaspect([1 .25 1])

pos_cntr = 0;
for probe_pos = probe_poss
    pos_cntr = pos_cntr+1;
    y = y_mat(:,probe_pos)';  % population response to a flash at probe_pos
    ill_pos = sum(rf_centers.*y)/sum(y);  % probe position estimate by the population
    shifts(pos_cntr) = ill_pos-probe_pos;  % illusory mislocalization of the probe
    
    subplot(4,1,3)
    hold on
    if length(probe_poss)<=1, plot_ind=1; else plot_ind=2; end
    if plot_ind==1
        if plot_rf_dist
            col_gray = [.6 .6 .6];
            plot(x,y_mat','color',col_gray)
        end
        plot(att_foc,0.02, ...
                'v','markerfacecolor','none','markeredgecolor',color,'markersize',mksz)
        plot(x,y,'color',color,'linewidth',1);
        xlabel Space
        ylabel Response
        xlim([recruit_win(1) recruit_win(end)]+att_foc)
        pbaspect([1 .25 1])
        subplot(4,1,4)
        pbaspect([1 .25 1])
    end
end
subplot(4,1,4)
if plot_ind==2
    plot(probe_poss-att_foc-0,shifts,'color',color,'LineWidth',1)
    line([recruit_win(1) recruit_win(end)], [0 0], 'color','k', 'linestyle','--')
    xlabel 'Probe position wrt focus of attention'
    ylabel 'Illusory shift'
    xlim([recruit_win(1) recruit_win(end)])
    pbaspect([1 .25 1])
    y_lim = ylim;
    ylim([y_lim])
    line([0 0], y_lim,'color','k','linestyle','--')
end
