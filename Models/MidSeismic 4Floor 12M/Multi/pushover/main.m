clc; clear; close all;

config = Config;

[capacity_sd, ap] = epa(config, 'inverted_triangle');

evalution(config, 'mmc');
evalution(config, 'inverted_triangle');
[dy(1), sdd(1), sdm(1)] = evalution(config, 'mode1');
[dy(2), sdd(2), sdm(2)] = evalution(config, 'mode2');
[dy(3), sdd(3), sdm(3)] = evalution(config, 'mode3');


% dy = sqrt(sum(dy .^ 2));
% sdd = sqrt(sum(sdd .^ 2));
% sdm = sqrt(sum(sdm .^ 2));

Ra = sqrt(sum(((sdd ./ dy) .^ 2)))
R = sqrt(sum(((sdm ./ dy) .^ 2)))

