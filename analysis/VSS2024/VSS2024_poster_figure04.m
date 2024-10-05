clc
clear
close all

% Specify the path to the JSON file
file_dir{1} = dir('../data/cyc02/complete/*left*');
file_dir{2} = dir('../data/cyc02/complete/*fair*');
file_dir{3} = dir('../data/cyc02/complete/*right*');    

% figure('units','normalized','outerposition',[.26 .3 .62 .5])

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
        k1 = 0;
        k2 = 1;
        ind_trials = (trials >= (k1 * ntrials)) & (trials <= (k2 * ntrials));
        
        % create data cell
        errx_lM(isub, ifile) = median(clk_xerr((dir<0) & ind_trials));
        errx_rM(isub, ifile) = median(clk_xerr((dir>0) & ind_trials));        

    end
end

%% 
gray = .5 * ones(1,3);

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
full_mat_org = full_mat;
[outlier_logic_mat,lower_bound,upper_bound] = isoutlier(full_mat_org,'ThresholdFactor',3);
outlier_ind = any(outlier_logic_mat,2);
full_mat(outlier_ind,:) = [];
outlier_mat = full_mat_org(outlier_ind,:);

%%
figure('units','inches','outerposition',[1 1 10 12])
hold on
% errorbar(1:3,median(full_mat),SE(full_mat),'linewidth',3,'Color','k','markersize',15,...
%     'marker','o','MarkerEdgeColor','none','MarkerFaceColor','k')  % without outliers
x = 1:3;
cmap = lines(7);
c = [cmap(4,:); .6*ones(1,3); cmap(5,:)];
barplot_colored(x,full_mat,c,.35)
errorbar(...
    x,median(full_mat),SE(full_mat),...
    'o', ...
    'marker','none', ...    
    'color','k', ...
    'linewidth',3)

xlim([.5 3.5])
xticks(1:3)
xticklabels({'Unlikely','Equally likely','Likely'})
% xlabel 'Motion direction likelihood condition'

ylabel({'Position offset (dva)', 'in direction of motion'})
yticks(-1:.1:1)
yline(0)

text(1,.2,['N = ',num2str(size(full_mat,1))],'color','k')

cleanplot

%% statistics
[pval, stats] = friedman(full_mat,1,"off");
fprintf('<Friedman test> Chi-sq(%d, %d)=%6.3f, p=%5.3f \n', stats{2,3}, nsub, stats{2,5}, stats{2,6})

[med, p21, W, z, r] = signrank_full(full_mat(:,2), full_mat(:,1));
[med, p32, W, z, r] = signrank_full(full_mat(:,3), full_mat(:,2));
[med, p31, W, z, r] = signrank_full(full_mat(:,3), full_mat(:,1));
p_list = [p21, p32, p31];
[sig, alpha_hat, p_adjusted] = BH_correct(p_list, .05, 2);

%% add stats to figure

line([1 3], [.3 .3], 'color', 'k', 'linewidth', 3)
text(2, .305, '***', 'horizontalalignment','center')

line([2.2 3], [.285 .285], 'color', 'k', 'linewidth', 3)
text(2.6, .29, '*', 'horizontalalignment','center')

line([1 1.8], [.285 .285], 'color', 'k', 'linewidth', 3)
text(1.4, .293, '\itn.s.', 'horizontalalignment','center')

fontsize(gcf,30,"points")
saveas(gcf,'../result/VSS2024_poster_figure04.pdf')

%%
function barplot_colored(x, A, color, bw)
% barSEmean(A, color)
% x: bar horizontal positions
% A: cell or mat (repetition x category), comma separated!
% color: color matrix (category x 3)
% bw: bar width
% 
% Mo Shams <m.shams.ahmar@gmail.com>
% Feb 2024
%

if isnumeric(A)
    for icol = 1:size(A,2)
        A_cell{icol} = A(:,icol);
    end
    A = A_cell;
end

ncat = numel(A); % number of categories

for i = x
    fill( ...
        [i-bw,i+bw,i+bw,i-bw], ...
        [0 0 nanmedian(A{i}) nanmedian(A{i})], ...
        color(i,:),...
        'edgecolor','none', ...
        'facealpha',.5);
    hold on    
end

% add base line
line([0 ncat+1],[0 0], 'color','k')
end
