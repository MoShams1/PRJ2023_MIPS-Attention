clc
clear
% close all

% Specify the path to the JSON files

file_dir = dir('../data/cyc06/*exp05*');
file_dir(12) = [];
nsub = numel(file_dir);

for isub = 1:nsub

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
    cue_cnd = cell2mat(struct2cell(jsonData.cue_condition));
    dis_cnd = cell2mat(struct2cell(jsonData.dis_condition));
    position_shift_single = cell2mat(struct2cell(jsonData.position_shift_norm));

    position_shift(isub, 1) = mean(position_shift_single(dis_cnd == 0 & cue_cnd == 0));
    position_shift(isub, 2) = mean(position_shift_single(dis_cnd == 0 & cue_cnd == 1));
    position_shift(isub, 3) = mean(position_shift_single(dis_cnd == 1 & cue_cnd == 0));
    position_shift(isub, 4) = mean(position_shift_single(dis_cnd == 1 & cue_cnd == 1));

    variability(isub,1) = std(position_shift_single(dis_cnd == 0 & cue_cnd == 0));
    variability(isub,2) = std(position_shift_single(dis_cnd == 0 & cue_cnd == 1));
    variability(isub,3) = std(position_shift_single(dis_cnd == 1 & cue_cnd == 0));
    variability(isub,4) = std(position_shift_single(dis_cnd == 1 & cue_cnd == 1));

end

%% Figure variables
y_limit = [1.2 2.2];
cmap = lines(7);

%% Position shift vs. Bar-Probe distance (average)
figure('units','inches','outerposition',[0, 0, 5, 5])
hold on

x = 1:4;
y = mean(position_shift);
e = SE(position_shift);
errorbar(x, y, e, ...
    'o','linewidth',2,'color','k')

xticks(1:4)
xlim([.5 4.5])
xticklabels({'1Bar-Uncued', '1Bar-Cued', '4Bar-Uncued', '4Bar-Cued'})
xline(0)

yticks(-5:.1:5)
ylim(y_limit)
ylabel({'Position shift (dva)', '(in direction of motion)'})
% yline(0)

title(['N = ', num2str(nsub)])
cleanplot

%% temporary statistics

signrank(position_shift(:,1), position_shift(:,3))
signrank(position_shift(:,2), position_shift(:,4))

figure
plot(variability)
