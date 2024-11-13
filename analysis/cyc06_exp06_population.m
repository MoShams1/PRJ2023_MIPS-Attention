clc
clear
close all

% Specify the path to the JSON files

file_dir = dir('../data/cyc06/*exp06*');
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
    bar_dir = cell2mat(struct2cell(jsonData.motion_dir));

    motion_state = struct2cell(jsonData.motion_state);

    ind_dynamic = strcmp(motion_state, 'dynamic');
    ind_static = strcmp(motion_state, 'static');

    probe2bar = cell2mat(struct2cell(jsonData.probe2bar_ms));
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
        err_mat_static(:,p2b_count) = click_xerr(ind_p2b & ind_static);
        err_mat_dynamic(:,p2b_count) = click_xerr(ind_p2b & ind_dynamic);
    end

    err_mat_static_pop(isub, :) = mean(err_mat_static,1);
    err_mat_dynamic_pop(isub, :) = mean(err_mat_dynamic,1);

    clear err_mat_static err_mat_dynamic
end

%% Figure variables
y_limit = [-.5 1.5];
cmap = lines(7);

%% Position shift vs. Bar-Probe distance (average)
figure('units','inches','outerposition',[0, 0, 5, 5])
hold on

x = p2b_base;
y = mean(err_mat_static_pop);
e = SE(err_mat_static_pop);
errorbar(x, y, e, ...
    'o-','linewidth',2,'color','k')
y = mean(err_mat_dynamic_pop);
e = SE(err_mat_dynamic_pop);
errorbar(x, y, e, ...
    'o-','linewidth',2,'color','r')

xticks(-200:100:300)
xlim([-250 350])
xlabel({'Probe-Bar SOA (ms)'})
xline(0)

yticks(-5:.25:5)
ylim(y_limit)
ylabel({'Position shift (dva)', '(in direction of motion)'})
yline(0)

title(['N = ', num2str(nsub)])
cleanplot
