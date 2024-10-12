clc
clear
close all

% Specify the path to the JSON files

file_dir = dir('../data/cyc05/*exp01*');
nsub = numel(file_dir);

for isub = 1:3    

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
    bar_xstart = cell2mat(struct2cell(jsonData.bar_xstart));
    bar_xstart(bar_dir == -1) = -bar_xstart(bar_dir == -1);
    
    probe_pos = reshape(cell2mat(struct2cell(jsonData.probe_pos)), 2, ntrials)';
    
    click_pos = reshape(cell2mat(struct2cell(jsonData.click_pos)), 2, ntrials)';
    click_xpos = click_pos(:,1);
    click_xerr = cell2mat(struct2cell(jsonData.click_xerr));
    click_xerr(bar_dir == -1) = -click_xerr(bar_dir == -1);
    
    cmap = lines(7);
    p2b_base = unique(probe2bar)';
    offset_base = unique(bar_xstart)';
    
    p2b_count = 0;
    for ip2b = p2b_base
        p2b_count = p2b_count+1;
        offset_count = 0;
        for ioffset = offset_base
            offset_count = offset_count+1;
            ind_p2b = probe2bar == ip2b;
            ind_offset = bar_xstart == ioffset;
            err_mat(:,p2b_count,offset_count) = click_xerr(ind_p2b & ind_offset);
        end
    end
    
    err_mat_pop(isub, :, :) = mean(err_mat,1);
    
    clear err_mat
end

%% Figure variables
y_limit = [-1 2];
cmap = lines(7);

%% Position shift vs. Bar-Probe distance
figure('units','inches','outerposition',[0, 0, 5, 5])
hold on

x = p2b_base;

for icurve = 1:3
    y = mean(err_mat_pop(:,:,icurve));
    e = SE(err_mat_pop(:,:,icurve));
    errorbar(x, y, e, ...
        'o-','linewidth',2,'color',cmap(icurve,:))
end

xticks(-4:1:4)
xlim([-4.5 4.5])
xlabel({'Probe-Bar distance (dva)', '(in direction of motion)'})
xline(0)

yticks(-5:.5:5)
ylim(y_limit)
ylabel({'Position shift (dva)', '(in direction of motion)'})
yline(0)

title(['N = ', num2str(nsub)])
cleanplot


%% Average plot
figure('units','inches','outerposition',[0, 0, 5, 5])

err_mat_pooled = [err_mat_pop(:,:,1); err_mat_pop(:,:,2); err_mat_pop(:,:,3)];

y = mean(err_mat_pooled);
e = SE(err_mat_pooled);
errorbar(x, y, e, ...
    'o-','linewidth',2,'color','k')


xticks(-4:1:4)
xlim([-4.5 4.5])
xlabel({'Probe-Bar distance (dva)', '(in direction of motion)'})
xline(0)

yticks(-5:.5:5)
ylim(y_limit)
ylabel({'Position shift (dva)', '(in direction of motion)'})
yline(0)

title(['N = ', num2str(nsub)])
cleanplot


%% Position shift vs. Probe2gaze distance
figure('units','inches','outerposition',[0, 0, 7, 5])
hold on
offset = [-2.5, 0, 2.5];
for icurve = 1:3
    y = mean(err_mat_pop(:,:,icurve));
    e = SE(err_mat_pop(:,:,icurve));
    errorbar(x+offset(icurve), y, e, ...
        'o-','linewidth',2,'color',cmap(icurve,:))
end

xticks(-7:1:7)
xlim([-7 7])
xlabel({'Probe-Gaze distance (dva)', '(in direction of motion)'})
xline(0)

yticks(-5:.5:5)
ylim(y_limit)
ylabel({'Position shift (dva)', '(in direction of motion)'})
yline(0)

title(['N = ', num2str(nsub)])
cleanplot
