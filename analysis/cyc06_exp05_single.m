clc
clear
close all

% Specify the path to the JSON files

file_dir = dir('../data/cyc06/*exp05*');
nsub = numel(file_dir);

isub = 1;

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
% bar_dir = cell2mat(struct2cell(jsonData.motion_dir));

cue_cnd = cell2mat(struct2cell(jsonData.cue_condition));
dis_cnd = cell2mat(struct2cell(jsonData.dis_condition));

% probe_pos = repmat([0,5], ntrials, 1);
% click_pos = reshape(cell2mat(struct2cell(jsonData.click_pos)), 2, ntrials)';
% click_xpos = click_pos(:,1);
position_shift = cell2mat(struct2cell(jsonData.position_shift_norm));
% click_xerr(bar_dir == -1) = -click_xerr(bar_dir == -1);

% p2b_base = unique(probe2bar)';
% p2b_count = 0;
% for ip2b = p2b_base
%     p2b_count = p2b_count+1;
%     ind_p2b = probe2bar == ip2b;
%     err_mat(:,p2b_count) = click_xerr(ind_p2b);
% end

%% Figure variables
% y_limit = [-.5 1.5];
cmap = lines(7);

%% Position shift (Uncued vs. Cued)
figure('units','inches','outerposition',[0, 0, 5, 5])
hold on

x = 1:4;
y = [
    mean(position_shift(dis_cnd == 0 & cue_cnd == 0))
    mean(position_shift(dis_cnd == 0 & cue_cnd == 1))
    mean(position_shift(dis_cnd == 1 & cue_cnd == 0))
    mean(position_shift(dis_cnd == 1 & cue_cnd == 1))
    ];
e = [
    SE(position_shift(dis_cnd == 0 & cue_cnd == 0))
    SE(position_shift(dis_cnd == 0 & cue_cnd == 1))
    SE(position_shift(dis_cnd == 1 & cue_cnd == 0))
    SE(position_shift(dis_cnd == 1 & cue_cnd == 1))
    ];
errorbar(x, y, e, ...
    'o','linewidth',2,'color','k')
cleanplot

xticks(1:4)
xlim([.5 4.5])
xticklabels({'1Bar-Uncued', '1Bar-Cued', '4Bar-Uncued', '4Bar-Cued'})
xline(0)

yticks(-5:.1:5)
% ylim(y_limit)
ylabel({'Position shift (dva)', '(in direction of motion)'})
% yline(0)

title(['Subject: ', subj_id])
cleanplot


