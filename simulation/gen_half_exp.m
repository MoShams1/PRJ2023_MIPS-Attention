


% Mohammad Shams <MoShamsCBR@gmail.com>
% June 2023
%
% Generates horizontally cropped exponentials

function y = gen_half_exp(x, x_offset, x_coeff, amp)

y = amp * exp((x + x_offset) * x_coeff);