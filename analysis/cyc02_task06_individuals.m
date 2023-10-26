clc
clear
% close all

% Specify the path to the JSON file

jsonFilePath = '../data/cyc02/MS01_task06_20231026_153748.json';


% Open the JSON file and read its content
fileID = fopen(jsonFilePath);
jsonContent = fread(fileID, '*char')';
fclose(fileID);

% Parse the JSON content
jsonData = jsondecode(jsonContent);

% convert structure to arrays
dir1 = cell2mat(struct2cell(jsonData.preflash_dir));
dir2 = struct2cell(jsonData.postflash_dir);
clk_xerr = cell2mat(struct2cell(jsonData.click_xerr));
clk_yerr = cell2mat(struct2cell(jsonData.click_yerr));

% create data cell
ind_v = strcmp(dir2, 'v');
ind_h = strcmp(dir2, 'h');
err_cell{1} = clk_xerr(ind_v & dir1>0);
err_cell{2} = clk_xerr(ind_h & dir1>0);
err_cell{3} = clk_xerr(ind_v & dir1<0);
err_cell{4} = clk_xerr(ind_h & dir1<0);
err_cell{5} = clk_yerr(ind_v & dir1>0);
err_cell{6} = clk_yerr(ind_h & dir1>0);
err_cell{7} = clk_yerr(ind_v & dir1<0);
err_cell{8} = clk_yerr(ind_h & dir1<0);

err_mat = cell2mat(err_cell);

labels = {'RU','RR','LU','LL'};
ntypes = numel(labels);

%% 2D plot
figure('units','normalized','outerposition',[.1 .3 .3 .5])
hold on

alpha = .5;

h1 = scatter(err_mat(:,1),err_mat(:,5),'b','o','fill','markerfacealpha',alpha);
h2 = scatter(err_mat(:,2),err_mat(:,6),'b','o');
h3 = scatter(err_mat(:,3),err_mat(:,7),'r','o','fill','markerfacealpha',alpha);
h4 = scatter(err_mat(:,4),err_mat(:,8),'r','o');

xline(0)
xlim([-1 1] * 1.2)
xticks(-1:.25:1)
xlabel 'Horizontal click error (dva)'

yline(0)
ylim([-1 1] * 1.2)
yticks(-1:.25:1)
ylabel 'Vertical click error (dva)'

legend([h1 h2 h3 h4],labels)

cleanplot

%% scatterbar plot
figure('units','normalized','outerposition',[.4 .3 .25 .5])
hold on

scatterbar(err_cell([1,2,5,6]), 30, 'b');
scatterbar(err_cell([3,4,7,8]), 30, 'r');

xlim([.5 ntypes+.5])
xticks(1:ntypes)
xticklabels({'Vx','Hx','Vy','Hy'})
xlabel 'Direction conditions'

ylim([-1 1] * 1.2)
yticks(-1:.25:1)
yline(0)
ylabel 'Click error (dva)'

title 'Raw data'

text(1,1.2,'Pre-Flash Rightward Motion','color','b')
text(1,1.1,'Pre-Flash Leftward Motion','color','r')
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
