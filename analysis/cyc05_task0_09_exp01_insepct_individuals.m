clc
clear
close all

% Specify the path to the JSON files

file_dir = dir('../data/cyc05/*task0_09*');
nsub = numel(file_dir);

isub = 2;

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
distance = cell2mat(struct2cell(jsonData.probe2bar_dva));
probe_pos = reshape(cell2mat(struct2cell(jsonData.probe_pos)), 2, ntrials)';
probe_xoffset = probe_pos(:,1);
click_pos = reshape(cell2mat(struct2cell(jsonData.click_pos)), 2, ntrials)';
click_xpos = click_pos(:,1);
click_xerr = cell2mat(struct2cell(jsonData.click_xerr));
click_xerr(bar_dir == -1) = -click_xerr(bar_dir == -1);

cmap = lines(7);

%% Position shift vs. Bar-Probe distance
distance_base = unique(distance)';

distance_count = 0;
for idistance = distance_base
    distance_count = distance_count+1;    
    ind = distance == idistance;    
    err_mat(:,distance_count) = click_xerr(ind);
end

figure('units','inches','outerposition',[0, 0, 5, 5])
x = distance_base;
y = mean(err_mat);
e = SE(err_mat);
errorbar(x, y, e, ...
    'o-','linewidth',2)

% xticks(-4:.5:4)
xlim([-4.5 4.5])
xlabel 'Probe-Bar distance (dva)'
xline(0)

% yticks(-5:.5:5)
% ylim([-1 1.5])
ylabel 'Position shift in direction of Bar motion (dva)'
yline(0)

cleanplot
