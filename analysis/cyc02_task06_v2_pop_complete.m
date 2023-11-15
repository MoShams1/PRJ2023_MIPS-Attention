clc
clear
close all

% Specify the path to the JSON file
file_dir{1} = dir('../data/cyc02/complete/*left*');
file_dir{2} = dir('../data/cyc02/complete/*fair*');
file_dir{3} = dir('../data/cyc02/complete/*right*');    


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

        % create data cell
        errx_lM(isub, ifile) = median(clk_xerr(dir<0));
        errx_rM(isub, ifile) = median(clk_xerr(dir>0));        

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

% fair = mean([rM_fB], 2);
% biased_cng = mean([rM_rB], 2);
% biased_inc = mean([rM_lB], 2);

% fair = mean([-lM_fB], 2);
% biased_cng = mean([-lM_lB], 2);
% biased_inc = mean([-lM_rB], 2);

full_mat = [fair, biased_inc, biased_cng];
figure
hold on
plot(full_mat','-o','color',gray,'markerfaceColor',gray,...
    'markersize',4, 'markeredgecolor','none')
errorbar(1:3,median(full_mat),SE(full_mat),'linewidth',2,'Color','k','markersize',7,...
    'marker','o','MarkerEdgeColor','none','MarkerFaceColor','k')

xlim([.5 3.5])
xticks(1:3)
xticklabels({'Fair','Biased-UnlikelyDir','Biased-LikelyDir'})

ylabel 'Click error (dva)'

yline(0)

cleanplot

friedman(full_mat)

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

    scatter(x,A{icat},marksz,color,'o','fill','markerfacealpha',alpha);
    line([icat-linelm icat+linelm],[nanmedian(A{icat}) nanmedian(A{icat})],...
        'color',color,'linewidth',2);
end

xlim([0 ncat+1])
set(gca,'xtick',1:ncat)
end
