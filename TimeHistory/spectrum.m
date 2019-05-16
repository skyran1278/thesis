clc; clear; close all;

structure_period = 0.965;
ss_s1 = [0.66, 0.49, 0.8, 0.54];

% pick 7 time history
filenames = [
  "RSN725_SUPER.B_B-POE360", "RSN900_LANDERS_YER270", "RSN953_NORTHR_MUL279", "RSN960_NORTHR_LOS000", "RSN1111_KOBE_NIS000", "RSN1116_KOBE_SHI000", "RSN1148_KOCAELI_ARE090", "RSN1158_KOCAELI_DZC180", "RSN1602_DUZCE_BOL090", "RSN1633_MANJIL_ABBAR--T", "RSN1787_HECTOR_HEC090"
];

NM = [
  1.614, 0.916, 0.702, 1.055, 1.000, 1.495, 1.169, 0.795, 0.711, 0.926, 1.046
];

tn = 0.001 : 0.001 : 5;
tn_length = length(tn);
acceleration = zeros(length(filenames), tn_length);

for filename = 1 : length(filenames)
    [ag, time_interval, NPTS, errCode] = parseAT2('./PEERNGARecords_Unscaled/' + filenames(filename) + '.AT2');

    period = 0 : time_interval : (NPTS - 1) * time_interval;

    for index = 1 : tn_length

        [~, ~, a_array] = newmark_beta(ag, time_interval, 0.05, tn(index), 'average');

        acceleration(filename, index) = max(abs(a_array));

    end

    acceleration(filename, :) = acceleration(filename, :) * NM(filename);

end

median_acceleration = median(acceleration);

% 0.5 0.3 0.7 0.4
[sad, ~] = design_spectrum(ss_s1(1), ss_s1(2), 0.05, tn);
[sam, ~] = design_spectrum(ss_s1(3), ss_s1(4), 0.05, tn);

tol = 0.0001;

period_index = abs(tn - structure_period) < tol;

sa = median_acceleration(period_index);

fprintf('Sa: %.3f, SaD Factor: %.3f, SaM Factor: %.3f\n', sa, sad(period_index) / sa, sam(period_index) / sa);
fprintf("'%s': {'sa': %.3f},\n", [filenames; acceleration(:, period_index).']);
% fprintf('Records: %s, PGA: %.3f, PGA: %.3f\n', max(abs(ag)), acceleration(1));

green = [26 188 156] / 256;
blue = [52 152 219] / 256;
red = [233 88 73] / 256;
orange = [230 126 34] / 256;
gray = [0.5 0.5 0.5];
background = [247 247 247] / 256;

figure;
xlabel('T(sec)');
ylabel('Sa(g)');
hold on;

plot(tn, sad, 'Color', blue, 'LineWidth', 1.5);
plot(tn, sam, 'Color', green, 'LineWidth', 1.5);
plot(tn, median_acceleration, 'Color', red);
plot([tn(period_index) tn(period_index)], [0 sam(period_index)], '--', 'Color', gray, 'LineWidth', 1.5);

