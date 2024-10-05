clc
clear
close all

% Specify the path to the JSON files

file_dir = dir('../data/cyc05/*task0_11*');
nsub = numel(file_dir);

isub = 1;

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
ntrials = length(cell2mat(struct2cell(jsonData.bar12soa_ms)));
bar_dir = cell2mat(struct2cell(jsonData.motion_dir));
soa = cell2mat(struct2cell(jsonData.bar12soa_ms));
probe_pos = reshape(cell2mat(struct2cell(jsonData.probe_pos)), 2, ntrials)';
probe_xoffset = probe_pos(:,1);
click_pos = reshape(cell2mat(struct2cell(jsonData.click_pos)), 2, ntrials)';
click_xpos = click_pos(:,1);
click_xerr = cell2mat(struct2cell(jsonData.click_xerr));
click_xerr(bar_dir == -1) = -click_xerr(bar_dir == -1);

cmap = lines(7);

%% Position shift vs. SOA
soa_base = unique(soa)';

soa_count = 0;
for isoa = soa_base
    soa_count = soa_count+1;    
    ind = soa == isoa;    
    err_mat(:,soa_count) = click_xerr(ind);
end

figure('units','inches','outerposition',[0, 0, 5, 5])
x = soa_base(1:end-1);
y = median(err_mat(:,1:end-1));
e = SE(err_mat(:,1:end-1));
errorbar(x, y, e, ...
    'o-','linewidth',2)

% xticks([-200:50:200, 300])
xlim([-450 450])
xlabel 'Bar1-Bar2 SOA (ms)'
xline(0)

yticks(-5:.5:5)
% ylim([-1 1.5])
ylabel 'Position shift in direction of Bar1 motion (dva)'
yline(0)

cleanplot
