clc
clear
close all

% Specify the path to the JSON files

file_dir = dir('../data/cyc05/*task0_2*');
nsub = numel(file_dir);

isub = 1;

% Specify the path to the JSON file
jsonFilePath = fullfile(file_dir(isub).folder,file_dir(isub).name);

% Open the JSON file and read its content
fileID = fopen(jsonFilePath);
jsonContent = fread(fileID, '*char')';
fclose(fileID);

% Parse the JSON content
jsonData = jsondecode(jsonContent);


%%% convert structure to arrays
ntrials = length(cell2mat(struct2cell(jsonData.soa_ms)));
bar_dir = cell2mat(struct2cell(jsonData.motion_dir));
soa = cell2mat(struct2cell(jsonData.soa_ms));
probe_pos = reshape(cell2mat(struct2cell(jsonData.probe_pos)), 2, ntrials)';
probe_xoffset = probe_pos(:,1);
click_pos = reshape(cell2mat(struct2cell(jsonData.click_pos)), 2, ntrials)';
click_xpos = click_pos(:,1);
click_xerr = cell2mat(struct2cell(jsonData.click_xerr));
click_xerr(bar_dir == -1) = -click_xerr(bar_dir == -1);


%% Position shift vs. SOA across three probe2bar values
soa_base = unique(soa)';

soa_count = 0;
for isoa = soa_base
    soa_count = soa_count+1;    
    ind = soa == isoa;
    err_mat(:,soa_count) = click_xerr(ind);
end

figure('units','inches','outerposition',[0, 0, 5, 5])
x = soa_base;
y = median(err_mat);
e = SE(err_mat);
errorbar(x, y, e, ...
    'linewidth',2)
xlabel 'Bar-Flash SOA (ms)'
ylabel 'Position shift in direction of motion (dva)'
yline(0)
cleanplot

% %% prepare data for figures
% right_dir = bar_dir == 1;
% left_dir = bar_dir == -1;
% right_probe = probe_pos == 2.5;
% left_probe = probe_pos == -2.5;
% 
% ind = right_dir & right_probe;
% m_rd_rp = abs(median(click_xerr(ind)));
% e_rd_rp = SE(click_xerr(ind));
% 
% ind = right_dir & left_probe;
% m_rd_lp = abs(median(click_xerr(ind)));
% e_rd_lp = SE(click_xerr(ind));
% 
% ind = left_dir & right_probe;
% m_ld_rp = abs(median(click_xerr(ind)));
% e_ld_rp = SE(click_xerr(ind));
% 
% ind = left_dir & left_probe;
% m_ld_lp = abs(median(click_xerr(ind)));
% e_ld_lp = SE(click_xerr(ind));
% 
% %%%% plot figures
% figure('units','inches','outerposition',[7, 4, 9, 4])
% 
% %% figure 01-A
% subplot(1,3,1)
% hold on
% 
% legend_vec = {'LeftD-LeftP', 'LeftD-RightP', 'RightD-LeftP', 'RightD-RightP'};
% 
% click_sz = 20;
% probe_sz = 50;
% colors = lines(7);
% cmap = [colors(7,:);colors(2,:); colors(6,:); colors(1,:)];
% alpha = .6;
% 
% ind = left_dir & left_probe;
% scatter(click_pos(ind,1),click_pos(ind,2),click_sz,cmap(1,:),'<','filled','markerfacealpha',alpha)
% ind = left_dir & right_probe;
% scatter(click_pos(ind,1),click_pos(ind,2),click_sz,cmap(2,:),'<','filled','markerfacealpha',alpha)
% ind = right_dir & left_probe;
% scatter(click_pos(ind,1),click_pos(ind,2),click_sz,cmap(3,:),'>','filled','markerfacealpha',alpha)
% ind = right_dir & right_probe;
% scatter(click_pos(ind,1),click_pos(ind,2),click_sz,cmap(4,:),'>','filled','markerfacealpha',alpha)
% 
% scatter(0, -2, probe_sz, '+k')
% scatter(-2.5, 4, probe_sz, 'ok', 'fill')
% scatter(2.5, 4, probe_sz, 'ok', 'fill')
% 
% xlabel 'Horizontal distance (dva)'
% xlim([-10 10])
% 
% ylabel 'Vertical distance (dva)'
% ylim([-3 8])
% 
% text(-9, .7, legend_vec(1), 'color',cmap(1,:))
% text(-9, 0, legend_vec(2), 'color',cmap(2,:))
% text(-9, -.7, legend_vec(3), 'color',cmap(3,:))
% text(-9, -1.4, legend_vec(4), 'color',cmap(4,:))
% 
% cleanplot
% 
% %% figure 01-B
% subplot(1,3,2)
% hold on
% 
% cerr = 'k';
% cbar = .6 * ones(1,3);
% lw = 1.5;
% xticks_vec = 1:4;
% xticklabels_vec = legend_vec;
% yticks_vec = 0:3;
% 
% x = 1:4;
% y = [m_ld_lp, m_ld_rp, m_rd_lp, m_rd_rp];
% err = [e_ld_lp, e_ld_rp, e_rd_lp, e_rd_rp];
% 
% barplot_colored(x,y,cmap,.35)
% errorbar(...
%     x,y,err,...
%     'o', ...
%     'marker','none', ...    
%     'color',cerr, ...
%     'linewidth',lw)
% 
% xticks(xticks_vec)
% xticklabels(xticklabels_vec)
% xlim([xticks_vec(1)-.5,xticks_vec(end)+.5])
% 
% ylabel 'Absolute perceived shift (dva)'
% yticks(yticks_vec)
% ylim([0 3])
% 
% cleanplot
% 
% 
% %% figure 01-C
% subplot(1,3,3)
% hold on
% 
% legend_vec = {'LikelyD-LeadP', 'UnlikelyD-LeadP', 'UnlikelyD-TrailP', 'LikelyD-TrailP'};
% 
% cerr = 'k';
% cbar = .6 * ones(1,3);
% lw = 1.5;
% xticks_vec = 1:4;
% xticklabels_vec = legend_vec;
% yticks_vec = 0:3;
% cmap_relative = .5*ones(4,3);
% 
% x = 1:4;
% 
% if strcmp(likely_dir, 'left')
%     y = [m_ld_lp, m_rd_rp, m_rd_lp, m_ld_rp];
%     err = [e_ld_lp, e_rd_rp, e_rd_lp, e_ld_rp];
% else
%     y = [m_rd_rp, m_ld_lp, m_ld_rp, m_rd_lp];
%     err = [e_rd_rp, e_ld_lp, e_ld_rp, e_rd_lp];
% end
% 
% barplot_colored(x,y,cmap_relative,.35)
% errorbar(...
%     x,y,err,...
%     'o', ...
%     'marker','none', ...    
%     'color',cerr, ...
%     'linewidth',lw)
% 
% xticks(xticks_vec)
% xticklabels(xticklabels_vec)
% xlim([xticks_vec(1)-.5,xticks_vec(end)+.5])
% 
% ylabel 'Absolute perceived shift (dva)'
% yticks(yticks_vec)
% ylim([0 3])
% 
% cleanplot
% 
% sgtitle(['Likely direction: ',likely_dir], 'fontsize',11)