clc
clear
close all

% Specify the path to the JSON file

% jsonFilePath = '../data/cyc02/MS01_task06_v2_fair_20231030_135025.json';  % fair
% jsonFilePath = '../data/cyc02/MS01_task06_v2_right_20231030_153745.json';  % right biased
% jsonFilePath = '../data/cyc02/MS01_task06_v2_left_20231030_154843.json';  % left biased

% jsonFilePath = '../data/cyc02/HA01_task06_v2_fair_20231031_111134.json';  % fair

% jsonFilePath = '../data/cyc02/AS01_task06_v2_fair_20231031_113747.json';  % fair

% jsonFilePath = '../data/cyc02/AB01_task06_v2_fair_20231101_133455.json';  % fair
jsonFilePath = '../data/cyc02/AB01_task06_v2_right_20231101_144331.json';  % right

% jsonFilePath = '../data/cyc02/MM01_task06_v2_fair_20231101_141135.json';  % fair
% jsonFilePath = '../data/cyc02/MM01_task06_v2_fair_20231101_142041.json';  % fair



% Open the JSON file and read its content
fileID = fopen(jsonFilePath);
jsonContent = fread(fileID, '*char')';
fclose(fileID);

% Parse the JSON content
jsonData = jsondecode(jsonContent);

% convert structure to arrays
dir = cell2mat(struct2cell(jsonData.postflash_dir));
clk_xerr = cell2mat(struct2cell(jsonData.click_xerr));
clk_yerr = cell2mat(struct2cell(jsonData.click_yerr));

% create data cell
err_cell{1} = clk_xerr(dir<0);
err_cell{2} = clk_yerr(dir<0);
err_cell{3} = clk_xerr(dir>0);
err_cell{4} = clk_yerr(dir>0);

% err_mat = cell2mat(err_cell);

labels = {'Left','Right'};
ntypes = numel(labels);

%% 2D plot
figure('units','normalized','outerposition',[.1 .3 .3 .5])
hold on

alpha = .25;

h1 = scatter(err_cell{:,1},err_cell{:,2},'r','<','fill','markerfacealpha',alpha);
h2 = scatter(err_cell{:,3},err_cell{:,4},'b','>','fill','markerfacealpha',alpha);

h3 = scatter(mean(err_cell{:,1}),mean(err_cell{:,2}),'r','o','fill');
h4 = scatter(mean(err_cell{:,3}),mean(err_cell{:,4}),'b','o','fill');

xline(0)
% xlim([-1 1] * 1.75)
xticks(-5:.2:5)
xlabel 'Horizontal click error (dva)'

yline(0)
% ylim([-1 1] * 1.75)
yticks(-5:.2:5)
ylabel 'Vertical click error (dva)'

legend([h1 h2 h3 h4],[labels, {'avg Left','avg Right'}])

grid on
cleanplot

%%
function scatterbar(A,marksz,color)
% A: a cell of cetegories

ncat    = numel(A); % number of categories
stdx    = .05; % standard deviation of scatters in each category
linelm  = .3; % line length for median
alpha = .3;

hold on
for icat = 1:ncat    
    rng default
    n = numel(A{icat});
    x = randn(n,1)*stdx + icat;
    
    scatter(x,A{icat},marksz,color,'o','fill','markerfacealpha',alpha);
    line([icat-linelm icat+linelm],[nanmedian(A{icat}) nanmedian(A{icat})],...
        'color',color,'linewidth',2);
end

xlim([0 ncat+1])
set(gca,'xtick',1:ncat)
end
