clc; clear; close all;

config = Config;

scaled_factor = 0.01 : 0.2 : 3;

scaled_factor_length = length(scaled_factor);

filenames = [
    "RSN725_SUPER.B_B-POE360", "RSN900_LANDERS_YER270", "RSN953_NORTHR_MUL279", "RSN960_NORTHR_LOS000", "RSN1111_KOBE_NIS000", "RSN1116_KOBE_SHI000", "RSN1148_KOCAELI_ARE090", "RSN1158_KOCAELI_DZC180", "RSN1602_DUZCE_BOL090", "RSN1633_MANJIL_ABBAR--T", "RSN1787_HECTOR_HEC090"
];

sd = NaN(11, scaled_factor_length);
sa = NaN(11, scaled_factor_length);

for index = 1 : scaled_factor_length
    for filename = 1 : length(filenames)
        config.filename = filenames(filename);
        [sd(filename, index), sa(filename, index)] = procedure_b(config, 'inverted_triangle', scaled_factor(index));
    end
end

median_sd = nanmedian(sd);
median_sa = nanmedian(sa);

for

median_sa = interp1(sa, sd,0:0.01: 0.5)

green = [26 188 156] / 256;
blue = [52 152 219] / 256;
red = [233 88 73] / 256;
orange = [230 126 34] / 256;
gray = [0.5 0.5 0.5];
background = [247 247 247] / 256;

figure;
hold on;
title('ADRS');
xlabel('sd(mm)');
ylabel('sa(g)');
plot(sd.', sa.', 'DisplayName', 'Elastic', 'Color', gray, 'LineWidth', 1.5);
plot(median_sd, median_sa, 'DisplayName', 'Elastic', 'Color', green, 'LineWidth', 1.5);
fprintf('        [%.3f, %.3f],\n', [sd; sa]);
% plot(sd_uniform, sa_uniform, 'DisplayName', 'Elastic', 'Color', blue, 'LineWidth', 1.5);
% plot(sd_power, sa_power, 'DisplayName', 'Elastic', 'Color', red, 'LineWidth', 1.5);
% plot(sd, scaled_factor * sa, 'DisplayName', 'Elastic', 'Color', green, 'LineWidth', 1.5);
% plot(sd_uniform, scaled_factor * sa, 'DisplayName', 'Elastic', 'Color', blue, 'LineWidth', 1.5);
% plot(sd_power, scaled_factor * sa, 'DisplayName', 'Elastic', 'Color', red, 'LineWidth', 1.5);

% figure;
% hold on;
% title('ADRS');
% xlabel('Roof Displacement(mm)');
% ylabel('sa(g)');
% plot(sd_triangle * PF1_phi, scaled_factor * sa, 'DisplayName', 'Elastic', 'Color', green, 'LineWidth', 1.5);
% plot(sd_uniform * PF1_phi, scaled_factor * sa, 'DisplayName', 'Elastic', 'Color', blue, 'LineWidth', 1.5);
% plot(sd_power * PF1_phi, scaled_factor * sa, 'DisplayName', 'Elastic', 'Color', red, 'LineWidth', 1.5);

% save('pushover_v2.mat')
