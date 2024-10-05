clc
clear
close all

% Specify the path to the JSON file
jsonFilePath{1} = '../data/cyc01/ECVP23_Exp03/0001_20230601_112438.json';
jsonFilePath{2} = '../data/cyc01/ECVP23_Exp03/0005_20230602_105623.json';
jsonFilePath{3} = '../data/cyc01/ECVP23_Exp03/0011_20230601_120919.json';
jsonFilePath{4} = '../data/cyc01/ECVP23_Exp03/1191_20230602_113813.json';
jsonFilePath{5} = '../data/cyc01/ECVP23_Exp03/2002_20230601_105314.json';
jsonFilePath{6} = '../data/cyc01/ECVP23_Exp03/AR01_20230227_195314.json';
jsonFilePath{7} = '../data/cyc01/ECVP23_Exp03/MS01_20230228_115227.json';

for isub = 1:numel(jsonFilePath)
    
    % Open the JSON file and read its content
    fileID = fopen(jsonFilePath{isub});
    jsonContent = fread(fileID, '*char')';
    fclose(fileID);
    
    % Parse the JSON content
    jsonData = jsondecode(jsonContent);
    
    % convert structure to arrays
    temp = cell2mat(struct2cell(jsonData.probe_loc));
    flash_loc(:,1) = temp(1:2:end);
    flash_loc(:,2) = temp(2:2:end);
    temp = cell2mat(struct2cell(jsonData.click_loc));
    click_loc(:,1) = temp(1:2:end);
    click_loc(:,2) = temp(2:2:end);
    bar_loc = round(cell2mat(struct2cell(jsonData.movobj_atflash)));
    bar_time = (bar_loc - 90) / 360 * 1000;
    x = unique(bar_loc);
    click_err = click_loc - flash_loc;
    angular_shift = -atand(click_err(:,2)./click_err(:,1));
    
    % create plot matrix
    for ibarloc = 1:size(x)
        angular_shift_mat(isub, ibarloc) = nanmean(angular_shift(bar_loc==x(ibarloc)));
        hor_shift_mat(isub, ibarloc) = nanmean(click_err(bar_loc==x(ibarloc),1));
    end

    clear flash_loc click_loc 

end
    
% plot
x = unique(bar_loc(:,1));
y = mean(hor_shift_mat,1);
err = SE(hor_shift_mat);

figure('units','normalized','outerposition',[.1 .1 .25 .45])
hold on
tl = tiledlayout(1,1);

ax1 = axes(tl);
ax1.XAxisLocation = 'bottom';
ax1.YAxisLocation = 'left';
errorbar(ax1,x,y,err,'-ok','markerfacecolor','k','linewidth',1,'markersize',4)
xline(90,'--')
yline(0,'--')
xlim([0-10 180])
xticks(0:45:180)
xticklabels((-90:45:90) ./ 360 .* 1000)
xlabel 'Bar relative to flash (ms)'
ylim([-.4-.1 .8+.1])
yticks(-.4:.4:.8)
ylabel({'Illusory shift', 'in the direction of motion (dva)'})

cleanplot

ax2 = axes(tl);
ax2.XAxisLocation = 'top';
ax2.YColor = 'none';
xlim([0-10 180])
xticks(0:45:180)
xticklabels(-90:45:90)
xlabel 'Bar relative to flash (deg)'

cleanplot