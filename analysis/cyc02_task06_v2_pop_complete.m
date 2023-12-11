clc
clear
close all

% Specify the path to the JSON file
file_dir{1} = dir('../data/cyc02/complete/*left*');
file_dir{2} = dir('../data/cyc02/complete/*fair*');
file_dir{3} = dir('../data/cyc02/complete/*right*');    

figure('units','normalized','outerposition',[.26 .3 .62 .5])

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

for icol = 1:3
    pval(icol) = signrank(full_mat(:,icol));
end

disp('Unlikely   Equally likely   Likely')
disp('median')
disp(round(median(full_mat),2))
disp('std')
disp(round(std(full_mat),3))
disp('pvals')
disp(round(pval,3))

subplot(1,3,1)
hold on
plot(full_mat','-o','color',gray,'markerfaceColor',gray,...
    'markersize',4, 'markeredgecolor','none')  % without outliers
% errorbar(1:3,median(full_mat),SE(full_mat),'linewidth',2,'Color','k','markersize',7,...
%     'marker','o','MarkerEdgeColor','none','MarkerFaceColor','k')  % without outliers
plot(lower_bound,':r','linewidth',1.5)
plot(upper_bound,':r','linewidth',1.5)
plot(outlier_mat','-o','color','r','markerfaceColor','r',...
    'markersize',4, 'markeredgecolor','none')  % the outliers

xlim([.5 3.5])
xticks(1:3)
xticklabels({'Unlikely','Equally likely','Likely'})
xlabel 'Motion direction likelihood condition'

ylabel 'Click error in direction of motion (dva)'
ylim([-1, 1.5])
yticks(-1:.5:2)
yline(0)

grid on

% text(1,1,['N = ',num2str(size(full_mat_org,1))],'color','r')
% text(1,.7,['N = ',num2str(size(full_mat,1))],'color','k')
text(1,1.1,['N = ',num2str(size(full_mat_org,1))],'color','k')

pbaspect([1,1.5,1])
cleanplot

f_test = friedman(full_mat,1,"off");

% post-hoc comparison
m_full_mat = median(full_mat);

inc_popchange = m_full_mat(2)-m_full_mat(1);
inc_change = median(full_mat(:,2)-full_mat(:,1));
inc_pval = signrank(full_mat(:,2),full_mat(:,1));

cng_popchange = m_full_mat(3)-m_full_mat(2);
cng_change = median(full_mat(:,3)-full_mat(:,2));
cng_pval = signrank(full_mat(:,3),full_mat(:,2));

cmp_popchange = m_full_mat(3)-m_full_mat(1);
cmp_change = median(full_mat(:,3)-full_mat(:,1));
cmp_pval = signrank(full_mat(:,3),full_mat(:,1));

fprintf('Friedman''s Test p-val: %6.3f (N = %d)\n\n', f_test, size(full_mat,1))
fprintf('Median motion-induced shift at 50%% conditio: %5.2f dva\n\n', median(full_mat(:,2)))
fprintf('20%% vs 50%%:\n   Median ind. diff= %5.2f dva (pop. diff: %5.2f dva) | p= %5.3f\n', inc_change, inc_popchange, inc_pval)
fprintf('80%% vs 50%%:\n   Median ind. diff= %5.2f dva (pop. diff: %5.2f dva) | p= %5.3f\n', cng_change, cng_popchange, cng_pval)
fprintf('80%% vs 20%%:\n   Median ind. diff= %5.2f dva (pop. diff: %5.2f dva) | p= %5.3f\n', cmp_change, cmp_popchange, cmp_pval)

%%
% figure('units','normalized','outerposition',[.43 .5 .2 .35])

subplot(1,3,2)
hold on
errorbar(1:3,median(full_mat),SE(full_mat),'linewidth',2,'Color','k','markersize',7,...
    'marker','o','MarkerEdgeColor','none','MarkerFaceColor','k')  % without outliers

xlim([.5 3.5])
xticks(1:3)
xticklabels({'Unlikely','Equally likely','Likely'})
xlabel 'Motion direction likelihood condition'

ylabel 'Click error in direction of motion (dva)'
yticks(-1:.1:1)
yline(0)

text(1,.25,['N = ',num2str(size(full_mat,1))],'color','k')

pbaspect([1,1,1])
cleanplot

%%

c_all = lines(7);
% c_map = [c_all(1,:); c_all(7,:)];
c_map = zeros(2,3);
gray = .7 * ones(1,3);

% figure('units','normalized','outerposition',[.63 .5 .15 .35])
subplot(1,3,3)
hold on

Dif_mat(:,1) = full_mat(:,2);
Dif_mat(:,2) = full_mat(:,3)-full_mat(:,1);

plot(Dif_mat','-','color',gray)

scatterbar(Dif_mat, 20, c_map)

xlim([.5 2.5])
xticks(1:2)
xticklabels({'Equally likely','Likely - Unlikely'})
xlabel 'Motion direction likelihood condition'

ylabel('Click error in direction of motion (dva)')
% ylim([-1, 1])
yticks(-1:.2:1)
yline(0)

text(2,.5,['N = ',num2str(size(Dif_mat,1))],'color','k')

pbaspect([.7,1.2,1])
cleanplot


%%
function scatterbar(A,marksz,color)
if ~iscell(A)
    A = mat2cell(A,size(A,1),ones(1,size(A,2)));
end
ncat    = numel(A); % number of categories
stdx    = .00025; % standard deviation of scatters in each category
linelm  = .3; % line length for median
alpha   = .3;

hold on
for icat = 1:ncat
    rng default
    n = numel(A{icat});
    x = randn(n,1)*stdx + icat;
    
    med_A = median(A{icat});
    iq25_A = prctile(A{icat},25);
    iq75_A = prctile(A{icat},75);

    scatter(x,A{icat},marksz,color(icat,:),'o','fill','markerfacealpha',alpha);
    line([icat-linelm icat+linelm], [med_A med_A],...
        'color',color(icat,:),'linewidth',2);
    line([icat-linelm icat+linelm], [iq25_A iq25_A],...
        'color',color(icat,:),'linewidth',1);
    line([icat-linelm icat+linelm], [iq75_A iq75_A],...
        'color',color(icat,:),'linewidth',1);
end

xlim([0 ncat+1])
set(gca,'xtick',1:ncat)
end