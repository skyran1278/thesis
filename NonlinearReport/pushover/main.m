clc; clear; close all;

config = Config;

[capacity_sd, ap] = epa(config, 'inverted_triangle');

evalution(config, 'inverted_triangle');

[dy(1), sdd(1), sdm(1)] = evalution(config, 'mode1');
[dy(2), sdd(2), sdm(2)] = evalution(config, 'mode2');
[dy(3), sdd(3), sdm(3)] = evalution(config, 'mode3');
Ra = sqrt(sum(((sdd ./ dy) .^ 2)));
R = sqrt(sum(((sdm ./ dy) .^ 2)));

fprintf('%.2f\t%.2f\n\n', Ra, R);

evalution(config, 'mmc');



