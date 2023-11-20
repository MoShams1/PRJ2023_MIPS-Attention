clc
clear
close all

% Specify the path to the JSON file

jsonFilePath = '../data/cyc02/MS01_task06_v2_fair_20231030_135025.json';
% jsonFilePath = '../data/cyc02/MS01_task06_v2_right_20231030_153745.json';
% jsonFilePath = '../data/cyc02/MS01_task06_v2_left_20231030_154843.json';

jsonFilePath = '../data/cyc02/HA01_task06_v2_fair_20231031_111134.json';
% jsonFilePath = '../data/cyc02/HA01_task06_v2_left_20231106_122752.json';
% jsonFilePath = '../data/cyc02/HA01_task06_v2_right_20231114_124643.json';

% jsonFilePath = '../data/cyc02/AS01_task06_v2_fair_20231031_113747.json';
% jsonFilePath = '../data/cyc02/AS01_task06_v2_right_20231103_131414.json';
% jsonFilePath = '../data/cyc02/AS01_task06_v2_left_20231110_113546.json';

% jsonFilePath = '../data/cyc02/AB01_task06_v2_fair_20231101_133455.json';
% jsonFilePath = '../data/cyc02/AB01_task06_v2_right_20231101_144331.json';
% jsonFilePath = '../data/cyc02/AB01_task06_v2_left_20231110_121914.json';

% jsonFilePath = '../data/cyc02/MM01_task06_v2_fair_20231101_142041.json';
% jsonFilePath = '../data/cyc02/MM01_task06_v2_left_20231106_135802.json';
% jsonFilePath = '../data/cyc02/MM01_task06_v2_right_20231114_181817.json';

% jsonFilePath = '../data/cyc02/AD01_task06_v2_fair_20231103_110225.json';
% jsonFilePath = '../data/cyc02/AD01_task06_v2_left_20231113_115612.json';

% jsonFilePath = '../data/cyc02/RP01_task06_v2_fair_20231103_113807.json';
% jsonFilePath = '../data/cyc02/RP01_task06_v2_left_20231103_120242.json';
% jsonFilePath = '../data/cyc02/RP01_task06_v2_right_20231110_120848.json';

% jsonFilePath = '../data/cyc02/NP01_task06_v2_fair_20231106_124744.json';
% jsonFilePath = '../data/cyc02/NP01_task06_v2_right_20231108_162439.json';
% jsonFilePath = '../data/cyc02/NP01_task06_v2_left_20231110_141401.json';

% jsonFilePath = '../data/cyc02/NG01_task06_v2_fair_20231108_141326.json';
% jsonFilePath = '../data/cyc02/NG01_task06_v2_right_20231113_145026.json';

% jsonFilePath = '../data/cyc02/NM01_task06_v2_fair_20231110_124127.json';

% jsonFilePath = '../data/cyc02/JK01_task06_v2_fair_20231110_115458.json';

% jsonFilePath = '../data/cyc02/EF01_task06_v2_fair_20231110_152506.json';
% jsonFilePath = '../data/cyc02/EF01_task06_v2_left_20231113_142654.json';
% jsonFilePath = '../data/cyc02/EF01_task06_v2_right_20231114_140427.json';

% jsonFilePath = '../data/cyc02/FM01_task06_v2_right_20231113_131845.json';

% jsonFilePath = '../data/cyc02/OS01_task06_v2_fair_20231114_180802.json';

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

