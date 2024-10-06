clc
clear
close all

file_dir = dir('../data/cyc05/*exp01_2*');
err_mat(:,:,1) = pool3offsets(file_dir);

file_dir = dir('../data/cyc05/*exp01_1*');
err_mat(:,:,2) = pool3offsets(file_dir);

file_dir = dir('../data/cyc05/*exp01_3*');
err_mat(:,:,3) = pool3offsets(file_dir);


%% Position shift vs. Bar-Probe distance
cmap = lines(7);
p2b_base = -4:.5:4;

figure('units','inches','outerposition',[0, 0, 5, 5])
hold on
x = p2b_base;

for icurve = 1:3
    y = mean(err_mat(:,:,icurve));
    e = SE(err_mat(:,:,icurve));
    errorbar(x, y, e, ...
        'o-','linewidth',2,'color',cmap(icurve,:))
end

xticks(-4:1:4)
xlim([-4.5 4.5])
xlabel({'Probe-Bar distance (dva)', '(in direction of motion)'})
xline(0)

yticks(-5:.25:5)
ylim([-.5 1.5])
ylabel({'Position shift (dva)', '(in direction of motion)'})
yline(0)

cleanplot

%% Average plot
figure('units','inches','outerposition',[0, 0, 5, 5])

err_mat_pooled = [err_mat(:,:,1); err_mat(:,:,2); err_mat(:,:,3)];

y = mean(err_mat_pooled);
e = SE(err_mat_pooled);
errorbar(x, y, e, ...
    'o-','linewidth',2,'color','k')


xticks(-4:1:4)
xlim([-4.5 4.5])
xlabel({'Probe-Bar distance (dva)', '(in direction of motion)'})
xline(0)

yticks(-5:.25:5)
ylim([-.5 1.5])
ylabel({'Position shift (dva)', '(in direction of motion)'})
yline(0)

cleanplot
