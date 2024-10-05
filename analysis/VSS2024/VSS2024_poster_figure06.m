clc
clear
close all

% Specify the path to the JSON file
file_dir{1} = dir('../data/cyc02/complete/*left*');
file_dir{2} = dir('../data/cyc02/complete/*fair*');
file_dir{3} = dir('../data/cyc02/complete/*right*');

figure('units','inches','outerposition',[1 1 13 10])
hold on

c = lines(7);
cmap = repmat([0.*ones(1,3); c(2,:); c(6,:)],3,1);

full_full_mat = nan(19,1);

for inbefore = 1:3

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

            % calculate nbefore index
            n_before_vec = cal_n_before_index(dir);

            % crop trials
            ntrials = length(dir);
            trials = (1:ntrials)';
            
            switch inbefore                
                case 1
                    ind_trials = n_before_vec >= 0;
                case 2
                    ind_trials = (n_before_vec == 0);
                case 3
                    ind_trials = (n_before_vec > 0);
            end

            nmat{inbefore}(isub, ifile) = sum(ind_trials);

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

%     disp('Unlikely   Equally likely   Likely')
%     disp(round(median(full_mat),2))
%     disp(round(std(full_mat),3))

%     f_test(inbefore) = friedman(full_mat,1,"off");    

    full_full_mat = [full_full_mat full_mat];

end
full_full_mat(:,1) = [];
clear full_mat
full_mat(:,1:3) = [full_full_mat(:,1),full_full_mat(:,4),full_full_mat(:,7)];
full_mat(:,4:6) = [full_full_mat(:,2),full_full_mat(:,5),full_full_mat(:,8)];
full_mat(:,7:9) = [full_full_mat(:,3),full_full_mat(:,6),full_full_mat(:,9)];

x = 1:9;
y = full_mat;
barplot_colored(x,y,cmap,.35)
errorbar(...
    x,median(y),SE(y),...
    'o', ...
    'marker','none', ...    
    'color','k', ...
    'linewidth',3)

% errorbar(1:3,median(full_mat),SE(full_mat),...
%     'linewidth',2,'Color',cmap(inbefore,:),'markersize',7,...
%     'marker','o','MarkerEdgeColor','none','MarkerFaceColor',cmap(inbefore,:))

xlim([.5 9.5])
xticks(1:9)
% xticklabels({'Unlikely','Equally likely','Likely'})
% xlabel 'Motion direction likelihood condition'

ylabel({'Position offset (dva)', 'in direction of motion'})
yticks(-1:.1:1)
ylim([0 .3])
yline(0)

% text(2.7,.03,['N = ',num2str(size(full_mat,1))],'color','k')

text(.6,.295,'All trials','color',cmap(1,:))
text(.6,.28, 'No same-dir. prec. trials','color',cmap(2,:))
text(.6,.265,'>1 same-dir. prec. trials','color',cmap(3,:))

cleanplot

%% save figure
fontsize(gcf,30,"points")
saveas(gcf, '../result/VSS2024_poster_figure06.pdf')

%%
function n_vec = cal_n_before_index(dir)

for itrial = 1:length(dir)
    cmp_tr = itrial;
    nbefore = 0;
    cmpr_flag = 1;
    while cmpr_flag && (cmp_tr>1)
        cmp_tr = cmp_tr-1;
        dir_diff = dir(itrial) - dir(cmp_tr);
        if dir_diff ~= 0
            cmpr_flag = 0;
        else
            nbefore = nbefore+1;
        end
    end
    n_vec(itrial,1) = nbefore;
end
end

function p_same = cal_p_before(dir)
for i = 11:length(dir)
    p_same(i,1) = sum((dir(i-10:i-1) - dir(i)) == 0) * 10;
end
end

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