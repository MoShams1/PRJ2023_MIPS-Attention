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
color_map = [1, 0, 0; 0, 0, 1];

label_list = {'first half', 'second half'};

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

    full_mat = [fair, biased_inc, biased_cng];
    
    figure(1)
    hold on
    errorbar(1:3,median(full_mat),SE(full_mat),'linewidth',2,'Color',c_map(ik,:),...
        'markersize',7,'marker','o','MarkerEdgeColor','none','MarkerFaceColor',c_map(ik,:))

    f_test = friedman(full_mat,1,"off");

    % post-hoc comparison
    m_full_mat = median(full_mat);

    inc_abschange = median(full_mat(:,2)-full_mat(:,1));
    inc_pval = median(signrank(full_mat(:,2),full_mat(:,1)));
    
    cng_abschange = median(full_mat(:,3)-full_mat(:,1));
    cng_pval = signrank(full_mat(:,3),full_mat(:,1));

    cmp_abschange = median(full_mat(:,3)-full_mat(:,2));
    cmp_pval = signrank(full_mat(:,3),full_mat(:,2));    

    disp(['<<< ',label_list{ik},' >>>'])
    fprintf('Friedman''s Test p-val: %6.2f\n', f_test)
    fprintf('Unlikely vs Fair: Change= %5.2f dva | p-val= %5.2f\n', inc_abschange, inc_pval)
    fprintf('Likely vs Fair  : Change= %5.2f dva | p-val= %5.2f\n', cng_abschange, cng_pval)
    fprintf('Unlik. vs Lik.  : Change= %5.2f dva | p-val= %5.2f\n', cmp_abschange, cmp_pval)
    disp('---')

    % scatterbar of the differences
    figure(2)
    subplot(1,2,ik)
    hold on

    Dif_mat(:,1) = full_mat(:,2)-full_mat(:,1);
    Dif_mat(:,2) = full_mat(:,3)-full_mat(:,1);

    scatterbar(Dif_mat, 20, color_map)
    
    xlim([.5 2.5])
    xticks(1:2)
    xticklabels({'Unlikely dir.','Likely dir.'})
    
    ylabel 'Click error difference rel. fair condition (dva)'
    ylim([-1, 1])
    yticks(-1:.2:1)
    yline(0)
    
    pbaspect([.5, 1, 1])
    
    cleanplot

    diff_unlikely = median(Dif_mat(:,1));
    pval_unlikely = signrank(Dif_mat(:,1));
    diff_likely = median(Dif_mat(:,2));
    pval_likely = signrank(Dif_mat(:,2));
    fprintf('Unlikely: median= %5.2f dva | p-val= %5.2f\n', diff_unlikely, pval_unlikely)
    fprintf('Likely  : median= %5.2f dva | p-val= %5.2f\n', diff_likely, pval_likely)
    disp('===')

end

%%
figure(1)
xlim([.5 3.5])
xticks(1:3)
xticklabels({'Fair','Biased-UnlikelyDir','Biased-LikelyDir'})

ylabel 'Click error (dva)'
yticks(0:.1:1)
yline(0)

text(1,.32,'Second half','color',c_map(2,:))
text(1,.335,'First half','color',c_map(1,:))
text(1,.3,['N = ',num2str(size(full_mat,1))],'color','k')

cleanplot

%%
function scatterbar(A,marksz,color)
if ~iscell(A)
    A = mat2cell(A,size(A,1),ones(1,size(A,2)));
end
ncat    = numel(A); % number of categories
stdx    = .05; % standard deviation of scatters in each category
linelm  = .3; % line length for median
alpha   = .3;

hold on
for icat = 1:ncat
    rng default
    n = numel(A{icat});
    x = randn(n,1)*stdx + icat;

    scatter(x,A{icat},marksz,color(icat,:),'o','fill','markerfacealpha',alpha);
    line([icat-linelm icat+linelm],[nanmedian(A{icat}) nanmedian(A{icat})],...
        'color',color(icat,:),'linewidth',2);
end

xlim([0 ncat+1])
set(gca,'xtick',1:ncat)
end
