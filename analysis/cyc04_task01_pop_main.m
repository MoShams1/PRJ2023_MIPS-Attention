clc
clear
close all

%%% FIGURE 1
figure('units','inches','outerposition',[7, 4, 4, 10])

subplot(3,1,1)
cyc04_task01_pop_analysis_all
y1 = y;
clearvars -except x y1

subplot(3,1,2)
cyc04_task01_pop_analysis_yes_correct
y2 = y;
clearvars -except x y1 y2

subplot(3,1,3)
cyc04_task01_pop_analysis_yes_wrong_or_no
y3 = y;
clearvars -except x y1 y2 y3

%%% FIGURE 2
figure('units','inches','outerposition',[7, 4, 3, 4])
hold on

lw = 1.5;
cmap = lines(7);
c_all = zeros(1,3);
c_correct = cmap(5,:);
c_wrong = cmap(7,:);
xticklabels_vec = {'LikelyD-LeadP', 'UnlikelyD-LeadP', 'UnlikelyD-TrailP', 'LikelyD-TrailP'};

errorbar(x,mean(y1),SE(y1),'-o','color',c_all,'LineWidth',lw,'MarkerFaceColor',c_all)
errorbar(x,mean(y2),SE(y2),'-o','color',c_correct,'LineWidth',lw,'MarkerFaceColor',c_correct)
errorbar(x,mean(y3),SE(y3),'-o','color',c_wrong,'LineWidth',lw,'MarkerFaceColor',c_wrong)


xticks(1:4)
xticklabels(xticklabels_vec)
xlim([.5 4])

ylabel 'Absolute perceived shift (dva)'
yticks(0:3)
ylim([-.5 3])

yline(0,'--')

text(1, 2.8, 'All', 'color',c_all)
text(1, 2.6, 'Biased correctly perceived', 'color',c_correct)
text(1, 2.4, 'Biased not (correctly) perceived', 'color',c_wrong)

cleanplot

