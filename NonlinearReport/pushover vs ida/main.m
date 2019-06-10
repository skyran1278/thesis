clc; clear; close all;

config = Config;

scaled_factor = [0.01, 0.1, 0.297, 0.396, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 2, 2.5];

sas = [
    0.480, 0.414, 0.635, 0.348, 0.283, 0.488, 0.132, 0.326, 0.738, 0.480, 0.439
];

filenames = [
    "RSN725_SUPER.B_B-POE360", "RSN900_LANDERS_YER270", "RSN953_NORTHR_MUL279", "RSN960_NORTHR_LOS000", "RSN1111_KOBE_NIS000", "RSN1116_KOBE_SHI000", "RSN1148_KOCAELI_ARE090", "RSN1158_KOCAELI_DZC180", "RSN1602_DUZCE_BOL090", "RSN1633_MANJIL_ABBAR--T", "RSN1787_HECTOR_HEC090"
];

sd = NaN(length(filenames), length(scaled_factor));
sa = NaN(1, length(scaled_factor));

for index = 1 : length(scaled_factor)
    for filename = 1 : length(filenames)
        config.filename = filenames(filename);
        [sd(filename, index), ~] = procedure_b(config, 'inverted_triangle', scaled_factor(index) / sas(index));
        sa(1, index) = scaled_factor(index);
    end
end

interp_sd = NaN(length(filenames), length(sa));

median_sd = nanmedian(sd);

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
plot(median_sd, sa, 'DisplayName', 'Elastic', 'Color', green, 'LineWidth', 1.5);
fprintf('        [%.3f, %.3f],\n', [median_sd; sa]);
