% clc
clear
% close all

% Specify the path to the JSON files

file_dir = dir('../data/cyc04/*task01*');

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
    
    % adjust each single click error sign as if the likely direction for
    % everyone was 'right'
    if strcmp(likely_dir,'left')
        click_xerr = -click_xerr;
    end
    
    %%% prepare data for figures
    right_dir = bar_dir == 1;
    left_dir = bar_dir == -1;
    right_probe = probe_pos == 2.5;
    left_probe = probe_pos == -2.5;


    ind = right_dir & right_probe;
    m_rd_rp = median(click_xerr(ind));
    e_rd_rp = SE(click_xerr(ind));
    
    ind = right_dir & left_probe;
    m_rd_lp = median(click_xerr(ind));
    e_rd_lp = SE(click_xerr(ind));
    
    ind = left_dir & right_probe;
    m_ld_rp = median(click_xerr(ind));
    e_ld_rp = SE(click_xerr(ind));
    
    ind = left_dir & left_probe;
    m_ld_lp = median(click_xerr(ind));
    e_ld_lp = SE(click_xerr(ind));

    % flip the sign of the 
    if strcmp(likely_dir, 'left')
        y(isub,:) = [m_ld_lp, -m_rd_rp, m_ld_rp, -m_rd_lp];        
    else
        y(isub,:) = [m_rd_rp, -m_ld_lp, m_rd_lp, -m_ld_rp];        
    end

end

%%%%% plot figures
figure('units','inches','outerposition',[7, 4, 3.5, 5])

hold on

legend_vec = {'LikelyDir', 'UnlikelyDir', 'UnlikelyDir', 'LikelyDir'};

xticks_vec = 1:4;
xticklabels_vec = legend_vec;
yticks_vec = -2:6;

x = 1:4;

scatterbar(mat2cell(y,24,ones(1,4)))

xticks(xticks_vec)
xticklabels(xticklabels_vec)
xlim([xticks_vec(1)-.5,xticks_vec(end)+.5])

ylabel 'Absolute perceived shift (dva)'
yticks(yticks_vec)
% ylim([-2.5 6])

yline(0,'--')

title 'All'

text(4, -2.25, ['N = ', num2str(nsub)])
text(1.5, -3.3, 'Leading Probe','HorizontalAlignment','center')
text(3.5, -3.3, 'Trailing Probe','HorizontalAlignment','center')

cleanplot
