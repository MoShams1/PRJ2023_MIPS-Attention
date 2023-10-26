clc
clear
close all

% Specify the path to the JSON file

jsonFilePath = '../data/cyc02/MS01_task06_20231026_141402.json';


% Open the JSON file and read its content
fileID = fopen(jsonFilePath);
jsonContent = fread(fileID, '*char')';
fclose(fileID);

% Parse the JSON content
jsonData = jsondecode(jsonContent);

% convert structure to arrays
dir1 = cell2mat(struct2cell(jsonData.preflash_dir));
dir2 = struct2cell(jsonData.postflash_dir);
pos = cell2mat(struct2cell(jsonData.probe_pos));
clk = cell2mat(struct2cell(jsonData.click_pos));
errx(:,1) = clk(1:40)-0;
erry(:,1) = clk(41:80)-1;

% create data cell
ind_v = strcmp(dir2, 'v');
ind_h = strcmp(dir2, 'h');
err_cell{1} = errx(ind_v & dir1>0);
err_cell{2} = errx(ind_h & dir1>0);
err_cell{3} = errx(ind_v & dir1<0);
err_cell{4} = errx(ind_h & dir1<0);
err_cell{5} = erry(ind_v & dir1>0);
err_cell{6} = erry(ind_h & dir1>0);
err_cell{7} = erry(ind_v & dir1<0);
err_cell{8} = erry(ind_h & dir1<0);

err_mat = cell2mat(err_cell);

%% plot

figure('units','normalized','outerposition',[.2 .3 .25 .5])
hold on

% typ_list = {'FG', 'FG-Edge', 'BB-LE', 'WB-RE', 'FE-LE', 'FE-RE'};

scatterbar(err_cell([1,2,5,6]), 30, 'b');
scatterbar(err_cell([3,4,7,8]), 30, 'r');

% xticklabels(typ_list)
% xlim([.5 ntypes+.5])
% xticks(1:ntypes)
% xlabel 'Annulus types'
% 
% ylim([-1.1 1.1] * 1.2)
% yticks(-1:.25:1)
yline(0)
% ylabel 'Point of subjective equality'
% 
% title 'Raw data'
% 
% text(1,1.2,'Post-Flash Rightward Motion','color','b')
% text(1,1.1,'Post-Flash Leftward Motion','color','r')
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
