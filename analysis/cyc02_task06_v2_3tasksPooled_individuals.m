clc
clear
close all

% Specify the path to the JSON file

filename{1} = 'MS01_task06_v2_left_20231030_154843.json';
filename{2} = 'MS01_task06_v2_fair_20231030_135025.json';
filename{3} = 'MS01_task06_v2_right_20231030_153745.json';

for ifile = 1:3

    jsonFilePath = ['../data/cyc02/',filename{ifile}];

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
    err_cell{ifile} = clk_xerr(dir<0);    
    err_cell{ifile+3} = clk_xerr(dir>0);        

end

labels = {'LeftBiased','Fair','RightBiased'};
ntypes = numel(labels);

%% 2D plot
figure('units','normalized','outerposition',[.1 .3 .2 .5])
hold on

alpha = .25;

scatterbar(err_cell(1:3),20,'r')
scatterbar(err_cell(4:6),20,'b')

xlim([.5 ntypes+.5])
xticks(1:ntypes)
xticklabels(labels)
xlabel 'Post-flash motion bias conditions'

ylim([-1 1] * 1.2)
yticks(-2:.25:2)
yline(0)
ylabel 'Horizontal click error (dva)'

text(.75,1,'Post-Flash Rightward Motion','color','b')
text(.75,-1,'Post-Flash Leftward Motion','color','r')
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
