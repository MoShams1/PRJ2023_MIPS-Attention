clc
clear
close all

% Specify the path to the JSON file
file_dir = dir('../data/cyc02/complete/*MS01*');

figure('units','inches','outerposition',[1 1 10 25])

titles = {'Equally likely', 'Left more likely', 'Right more likely'};

cmap = lines(7);
c_likely = cmap(5,:);
c_unlikely = cmap(4,:);
c_equal = .5 .* ones(1,3);

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

    alpha = .25;
    msz_click = 100;
    msz_mean = 150;
    msz_mean_edge = msz_mean * 1.5;
    
    if ifile == 1
        c_left = c_equal .* 1.2;
        c_right = c_equal .* .6;
    end
    if ifile == 2
        c_left = c_likely;
        c_right = c_unlikely;
    end
    if ifile == 3
        c_left = c_unlikely;
        c_right = c_likely;
    end

    h1 = scatter(errx_lM,erry_lM,msz_click,c_left,'<','fill','markerfacealpha',alpha);
    h2 = scatter(errx_rM,erry_rM,msz_click,c_right,'>','fill','markerfacealpha',alpha);

    scatter(mean(errx_lM),mean(erry_lM),msz_mean_edge,'k','o','fill');
    scatter(mean(errx_rM),mean(erry_rM),msz_mean_edge,'k','o','fill');
    h3 = scatter(mean(errx_lM),mean(erry_lM),msz_mean,c_left,'o','fill');
    h4 = scatter(mean(errx_rM),mean(erry_rM),msz_mean,c_right,'o','fill');

    xline(0)
    xticks(-5:2:5)
    if ifile == 3
        xlabel 'Horizontal position offset (dva)'
    end

    yline(0)
    yticks(-5:2:5)
    if ifile == 2
        ylabel 'Vertical position offset (dva)'
    end

%     title(titles{ifile})

%     if ifile == 1
%         legend([h1 h2 h3 h4],[{'Left','Right'}, {'avg Left','avg Right'}],'location','best')
%     end

    axis square
    axis(1.5.*[-1 1 -1 1])
%     grid on
    cleanplot

end

linkaxes(ax,'xy')
fontsize(gcf,30,'points')

saveas(gcf,'../result/VSS2024_poster_figure03.pdf')

function cleanplot
set(gca,'tickdir','out','color','none')
box off
end