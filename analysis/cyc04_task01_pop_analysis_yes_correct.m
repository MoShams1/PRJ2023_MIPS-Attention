% clc
% clear
% close all

% Specify the path to the JSON files

file_dir = dir('../data/cyc04/yes_correct/*task01*');

nsub = numel(file_dir);

for isub = 1:nsub

    % Specify the path to the JSON file
    jsonFilePath = fullfile(file_dir(isub).folder,file_dir(isub).name);
    
    % Open the JSON file and read its content
    fileID = fopen(jsonFilePath);
    jsonContent = fread(fileID, '*char')';
    fclose(fileID);
    
    % Parse the JSON content
    jsonData = jsondecode(jsonContent);
    
    
    %%% convert structure to arrays
    likely_dir = jsonData.likely_dir.x0;
    bar_dir = cell2mat(struct2cell(jsonData.bar_dir));
    probe_pos = reshape(cell2mat(struct2cell(jsonData.probe_pos)), 2, length(bar_dir))';
    click_pos = reshape(cell2mat(struct2cell(jsonData.click_pos)), 2, length(bar_dir))';
    click_xpos = click_pos(:,1);
    click_xerr = cell2mat(struct2cell(jsonData.click_xerr));
    
    
    %%% prepare data for figures
    right_dir = bar_dir == 1;
    left_dir = bar_dir == -1;
    right_probe = probe_pos == 2.5;
    left_probe = probe_pos == -2.5;
    
    ind = right_dir & right_probe;
    m_rd_rp = abs(median(click_xerr(ind)));
    e_rd_rp = SE(click_xerr(ind));
    
    ind = right_dir & left_probe;
    m_rd_lp = abs(median(click_xerr(ind)));
    e_rd_lp = SE(click_xerr(ind));
    
    ind = left_dir & right_probe;
    m_ld_rp = abs(median(click_xerr(ind)));
    e_ld_rp = SE(click_xerr(ind));
    
    ind = left_dir & left_probe;
    m_ld_lp = abs(median(click_xerr(ind)));
    e_ld_lp = SE(click_xerr(ind));

    % ------

    if strcmp(likely_dir, 'left')
        y(isub,:) = [m_ld_lp, m_rd_rp, m_rd_lp, m_ld_rp];        
    else
        y(isub,:) = [m_rd_rp, m_ld_lp, m_ld_rp, m_rd_lp];        
    end

end

%%%%% plot figures
% figure('units','inches','outerposition',[7, 4, 4, 4])

hold on

legend_vec = {'LikelyD-LeadP', 'UnlikelyD-LeadP', 'UnlikelyD-TrailP', 'LikelyD-TrailP'};

cerr = 'k';
cbar = .6 * ones(1,3);
lw = 1.5;
xticks_vec = 1:4;
xticklabels_vec = legend_vec;
yticks_vec = 0:3;
cmap_relative = .5*ones(4,3);

x = 1:4;

barplot_colored(x,mean(y),cmap_relative,.35)
errorbar(...
    x,mean(y),SE(y),...
    'o', ...
    'marker','none', ...    
    'color',cerr, ...
    'linewidth',lw)

xticks(xticks_vec)
xticklabels(xticklabels_vec)
xlim([xticks_vec(1)-.5,xticks_vec(end)+.5])

ylabel 'Absolute perceived shift (dva)'
yticks(yticks_vec)
ylim([-.5 3])

title 'Biased perceived correctly'

text(4, -.25, ['N = ', num2str(nsub)])

cleanplot
