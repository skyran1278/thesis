clc; clear; close all;

maxEQ = 30;
maxDL = 20;

beamLength = 10;

x = 0 : 0.01 : beamLength;
x_length = length(x);

midline = zeros(1, x_length);

EQ = -maxEQ + 2 * maxEQ / beamLength * x;
NEQ = -EQ;
DL = - maxDL / 3 + 4 * maxDL * (x / beamLength - 0.5) .^ 2;
DL12 = - maxDL * 2 / 3 + 4 * maxDL * (x / beamLength - 0.5) .^ 2;
DL8 = - maxDL + 4 * maxDL * (x / beamLength - 0.5) .^ 2;

% DL + EQ
negativeMn = EQ .* (EQ >= 0) + NEQ .* (NEQ >= 0) + 1.0 * DL .* (DL >= 0);
positiveMn = EQ .* (EQ <= 0) + NEQ .* (NEQ <= 0) + 1.0 * DL .* (DL <= 0);

topLeftRebar = max(negativeMn(x <= beamLength / 3));
topRightRebar = max(negativeMn(x >= beamLength / 3));

% �t�s�x�ݨD���u
topRebar = [topLeftRebar - topLeftRebar / (beamLength / 2) * x(x <= beamLength / 2), topRightRebar / (beamLength / 2) * x(x > beamLength / 2) - topRightRebar];

% ����
botLeftRebar = -min(positiveMn(x <= beamLength / 3));
botMidRebar = -min(positiveMn(x >= 1 * beamLength / 4 & x <= 3 * beamLength / 4));
botRightRebar = -min(positiveMn(x >= 2 * beamLength / 3));

botRebarDL = 4 * botMidRebar * (x / beamLength - 0.5) .^ 2 - botMidRebar;

botRebar = min([EQ; NEQ; botRebarDL]);
botRebarOtherMethod = [-botLeftRebar + (botLeftRebar - botMidRebar) / (beamLength / 2) * x(x <= beamLength / 2), -botMidRebar + (botMidRebar - botRightRebar) / (beamLength / 2) * (x(x > beamLength / 2) - (beamLength / 2)) ];

% bot = - botMidRebar * ones(1, x_length);

greenColor = [26 188 156] / 256;
blueColor = [52 152 219] / 256;
redColor = [233 88 73] / 256;
grayColor = [0.5 0.5 0.5];
bgColor = [247 247 247] / 256;

% ���O�B�a�_�O����ڻݨD
% 1
figure;
plot(x, midline, 'Color', grayColor, 'LineWidth', 1.75);
hold on;
plot(x, EQ, '-', 'Color', greenColor, 'LineWidth', 1.75);
legendEQ = plot(x, NEQ, '-', 'Color', greenColor, 'LineWidth', 1.75);
legendGravity = plot(x, DL, '--', 'Color', greenColor, 'LineWidth', 1.75);
axis([0 beamLength -50 50]);
legend([legendEQ, legendGravity], 'EQ', 'Gravity', 'Location', 'northeast');
title('Mn');
xlabel('m');
ylabel('tf-m');

% �u���|�[
% 2
figure;
plot(x, midline, 'Color', grayColor, 'LineWidth', 1.75);
hold on;
plot(x, EQ, 'Color', grayColor, 'LineWidth', 1.75);
legendEQ = plot(x, NEQ, 'Color', grayColor, 'LineWidth', 1.75);
legendGravity = plot(x, DL, 'Color', grayColor, 'LineWidth', 1.75);
legendMn = plot(x, positiveMn, 'Color', greenColor, 'LineWidth', 1.75);
plot(x, negativeMn, 'Color', greenColor, 'LineWidth', 1.75);
axis([0 beamLength -50 50]);
legend([legendEQ, legendGravity, legendMn], 'EQ', 'Gravity', 'Linear Add', 'Location', 'northeast');
title('Mn');
xlabel('m');
ylabel('tf-m');

% ���ݬ� 0~1/3 ���̤j��
% �����O 1/4~3/4 ���̤j��
% �k�ݬO 2/3~1 ���̤j��
% 3
figure;
plot(x, midline, '-k');
hold on;
plot(x, EQ, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, NEQ, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, DL, 'Color', grayColor, 'LineWidth', 1.75);
legendMn = plot(x, positiveMn, 'Color', greenColor, 'LineWidth', 1.75);
plot(x, negativeMn, 'Color', greenColor, 'LineWidth', 1.75);
legendActural = plot(0, topLeftRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(beamLength / 2, 0, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(beamLength, topRightRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(0, -botLeftRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(beamLength / 2, -botMidRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(beamLength, -botRightRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
axis([0 beamLength -50 50]);
legend([legendActural, legendMn(1)], 'Actural Rebar', 'Demand', 'Location', 'northeast');
title('Mn');
xlabel('m');
ylabel('tf-m');

% ��ڰt�����ӷ|�A�j�@�I
% �ӥB�ַ̤|����䪺����
% �o�̨��� critical �����p
% 4
figure;
plot(x, midline, '-k');
hold on;
plot(x, EQ, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, NEQ, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, DL, 'Color', grayColor, 'LineWidth', 1.75);
legendMn = plot(x, positiveMn, 'Color', greenColor, 'LineWidth', 1.75);
plot(x, negativeMn, 'Color', greenColor, 'LineWidth', 1.75);
legendActural = plot(0, topLeftRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(beamLength / 2, 10, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(beamLength, topRightRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(0, -botLeftRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(beamLength / 2, -botMidRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(beamLength, -botRightRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
axis([0 beamLength -50 50]);
legend([legendActural, legendMn(1)], 'Actural Rebar', 'Demand', 'Location', 'northeast');
title('Mn');
xlabel('m');
ylabel('tf-m');

% �A�ӴN�O�̾ڲ{���t���̾ڻݨD���u���u��
% �����O�W�h��������
% �����S���ݨD
% ��ݥD�n�ѭ@�_����
% �ڭ̴N�����Ԫ�
% 5
figure;
plot(x, midline, '-k');
hold on;
plot(x, EQ, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, NEQ, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, DL, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, positiveMn, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, negativeMn, 'Color', greenColor, 'LineWidth', 1.75);
plot(x, topRebar, 'Color', blueColor, 'LineWidth', 1.75);
plot(0, topLeftRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(beamLength / 2, 10, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(beamLength, topRightRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(0, -botLeftRebar, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(beamLength / 2, -botMidRebar, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(beamLength, -botRightRebar, 'o', 'Color', grayColor, 'LineWidth', 1.75);
axis([0 beamLength -50 50]);
title('Mn');
xlabel('m');
ylabel('tf-m');

% ���U�ӬO�U�h��������
% �o�����N��������F
% ���k��ݥѭ@�_����
% �����ڭ̭쥻�w���O�ѭ��O����
% ��ӯu���U�h�����ɭԵo�{�|���a�_�O���]�������i�ӤF
% �p�G�����̷ӭ��O�A��ݨ̾ڦa�_�O���j�ȷ|�p�k���Ŧ⪺�u
% 6
figure;
plot(x, midline, '-k');
hold on;
plot(x, EQ, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, NEQ, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, DL, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, positiveMn, 'Color', greenColor, 'LineWidth', 1.75);
plot(x, negativeMn, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, botRebar, 'Color', blueColor, 'LineWidth', 1.75);
plot(0, topLeftRebar, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(beamLength / 2, 10, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(beamLength, topRightRebar, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(0, -botLeftRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(beamLength / 2, -botMidRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(beamLength, -botRightRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
axis([0 beamLength -50 50]);
title('Mn');
xlabel('m');
ylabel('tf-m');

% �i�H�o�{�Ŧ⪺�����ۤ���ڻݨD�h���F
% �Ӻ�ⳡ�������O�u
% 7
figure;
plot(x, midline, '-k');
hold on;
enoughRebar = positiveMn - botRebar > 0;
notEnoughRebar = positiveMn - botRebar < 0;
fill([x(enoughRebar) x(enoughRebar)], [botRebar(enoughRebar) positiveMn(enoughRebar)], blueColor, 'edgeColor', blueColor)
fill([x(notEnoughRebar) x(notEnoughRebar)], [botRebar(notEnoughRebar) positiveMn(notEnoughRebar)], greenColor, 'edgeColor', 'none')
plot(x, EQ, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, NEQ, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, DL, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, positiveMn, 'Color', greenColor, 'LineWidth', 1.75);
plot(x, negativeMn, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, botRebar, 'Color', blueColor, 'LineWidth', 1.75);
plot(0, topLeftRebar, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(beamLength / 2, 10, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(beamLength, topRightRebar, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(0, -botLeftRebar, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(beamLength / 2, -botMidRebar, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(beamLength, -botRightRebar, 'o', 'Color', grayColor, 'LineWidth', 1.75);
axis([0 beamLength -50 50]);
title('Mn');
xlabel('m');
ylabel('tf-m');

% �Ӧp�G�ڭ̪����Ԫ��u
% �įq�|�U��
% �q���� 25% ���įq�U���� 17%
% �Ӧp�G�Ҽ{�������ר��Ĳv�ٷ|�i�@�B�U��
% �������סG6% 3%
% �S�������G25% 17%
% 8
figure;
plot(x, midline, '-k');
hold on;
plot(x, EQ, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, NEQ, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, DL, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, positiveMn, 'Color', greenColor, 'LineWidth', 1.75);
plot(x, negativeMn, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, botRebarOtherMethod, 'Color', blueColor, 'LineWidth', 1.75);
plot(0, topLeftRebar, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(beamLength / 2, 10, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(beamLength, topRightRebar, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(0, -botLeftRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(beamLength / 2, -botMidRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(beamLength, -botRightRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
axis([0 beamLength -50 50]);
title('Mn');
xlabel('m');
ylabel('tf-m');

% �ڭ̼Ȱ��@�U
% �`���@�U�Ҧ�������
% ��⪺�u�O�a�_�O�[�W���O���ݨD
% �Ŧ⪺�O�ڭ̪��t��k
% �����ڭ̨õL�k�����{�b������
% �o�˥u�� 3% ���Ĳv
% �p�G�Q�n�q�{���t���N���ܦn���ĪG���� ( �p�G�w�g���Ͱt�����F)
% ���ڭ̴N�|�ݭn��h�����
% 9
figure;
plot(x, midline, '-k');
hold on;
plot(x, EQ, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, NEQ, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, DL, 'Color', grayColor, 'LineWidth', 1.75);
legendMn = plot(x, positiveMn, 'Color', greenColor, 'LineWidth', 1.75);
plot(x, negativeMn, 'Color', greenColor, 'LineWidth', 1.75);
plot(x, topRebar, 'Color', blueColor, 'LineWidth', 1.75);
lengendMultiRebar = plot(x, botRebarOtherMethod, 'Color', blueColor, 'LineWidth', 1.75);
axis([0 beamLength -50 50]);
legend([legendMn, lengendMultiRebar], 'Demand', 'Multi Rebar', 'Location', 'southeast');
title('Mn');
xlabel('m');
ylabel('tf-m');

% ���O �p�G�ڭ̪��D�o�����O���u����
% �A�[�W�|�Ӱt���I
% �����ܦh���u�N�i�H�f���X�ӤF
% 10
figure;
plot(x, midline, '-k');
hold on;
% plot(x, EQ, 'Color', grayColor, 'LineWidth', 1.75);
% plot(x, NEQ, 'Color', grayColor, 'LineWidth', 1.75);
plot(x, DL, 'Color', greenColor, 'LineWidth', 1.75);
% plot(x, positiveMn, 'Color', grayColor, 'LineWidth', 1.75);
% plot(x, negativeMn, 'Color', grayColor, 'LineWidth', 1.75);
plot(0, topLeftRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
% plot(beamLength / 2, 10, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(beamLength, topRightRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(0, -botLeftRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
% plot(beamLength / 2, -botMidRebar, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(beamLength, -botRightRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
axis([0 beamLength -50 50]);
title('Mn');
xlabel('m');
ylabel('tf-m');

% �H�W�h������
% �t���I �V ���O = �a�_�O
% �U�h���N�����O�a�_�O
% �ҥH�a�_�O�M���O�N�X�ӤF
% ���N�i�H�^��e�������u
% �ڭ̴N�i�H���� match �ݨD�F
% 11
figure;
plot(x, midline, '-k');
hold on;
plot(x, DL, 'Color', greenColor, 'LineWidth', 1.75);
plot(x, positiveMn - 1, 'Color', redColor, 'LineWidth', 1.75);
plot(x, negativeMn + 1, 'Color', redColor, 'LineWidth', 1.75);
plot(0, topLeftRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
% plot(beamLength / 2, 10, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(beamLength, topRightRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(0, -botLeftRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
% plot(beamLength / 2, -botMidRebar, 'o', 'Color', grayColor, 'LineWidth', 1.75);
plot(beamLength, -botRightRebar, 'o', 'Color', greenColor, 'LineWidth', 1.75);
plot(x, EQ, 'Color', blueColor, 'LineWidth', 1.75);
plot(x, NEQ, 'Color', blueColor, 'LineWidth', 1.75);
axis([0 beamLength -50 50]);
title('Mn');
xlabel('m');
ylabel('tf-m');

% �H�W�h������
% �t���I �V ���O = �a�_�O
% �U�h���N�����O�a�_�O
% �ҥH�a�_�O�M���O�N�X�ӤF
% ���N�i�H�^��e�������u
% �ڭ̴N�i�H���� match �ݨD�F
% 12
figure;
subplot(3, 1, 1);
plot(x, midline, '-k');
hold on;
plot(x, DL, 'Color', greenColor, 'LineWidth', 1.75);
axis([0 beamLength -30 20]);
subplot(3, 1, 2);
plot(x, midline, '-k');
hold on;
plot(x, DL12, 'Color', greenColor, 'LineWidth', 1.75);
axis([0 beamLength -30 20]);
subplot(3, 1, 3);
plot(x, midline, '-k');
hold on;
plot(x, DL8, 'Color', greenColor, 'LineWidth', 1.75);
axis([0 beamLength -30 20]);

% figure;
% plot(x, midline, '-k');
% hold on;
% legendEQ = plot(x, EQ, '-k', x, NEQ, '-k');
% legendGravity = plot(x, DL, '-k');
% legendMn = plot(x, negativeMn, '-r', x, positiveMn, '-r');
% % % plot(x, botRebarDL, '--b');
% % % plot(x, bot, '--g');
% % plot(x, topRebar, '-b');
% % plot(x, botRebar, '-b');
% % plot(x, botRebarOtherMethod, '-g');

% plot(0, topLeftRebar, 'or');
% plot(beamLength / 2, 0, 'or');
% plot(beamLength, topRightRebar, 'or');
% plot(0, -botLeftRebar, 'or');
% plot(beamLength / 2, -botMidRebar, 'or');
% plot(beamLength, -botRightRebar, 'or');
% axis([0 beamLength -50 50]);
% legend([legendEQ(1), legendGravity, legendMn(1)], 'EQ', 'Gravity', 'Linear Add', 'Location', 'northeast');
% title('Mn');
% xlabel('m');
% ylabel('tf-m');
