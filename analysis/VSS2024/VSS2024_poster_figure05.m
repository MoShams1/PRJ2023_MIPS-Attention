clc
clear
close all

% Specify the path to the JSON file
file_dir{1} = dir('../data/cyc02/complete/*left*');
file_dir{2} = dir('../data/cyc02/complete/*fair*');
file_dir{3} = dir('../data/cyc02/complete/*right*');

stp = .1;
win = .5;
k_list = 0:stp:1-win;

c_all = lines(7);
c_map = [c_all(4,:); c_all(5,:)];
color_map = [1, 0, 0; 0, 0, 1; 0, 0, 0];
offset = [-.05, .05];

label_list = {'First half', 'Second half'};

for ik = 1:length(k_list)
    for ifile = 1:3

        nsub = numel(file_dir{ifile});

        for isub = 1:nsub

            jsonFilePath = ['../data/cyc02/complete/',file_dir{ifile}(isub).name];

            % Open the JSON file and read its content
            fileID = fopen(jsonFilePath);
            jsonContent = fread(fileID, '*char')';
            fclose(fileID);

            % Parse the JSON content
            jsonData = jsondecode(jsonContent);

            % convert structure to arrays
            dir = cell2mat(struct2cell(jsonData.postflash_dir));
            clk_xerr = cell2mat(struct2cell(jsonData.click_xerr));
            clk_yerr = cell2mat(struct2cell(jsonData.click_yerr));

            % crop trials
            ntrials = length(dir);
            trials = (1:ntrials)';
            k1 = k_list(ik);
            k2 = k1+win;
            ind_trials = (trials >= (k1 * ntrials)) & (trials <= (k2 * ntrials));

            % create data cell
            errx_lM(isub, ifile) = median(clk_xerr((dir<0) & ind_trials));
            errx_rM(isub, ifile) = median(clk_xerr((dir>0) & ind_trials));

        end
    end

    rM_rB = errx_rM(:,3);
    rM_fB = errx_rM(:,2);
    rM_lB = errx_rM(:,1);

    lM_rB = errx_lM(:,3);
    lM_fB = errx_lM(:,2);
    lM_lB = errx_lM(:,1);

    fair = mean([rM_fB, -lM_fB], 2);
    biased_cng = mean([rM_rB, -lM_lB], 2);
    biased_inc = mean([rM_lB, -lM_rB], 2);

    full_mat = [biased_inc, fair, biased_cng];
    
    % remove outliers
    full_mat(6,:) = [];
        
    diff_mat_8050(:,ik) = full_mat(:,3) - full_mat(:,2);
    diff_mat_2050(:,ik) = full_mat(:,1) - full_mat(:,2);
    f_test(:,ik) = friedman(full_mat,1,"off");

end

%%

c = lines(7);
x = (win/2:stp:1-win/2) * 100;

figure('units','inches','outerposition',[1 1 9 15])
hold on

subplot(2,1,2)
plot(f_test,'-ok','markerfacecolor','k','markeredgecolor','none','linewidth',3,'markersize',10)
set(gca,'yscale','log')
yline(.05,'color',c(7,:),'linewidth',1.5,'linestyle','--')
yline(.01,'color',c(2,:),'linewidth',1.5,'linestyle','--')
yline(.001,'color',c(3,:),'linewidth',1.5,'linestyle','--')

xlim([.5 length(f_test)+.5])
xticks(1:length(x))
xticklabels(x)
xlabel 'Session progress (%)'

ylim([.0001 1])
yticks([.001, .01, .05, 1])
ylabel({'Friedman test', 'p-value'})

cleanplot
pbaspect([2 1 1])

% ------------------------
subplot(2,1,1)
hold on
errorbar(median(diff_mat_2050),SE(diff_mat_2050),'color',c_map(1,:),'linewidth',3)
errorbar(median(diff_mat_8050),SE(diff_mat_8050),'color',c_map(2,:),'linewidth',3)

xlim([.5 length(f_test)+.5])
xticks(1:length(x))
xticklabels(x)
% xlabel 'Session progress (%)'

ylabel({'Position offset from equal likelihood (dva)','in direction of motion'})
yline(0)
ylim([-.15 .15])

text(1,.15,'Likely direction','color',c_map(2,:))
text(1,-.13,'Unlikely direction','color',c_map(1,:))


cleanplot

% ------------------------
fontsize(gcf,30,"points")
saveas(gcf,'../result/VSS2024_poster_figure05.pdf')