clc
clear
close all

% Specify the path to the JSON file

jsonFilePath = '../data/cyc02/YG01_task06_v2_fair_20231116_132330.json';

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
xticks(-5:.2:5)
xlabel 'Horizontal click error (dva)'

yline(0)
yticks(-5:.2:5)
ylabel 'Vertical click error (dva)'

legend([h1 h2 h3 h4],[labels, {'avg Left','avg Right'}],'location','best')

grid on
cleanplot
legend boxon

