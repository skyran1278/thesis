clc; clear; close all;

multi = Multi;
tradition = Tradition;

% [capacity_sd, ap] = epa(config, 'inverted_triangle');

% evalution(multi, 'inverted_triangle', 'multi');
% evalution(tradition, 'inverted_triangle', 'tradition');

% [dy_multi(1), sdd_multi(1), sdm_multi(1)] = evalution(multi, 'mode1', 'multi');
% [dy(1), sdd(1), sdm(1)] = evalution(tradition, 'mode1', 'tradition');
% [dy_multi(2), sdd_multi(2), sdm_multi(2)] = evalution(multi, 'mode2', 'multi');
% [dy(2), sdd(2), sdm(2)] = evalution(tradition, 'mode2', 'tradition');
% [dy_multi(3), sdd_multi(3), sdm_multi(3)] = evalution(multi, 'mode3', 'multi');
% [dy(3), sdd(3), sdm(3)] = evalution(tradition, 'mode3', 'tradition');

% Ra = sqrt(sum(((sdd_multi ./ dy_multi) .^ 2)));
% R = sqrt(sum(((sdm_multi ./ dy_multi) .^ 2)));
% fprintf('%.2f\t%.2f\n\n', Ra, R);

% Ra = sqrt(sum(((sdd ./ dy) .^ 2)));
% R = sqrt(sum(((sdm ./ dy) .^ 2)));
% fprintf('%.2f\t%.2f\n\n', Ra, R);

evalution(multi, 'mmc', 'multi');
evalution(tradition, 'mmc', 'tradition');



