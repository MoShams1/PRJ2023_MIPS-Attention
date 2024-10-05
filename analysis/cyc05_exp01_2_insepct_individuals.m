clc
clear
% close all

% Specify the path to the JSON files

file_dir = dir('../data/cyc05/*exp01*');
nsub = numel(file_dir);

isub = 2;

disp(['Subject: ', file_dir(isub).name(end-8:end-5)])

% Specify the path to the JSON file
jsonFilePath = fullfile(file_dir(isub).folder,file_dir(isub).name);

% Open the JSON file and read its content
fileID = fopen(jsonFilePath);
jsonContent = fread(fileID, '*char')';
fclose(fileID);

% Parse the JSON content
jsonData = jsondecode(jsonContent);


%%% convert structure to arrays
ntrials = length(cell2mat(struct2cell(jsonData.probe2bar_dva)));
bar_dir = cell2mat(struct2cell(jsonData.motion_dir));

probe2bar = cell2mat(struct2cell(jsonData.probe2bar_dva));
% xoffset = cell2mat(struct2cell(jsonData.bar_xoffset));
probe_pos = reshape(cell2mat(struct2cell(jsonData.probe_pos)), 2, ntrials)';

click_pos = reshape(cell2mat(struct2cell(jsonData.click_pos)), 2, ntrials)';
click_xpos = click_pos(:,1);
click_xerr = cell2mat(struct2cell(jsonData.click_xerr));
click_xerr(bar_dir == -1) = -click_xerr(bar_dir == -1);

cmap = lines(7);

%% Position shift vs. Bar-Probe distance
p2b_base = unique(probe2bar)';

p2b_count = 0;
for ip2b = p2b_base
    p2b_count = p2b_count+1;    
    ind = probe2bar == ip2b;    
    err_mat(:,p2b_count) = click_xerr(ind);
end

figure('units','inches','outerposition',[0, 0, 5, 5])
x = p2b_base;
y = median(err_mat);
e = SE(err_mat);
errorbar(x, y, e, ...
    'o-','linewidth',2)

xticks(-4:1:4)
xlim([-4.5 4.5])
xlabel({'Probe-Bar distance (dva)', '(in direction of motion)'})
xline(0)

yticks(-5:.25:5)
% ylim([-.2 1.2])
ylabel({'Position shift (dva)', '(in direction of motion)'})
yline(0)

cleanplot
