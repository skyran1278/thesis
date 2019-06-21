clc; clear; close all;

maxEQ = 10;
maxDL = 40;

beamLength = 12;

x = 0 : 0.01 : beamLength;
x_length = length(x);

midline = zeros(1, x_length);

EQ = -maxEQ + 2 * maxEQ / beamLength * x;
NEQ = -EQ;
DL = - maxDL / 3 + 4 * maxDL * (x / beamLength - 0.5) .^ 2;
% DL12 = - maxDL * 2 / 3 + 4 * maxDL * (x / beamLength - 0.5) .^ 2;
% DL8 = - maxDL + 4 * maxDL * (x / beamLength - 0.5) .^ 2;

% DL + EQ
negativeMn = EQ .* (EQ >= 0) + NEQ .* (NEQ >= 0) + 1.0 * DL;
% positiveMn = EQ .* (EQ <= 0) + NEQ .* (NEQ <= 0) + 1.0 * DL;

% topLeftRebar = max(negativeMn(x <= beamLength / 3));
% topRightRebar = max(negativeMn(x >= beamLength / 3));

% topRebar = [topLeftRebar - topLeftRebar / (beamLength / 2) * x(x <= beamLength / 2), topRightRebar / (beamLength / 2) * x(x > beamLength / 2) - topRightRebar];

% botLeftRebar = -min(positiveMn(x <= beamLength / 3));
% botMidRebar = -min(positiveMn(x >= 1 * beamLength / 4 & x <= 3 * beamLength / 4));
% botRightRebar = -min(positiveMn(x >= 2 * beamLength / 3));

% botRebarDL = 4 * botMidRebar * (x / beamLength - 0.5) .^ 2 - botMidRebar;

% botRebar = min([EQ; NEQ; botRebarDL]);
% botRebarOtherMethod = [-botLeftRebar + (botLeftRebar - botMidRebar) / (beamLength / 2) * x(x <= beamLength / 2), -botMidRebar + (botMidRebar - botRightRebar) / (beamLength / 2) * (x(x > beamLength / 2) - (beamLength / 2)) ];

greenColor = [26 188 156] / 256;
blueColor = [52 152 219] / 256;
redColor = [233 88 73] / 256;
grayColor = [0.5 0.5 0.5];
bgColor = [247 247 247] / 256;

figure;
hold on;
plot(x, EQ .* (EQ >= 0), 'Color', redColor, 'LineWidth', 2);
legendEQ = plot(x, NEQ .* (NEQ >= 0), 'Color', redColor, 'LineWidth', 2);
legendGravity = plot(x, DL, 'Color', greenColor, 'LineWidth', 2);
legendMn = plot(x, negativeMn .* (negativeMn >= 0), 'Color', blueColor, 'LineWidth', 2);
plot(x, midline, 'Color', grayColor, 'LineWidth', 2);
legend([legendEQ, legendGravity, legendMn], 'Lateral Load', 'Gravity Load', 'Combined Load', 'Location', 'best');
title('Moment Diagram');
xlabel('Length (m)');
ylabel('Moment (ton-m)');
grid on;
grid minor;
axis([0 inf -20 40]);

maxEQ = 30;
maxDL = 10;

beamLength = 12;

x = 0 : 0.01 : beamLength;
x_length = length(x);

midline = zeros(1, x_length);

EQ = -maxEQ + 2 * maxEQ / beamLength * x;
NEQ = -EQ;
DL = - maxDL / 3 + 4 * maxDL * (x / beamLength - 0.5) .^ 2;


% DL + EQ
negativeMn = EQ .* (EQ >= 0) + NEQ .* (NEQ >= 0) + 1.0 * DL;

figure;
hold on;
plot(x, EQ .* (EQ >= 0), 'Color', redColor, 'LineWidth', 2);
legendEQ = plot(x, NEQ .* (NEQ >= 0), 'Color', redColor, 'LineWidth', 2);
legendGravity = plot(x, DL, 'Color', greenColor, 'LineWidth', 2);
legendMn = plot(x, negativeMn .* (negativeMn >= 0), 'Color', blueColor, 'LineWidth', 2);
plot(x, midline, 'Color', grayColor, 'LineWidth', 2);
legend([legendEQ, legendGravity, legendMn], 'Lateral Load', 'Gravity Load', 'Combined Load', 'Location', 'best');
title('Moment Diagram');
xlabel('Length (m)');
ylabel('Moment (ton-m)');
grid on;
grid minor;
axis([0 inf -20 40]);
