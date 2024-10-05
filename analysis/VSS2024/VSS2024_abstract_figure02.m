clc
clear
close all

% Specify the path to the JSON file
file_dir = dir('../data/cyc02/complete/*MS01*');

figure('units','normalized','outerposition',[.1 0 .25 1])

titles = {'Equal likelihood', 'Left more likely', 'Right more likely'};

for ifile = 1:3

    jsonFilePath = ['../data/cyc02/complete/',file_dir(ifile).name];

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

    % create data cell
    errx_lM = clk_xerr(dir<0);
    errx_rM = clk_xerr(dir>0);
    erry_lM = clk_yerr(dir<0);
    erry_rM = clk_yerr(dir>0);

    % 2D plot    
    ax(ifile) = subplot(3,1,ifile);
    hold on

    alpha = .15;

    h1 = scatter(errx_lM,erry_lM,'r','<','fill','markerfacealpha',alpha);
    h2 = scatter(errx_rM,erry_rM,'b','>','fill','markerfacealpha',alpha);

    scatter(mean(errx_lM),mean(erry_lM),70,'w','o','fill');
    scatter(mean(errx_rM),mean(erry_rM),70,'w','o','fill');
    h3 = scatter(mean(errx_lM),mean(erry_lM),'r','o','fill');
    h4 = scatter(mean(errx_rM),mean(erry_rM),'b','o','fill');

    xline(0)
    xticks(-5:.5:5)
    xlabel 'Horizontal click error (dva)'

    yline(0)
    yticks(-5:.5:5)
    ylabel 'Vertical click error (dva)'

    title(titles{ifile})

    if ifile == 1
        legend([h1 h2 h3 h4],[{'Left','Right'}, {'avg Left','avg Right'}],'location','best')
    end

    axis square
    grid on
    cleanplot

end

linkaxes(ax,'xy')

function cleanplot
set(gca,'tickdir','out','color','none')
box off
end