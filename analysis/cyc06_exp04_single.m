clc
clear
close all

% Specify the path to the JSON files

file_dir = dir('../data/cyc06/*exp04*');
nsub = numel(file_dir);

isub = 3;

subj_id = file_dir(isub).name(end-8:end-5);
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
ntrials = length(cell2mat(struct2cell(jsonData.probe2bar_ms)));
bar_dir = cell2mat(struct2cell(jsonData.motion_dir));

probe2bar = cell2mat(struct2cell(jsonData.probe2bar_ms));
probe_start = cell2mat(struct2cell(jsonData.probe_on_ms));

probe_pos = repmat([0,5], ntrials, 1);
click_pos = reshape(cell2mat(struct2cell(jsonData.click_pos)), 2, ntrials)';
click_xpos = click_pos(:,1);
click_xerr = cell2mat(struct2cell(jsonData.click_xerr));
click_xerr(bar_dir == -1) = -click_xerr(bar_dir == -1);

p2b_base = unique(probe2bar)';
p2b_count = 0;
for ip2b = p2b_base
    p2b_count = p2b_count+1;
    ind_p2b = probe2bar == ip2b;
    err_mat(:,p2b_count) = click_xerr(ind_p2b);
end

%% Figure variables
y_limit = [-.5 1.5];
cmap = lines(7);

%% Position shift vs. Bar-Probe distance
figure('units','inches','outerposition',[0, 0, 5, 5])
hold on

x = p2b_base;
y = mean(err_mat);
e = SE(err_mat);
errorbar(x, y, e, ...
    'o-','linewidth',2,'color','k')


xticks(-200:100:300)
xlim([-250 350])
xlabel({'Probe-Bar SOA (ms)'})
xline(0)

yticks(-5:.25:5)
ylim(y_limit)
ylabel({'Position shift (dva)', '(in direction of motion)'})
yline(0)

title(['Subject: ', subj_id])
cleanplot


