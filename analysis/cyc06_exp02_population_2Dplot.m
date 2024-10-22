clc
clear
close all

% Specify the path to the JSON files

file_dir = dir('../data/cyc06/*exp02*');
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
    ntrials = length(cell2mat(struct2cell(jsonData.probe2bar_rel2motion)));
    bar_dir = cell2mat(struct2cell(jsonData.motion_dir));

    probe2bar = cell2mat(struct2cell(jsonData.probe2bar_rel2motion));
    probe_pos = repmat([0,5], ntrials, 1);
    click_pos = reshape(cell2mat(struct2cell(jsonData.click_pos)), 2, ntrials)';    
    click_xerr = cell2mat(struct2cell(jsonData.click_xerr));
    click_xerr(bar_dir == -1) = -click_xerr(bar_dir == -1);    
    click_yerr = cell2mat(struct2cell(jsonData.click_yerr));

    click_xpos = click_pos(:,1);
    click_xpos(bar_dir == -1) = -click_xpos(bar_dir == -1);
    click_ypos = click_pos(:,2);

    p2b_base = unique(probe2bar)';

    p2b_count = 0;
    for ip2b = p2b_base
        p2b_count = p2b_count+1;
        ind_p2b = probe2bar == ip2b;
        err_mat_x(:,p2b_count) = click_xerr(ind_p2b);
        err_mat_y(:,p2b_count) = click_yerr(ind_p2b);
        click_mat_x(:,p2b_count) = click_xpos(ind_p2b);
        click_mat_y(:,p2b_count) = click_ypos(ind_p2b);
    end

    err_mat_pop_x(isub, :) = mean(err_mat_x,1);
    err_mat_pop_y(isub, :) = mean(err_mat_y,1);
    click_mat_pop_x(isub, :) = mean(click_mat_x,1);
    click_mat_pop_y(isub, :) = mean(click_mat_y,1);

    clear err_mat_x err_mat_y click_mat_x click_mat_y
end

%% Figure variables
y_limit = [-.5 1.5];
cmap = lines(7);

%% Position shift vs. Bar-Probe distance
figure('units','inches','outerposition',[0, 0, 5, 5])
hold on

x = p2b_base;
y = mean(err_mat_pop_x);
e = SE(err_mat_pop_x);
errorbar(x, y, e, ...
    'o-','linewidth',2,'color','k')


xticks(-4:1:4)
xlim([-4.5 4.5])
xlabel({'Probe-Bar distance (dva)', '(in direction of motion)'})
xline(0)

yticks(-5:.25:5)
ylim(y_limit)
ylabel({'Position shift (dva)', '(in direction of motion)'})
yline(0)

title(['N = ', num2str(nsub)])
cleanplot


%% Horizontal position shift vs. Bar-Probe distance
figure('units','inches','outerposition',[0, 0, 5, 5])
hold on

x = p2b_base;
y = mean(err_mat_pop_y);
e = SE(err_mat_pop_y);
errorbar(x, y, e, ...
    'o-','linewidth',2,'color','k')


xticks(-4:1:4)
xlim([-4.5 4.5])
xlabel({'Probe-Bar distance (dva)', '(in direction of motion)'})
xline(0)

yticks(-5:.25:5)
ylim([-2.5 0])
ylabel({'Vertical position shift (dva)'})
yline(0)

title(['N = ', num2str(nsub)])
cleanplot


%% Radial position shift vs. Bar-Probe distance

err_mat_pop_r = sqrt(err_mat_pop_x.^2 + err_mat_pop_y.^2);

figure('units','inches','outerposition',[0, 0, 5, 5])
hold on

x = p2b_base;
y = mean(err_mat_pop_r);
e = SE(err_mat_pop_r);
errorbar(x, y, e, ...
    'o-','linewidth',2,'color','k')


xticks(-4:1:4)
xlim([-4.5 4.5])
xlabel({'Probe-Bar distance (dva)', '(in direction of motion)'})
xline(0)

yticks(-5:.5:5)
ylim([0 3])
ylabel({'Radial position shift (dva)'})
yline(0)

title(['N = ', num2str(nsub)])
cleanplot


%% Angular position shift vs. Bar-Probe distance

err_mat_pop_theta = atan2d(err_mat_pop_y, err_mat_pop_x);
ind_neg = err_mat_pop_theta<0;
ind_q4 = err_mat_pop_theta>=90;
err_mat_pop_theta(ind_neg) = err_mat_pop_theta(ind_neg) + 360;

figure('units','inches','outerposition',[0, 0, 5, 5])
hold on

x = p2b_base;
y = mean(err_mat_pop_theta);
e = SE(err_mat_pop_theta);
errorbar(x, y, e, ...
    'o-','linewidth',2,'color','k')


xticks(-4:1:4)
xlim([-4.5 4.5])
xlabel({'Probe-Bar distance (dva)', '(in direction of motion)'})
xline(0)

yticks(-360:15:360)
ylim([225 315])
ylabel({'Angular position shift (deg)','(motion: 360 deg; gaze: 270 deg'})
yline(0)

title(['N = ', num2str(nsub)])
cleanplot


%% 2D position shift vs. Bar-Probe distance

figure('units','inches','outerposition',[0, 0, 5, 5])
hold on

x = mean(click_mat_pop_x);
y = mean(click_mat_pop_y);
e_x = SE(click_mat_pop_x);
e_y = SE(click_mat_pop_y);
errorbar(x,y,e_y/2,e_y/2,e_x/2,e_x/2,'ok')

plot(0,0,'ok')
% plot(0,5,'or','markerfacecolor','r')

xticks(-4:1:4)
xlim([-4.5 4.5])
xlabel({'Horizontal distance (dva)'})
% xline(0)

yticks(-10:1:10)
ylim([-.5 5.5])
ylabel({'Vertical distance (dva)'})
yline(5,'r')

cleanplot

%% 2D position shift vs. Bar-Probe distance (arrow plot)

figure('units','inches','outerposition',[0, 0, 5, 5])
hold on

x = -4:.5:4;
y = 5 * ones(1,numel(x));
u = mean(err_mat_pop_x);
v = mean(err_mat_pop_y);
quiver(x,y,u,v, ...
    'k','linewidth',2);

scatter(0,0,100,'+k')

xticks(-5:1:5)
xlim([-5 5])
xlabel({'Horizontal distance (dva)'})

yticks(-10:1:10)
ylim([-.5 5.5])
ylabel({'Vertical distance (dva)'})

cleanplot