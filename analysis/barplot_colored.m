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
        [0 0 nanmean(A{i}) nanmean(A{i})], ...
        color(i,:));
    hold on    
end

% add base line
line([0 ncat+1],[0 0], 'color','k')