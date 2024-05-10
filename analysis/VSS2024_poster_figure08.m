clc
clear
close all

% Specify the path to the JSON files

file_dir = dir('../data/cyc04/*task01*');
% file_dir = dir('../data/cyc04/yes_correct/*task01*');
% file_dir = dir('../data/cyc04/yes_wrong_or_no/*task01*');

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

    % adjust click error sign to make them in the direction of motion
    click_xerr(left_dir) = -click_xerr(left_dir);

    
    %%% indexing
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

    % assign the correct directions to the likely and unlikely categories
    if strcmp(likely_dir, 'right')
        y(isub,:) = [m_rd_rp, m_ld_lp, m_rd_lp, m_ld_rp]; 
    else
        y(isub,:) = [m_ld_lp, m_rd_rp, m_ld_rp, m_rd_lp];        
    end

end

%%%%% plot figures
figure('units','inches','outerposition',[1, 1, 12, 15])

hold on

legend_vec = {'LikelyDir', 'UnlikelyDir', 'LikelyDir', 'UnlikelyDir'};

xticks_vec = 1:4;
xticklabels_vec = legend_vec;
yticks_vec = -2:6;

x = 1:4;

% cmap = lines(7);
c = .6 * ones(4,3);
barplot_colored(x,y,c,.35)
errorbar(...
    x,mean(y),SE(y),...
    'o', ...
    'marker','none', ...    
    'color','k', ...
    'linewidth',2)
scatterbar(mat2cell(y,size(y,1),ones(1,4)))

xticks(xticks_vec)
xticklabels(xticklabels_vec)
xlim([xticks_vec(1)-.5,xticks_vec(end)+.5])

ylabel({'Position offset (dva)', '(in direction of motion)'})
yticks(yticks_vec)
ylim([-2 6.5])
yline(0,'--')

% title 'All'

text(4, -1.75, ['N = ', num2str(nsub)])
text(1.5, -2.75, 'Leading Probe','HorizontalAlignment','center')
text(3.5, -2.75, 'Trailing Probe','HorizontalAlignment','center')

cleanplot

%% stats

[delta, p, W, z, r] = signrank_full(y(:,1),y(:,3));
fprintf('<Likely; Leading Probe vs Trailing Probe> md = %4.1f dva, W = %5d, z = %5.2f, p = %5.3f, r = %4.2f \n', ...
delta,W,z,p,r)

[delta, p, W, z, r] = signrank_full(y(:,2),y(:,4));
fprintf('<Unlikely; Leading Probe vs Trailing Probe> md = %4.1f dva, W = %5d, z = %5.2f, p = %5.3f, r = %4.2f \n', ...
delta,W,z,p,r)

[delta, p, W, z, r] = signrank_full(y(:,1),y(:,2));
fprintf('<Leading Probe; Likely vs Unlikely> md = %4.1f dva, W = %5d, z = %5.2f, p = %5.3f, r = %4.2f \n', ...
delta,W,z,p,r)

[delta, p, W, z, r] = signrank_full(y(:,3),y(:,4));
fprintf('<Trailing Probe; Likely vs Unlikely> md = %4.1f dva, W = %5d, z = %5.2f, p = %5.3f, r = %4.2f \n', ...
delta,W,z,p,r)

%% add stats to figure
lw = 2;

line([1 2],[5.5 5.5],'linewidth',lw,'color','k')
text(1.5, 5.7, '\it n.s.','HorizontalAlignment','center')

line([3 4],[5.5 5.5],'linewidth',lw,'color','k')
text(3.5, 5.7, '\it n.s.','HorizontalAlignment','center')

line([1 3],[6 6],'linewidth',lw,'color','k')
text(2, 6.1, '**','HorizontalAlignment','center','FontSize',14)

line([2 4],[6.5 6.5],'linewidth',lw,'color','k')
text(3, 6.6, '**','HorizontalAlignment','center','FontSize',14)

%% save figure
fontsize(gcf,30,"points")
saveas(gcf, '../result/VSS2024_poster_figure8.pdf')

function scatterbar(A,marksz)
% A: a cell of cetegories

ncat    = numel(A); % number of categories
stdx    = .07; % standard deviation of scatters in each category
linelm  = .3; % line length for median
if nargin < 2
    marksz  = 200; % marker size
end
alpha = .25;
c = .6 * ones(4,3);

hold on
for icat = 1:ncat    
    rng default
    n = numel(A{icat});
    x = randn(n,1)*stdx + icat;
    
    scatter(x,A{icat},marksz,c(icat,:), ...
        'o','markerfacecolor',c(icat,:), ...
        'markeredgecolor','k','markerfacealpha',alpha);
    line([icat-linelm icat+linelm],[nanmedian(A{icat}) nanmedian(A{icat})],...
        'color',c(icat,:),'linewidth',1);
end

xlim([0 ncat+1])
set(gca,'xtick',1:ncat)
end