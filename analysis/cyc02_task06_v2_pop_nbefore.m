clc
clear
close all

% Specify the path to the JSON file
file_dir{1} = dir('../data/cyc02/complete/*left*');
file_dir{2} = dir('../data/cyc02/complete/*fair*');
file_dir{3} = dir('../data/cyc02/complete/*right*');

figure('units','normalized','outerposition',[.2 .2 .2 .35])
hold on

c = lines(7);
cmap = [zeros(1,3); c(5,:); c(3,:)];

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

    f_test(inbefore) = friedman(full_mat,1,"off");    

    errorbar(1:3,median(full_mat),SE(full_mat),...
        'linewidth',2,'Color',cmap(inbefore,:),'markersize',7,...
        'marker','o','MarkerEdgeColor','none','MarkerFaceColor',cmap(inbefore,:))

end

xlim([.5 3.5])
xticks(1:3)
xticklabels({'Unlikely','Equally likely','Likely'})
xlabel 'Motion direction likelihood condition'

ylabel 'Click error in direction of motion (dva)'
yticks(-1:.1:1)
yline(0)

text(2.7,.03,['N = ',num2str(size(full_mat,1))],'color','k')

text(.6,.295,'All trials','color',cmap(1,:))
text(.6,.28, 'No same-dir. prec. trials','color',cmap(2,:))
text(.6,.265,'>1 same-dir. prec. trials','color',cmap(3,:)*.9)

pbaspect([1,1,1])
cleanplot

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