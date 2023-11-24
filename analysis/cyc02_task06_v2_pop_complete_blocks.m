clc
clear
close all

% Specify the path to the JSON file
file_dir{1} = dir('../data/cyc02/complete/*left*');
file_dir{2} = dir('../data/cyc02/complete/*fair*');
file_dir{3} = dir('../data/cyc02/complete/*right*');

k1_list = [0, .5];
k2_list = [.5, 1];

c_all = lines(7);
c_map = [c_all(5,:); c_all(2,:)];
color_map = [1, 0, 0; 0, 0, 1; 0, 0, 0];
offset = [-.05, .05];

label_list = {'First half', 'Second half'};

for ik = 1:2
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
            k1 = k1_list(ik);
            k2 = k2_list(ik);
            ind_trials = (trials >= (k1 * ntrials)) & (trials <= (k2 * ntrials));

            % create data cell
            errx_lM(isub, ifile) = median(clk_xerr((dir<0) & ind_trials));
            errx_rM(isub, ifile) = median(clk_xerr((dir>0) & ind_trials));

        end
    end

    %
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
    [~,lower_bound,upper_bound] = isoutlier(full_mat_org,'ThresholdFactor',3);
    full_mat(6,:) = [];


    figure(1)
    hold on
    errorbar((1:3)+offset(ik),median(full_mat),SE(full_mat),...
        'linewidth',2,'Color',c_map(ik,:),'linestyle',':',...
        'markersize',7,'marker','o','MarkerEdgeColor','none','MarkerFaceColor',c_map(ik,:))

    f_test = friedman(full_mat,1,"off");

    % post-hoc comparison
    m_full_mat = median(full_mat);

    inc_abschange = m_full_mat(1)-m_full_mat(2);
    inc_pval = signrank(full_mat(:,1),full_mat(:,2));
    
    cng_abschange = m_full_mat(3)-m_full_mat(2);
    cng_pval = signrank(full_mat(:,2),full_mat(:,3));
    
    cmp_abschange = m_full_mat(3)-m_full_mat(1);
    cmp_pval = signrank(full_mat(:,1),full_mat(:,3));  

    disp(['<<< ',label_list{ik},' >>>'])
    fprintf('Friedman''s Test p-val: %6.3f\n', f_test)
%     fprintf('20%% vs 50%%: Change= %5.2f dva | p-val= %5.2f\n', inc_abschange, inc_pval)
%     fprintf('80%% vs 50%%: Change= %5.2f dva | p-val= %5.2f\n', cng_abschange, cng_pval)
%     fprintf('80%% vs 20%%: Change= %5.2f dva | p-val= %5.2f\n', cmp_abschange, cmp_pval)
%     disp('---')

    % scatterbar of the differences
    figure(2)
    subplot(1,2,ik)
    hold on

    Dif_mat(:,1) = full_mat(:,2)-full_mat(:,1);
    Dif_mat(:,2) = full_mat(:,3)-full_mat(:,2);
    Dif_mat(:,3) = full_mat(:,3)-full_mat(:,1);

    scatterbar(Dif_mat, 20, color_map)
    
    title(label_list{(ik)})
    xlim([.5 3.5])
    xticks(1:3)
    xticklabels({'0.5-0.2','0.8-0.5','0.8-0.2'})
    xlabel 'Subtracted conditions'
    
    ylabel('Click error difference (dva)')
    ylim([-1, 1])
    yticks(-1:.2:1)
    yline(0)
    
    pbaspect([.5, 1, 1])
    
    cleanplot

    diff_52 = median(Dif_mat(:,1));
    pval_52 = signrank(Dif_mat(:,1));
    diff_85 = median(Dif_mat(:,2));
    pval_85 = signrank(Dif_mat(:,2));
    diff_82 = median(Dif_mat(:,3));
    pval_82 = signrank(Dif_mat(:,3));
    fprintf('50%%-20%%: median= %5.2f dva | p-val= %5.3f\n', diff_52, pval_52)
    fprintf('80%%-50%%: median= %5.2f dva | p-val= %5.3f\n', diff_85, pval_85)
    fprintf('80%%-20%%: median= %5.2f dva | p-val= %5.3f\n', diff_82, pval_82)
    disp('===')

end

%
figure(1)
xlim([.5 3.5])
xticks(1:3)
xticklabels({'0.2','0.5','0.8'})
xlabel 'Motion direction probability'

ylabel 'Click error in the direction of motion (dva)'
yticks(-1:.1:1)
yline(0)
ylim([-.1, .4])

text(1,.32,label_list{2},'color',c_map(2,:))
text(1,.335,label_list{1},'color',c_map(1,:))
text(1,.3,['N = ',num2str(size(full_mat,1))],'color','k')

cleanplot

%%
function scatterbar(A,marksz,color)
if ~iscell(A)
    A = mat2cell(A,size(A,1),ones(1,size(A,2)));
end
ncat    = numel(A); % number of categories
stdx    = .025; % standard deviation of scatters in each category
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
        'color',color(icat,:),'linewidth',.5);
    line([icat-linelm icat+linelm], [iq75_A iq75_A],...
        'color',color(icat,:),'linewidth',.5);
end

xlim([0 ncat+1])
set(gca,'xtick',1:ncat)
end
