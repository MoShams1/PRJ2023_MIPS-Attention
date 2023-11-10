clc
clear
close all

normalize = 0;

% Specify the path to the JSON file
file_dir{1} = dir('../data/cyc02/*left*');
file_dir{2} = dir('../data/cyc02/*fair*');
file_dir{3} = dir('../data/cyc02/*right*');


for ifile = [2,1,3]

    nsub = numel(file_dir{ifile});

    for isub = 1:nsub

        jsonFilePath = ['../data/cyc02/',file_dir{ifile}(isub).name];

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
        
        if ifile == 2 && normalize
            % calculate offset
            xoffset(isub,1) = mean([median(clk_xerr(dir<0)),median(clk_xerr(dir>0))]);
        else
            xoffset(isub,1) = 0;
        end

        % create data cell
        errx_cell{ifile}(isub,1)   = median(clk_xerr(dir<0)) - xoffset(isub);
        errx_cell{ifile+3}(isub,1) = median(clk_xerr(dir>0)) - xoffset(isub);
        erry_cell{ifile}(isub,1)   = median(clk_yerr(dir<0)) - xoffset(isub);
        erry_cell{ifile+3}(isub,1) = median(clk_yerr(dir>0)) - xoffset(isub);

    end
end

labels = {'LeftBiased','Fair','RightBiased'};

%% 2D plot

% for ifile = 1:3
% 
%     figure('units','normalized','outerposition',[.1 .3 .3 .5])
%     hold on
% 
%     alpha = .25;
% 
%     h1 = scatter(errx_cell{ifile},erry_cell{ifile},'r','<','fill','markerfacealpha',alpha);
%     h2 = scatter(errx_cell{ifile+3},erry_cell{ifile+3},'b','>','fill','markerfacealpha',alpha);
% 
%     h3 = scatter(mean(errx_cell{ifile}),mean(erry_cell{ifile}),'r','o','fill');
%     h4 = scatter(mean(errx_cell{ifile+3}),mean(erry_cell{ifile+3}),'b','o','fill');
% 
%     xline(0)
%     xticks(-5:.2:5)
%     xlabel 'Horizontal click error (dva)'
% 
%     yline(0)
%     yticks(-5:.2:5)
%     ylabel 'Vertical click error (dva)'
%     
%     title(labels{ifile})
% 
%     legend([h1 h2 h3 h4],{'Left','Right','avg Left','avg Right'},'location','best')
%     
%     grid on
%     cleanplot
%     legend boxon
% 
% end

%% scatterbar

ntypes = numel(labels);

figure('units','normalized','outerposition',[.1 .3 .2 .5])
hold on

alpha = .25;

scatterbar(errx_cell(1:3),20,'r')
scatterbar(errx_cell(4:6),20,'b')

xlim([.5 ntypes+.5])
xticks(1:ntypes)
xticklabels(labels)
xlabel 'Post-flash motion bias conditions'

ylim([-1 1] * 1.2)
yticks(-2:.25:2)
yline(0)
ylabel 'Horizontal click error (dva)'

text(.75,1,'Post-Flash Rightward Motion','color','b')
text(.75,-1,'Post-Flash Leftward Motion','color','r')
grid on
cleanplot

%%
function scatterbar(A,marksz,color)

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
    line([icat-linelm icat+linelm],[nanmean(A{icat}) nanmean(A{icat})],...
        'color',color,'linewidth',2);
end

xlim([0 ncat+1])
set(gca,'xtick',1:ncat)
end
