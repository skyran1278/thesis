function [dy, sdd, sdm] = evalution(config, load_pattern, multi)
%
% description.
%
% @since 1.0.0
% @param {type} [name] description.
% @return {type} [name] description.
% @see dependencies
%
    green = [26 188 156] / 256;
    blue = [52 152 219] / 256;
    red = [233 88 73] / 256;
    orange = [230 126 34] / 256;
    gray = [0.5 0.5 0.5];
    background = [247 247 247] / 256;

    [sdd, sad] = procedure_b(config, load_pattern, 'DBE', true);
    [sdm, sam] = procedure_b(config, load_pattern, 'MCE', true);

    % pushover parameter PF and effective_mass
    [PF, effective_mass] = config.parameter(load_pattern);

    % pushover curve
    [capacity_sd, capacity_sa] = config.load_pattern(load_pattern);

    % elastic line
    [elastic_sd, elastic_sa] = get_elastic_line(capacity_sd, capacity_sa);

    % max sa
    [max_sa, max_sa_index] = max(capacity_sa);

    % max sd
    max_sd = capacity_sd(max_sa_index);

    % use equal area to get yielding point
    [dy, ay] = get_yielding_point(elastic_sd, elastic_sa, capacity_sd, capacity_sa, max_sd, max_sa);

    % build bilinear curve
    [bilinear_sd, bilinear_sa] = get_bilinear_line(elastic_sd, elastic_sa, dy, ay, max_sd, max_sa, capacity_sd);

    Ra = sdd / dy;
    R = sdm / dy;

    % sd => roof displacement
    capacity_sd = PF * capacity_sd;
    bilinear_sd = PF * bilinear_sd;
    dy = PF * dy;
    sdd = PF * sdd;
    sdm = PF * sdm;

    % sa => base shear
    capacity_sa = effective_mass * capacity_sa;
    bilinear_sa = effective_mass * bilinear_sa;
    ay = effective_mass * ay;
    sad = effective_mass * sad;
    sam = effective_mass * sam;

    figure;
    if multi == "multi"
        % figure('Position', [10 10 640 860]);
        % subplot(2, 1, 1);
        % title('(a) Multi-Cut');
        title('Optimization');
    else
        % subplot(2, 1, 2);
        % title('(b) Tradition');
        title('Tradition');
    end

    hold on;
    xlabel('Displacement (mm)');
    ylabel('Base Shear (tonf)');
    plot(bilinear_sd, bilinear_sa, 'DisplayName', 'Bilinear', 'Color', gray, 'LineWidth', 1.5);
    plot(capacity_sd, capacity_sa, 'DisplayName', 'Capacity', 'Color', green, 'LineWidth', 1.5);
    plot(dy, ay, 'o', 'DisplayName', 'Yielding Point', 'Color', gray);
    plot(sdd, sad, 'o', 'DisplayName', '475 Performance Point', 'Color', blue);
    plot(sdm, sam, 'o', 'DisplayName', '2500 Performance Point', 'Color', red);
    text(dy * 1.1, ay, sprintf('Yielding Point: %.1fmm', dy), 'Color', gray);
    text(sdd * 1.1, sad, sprintf('475 Performance Point: %.1fmm', sdd), 'Color', blue);
    text(sdm * 1.1, sam, sprintf('2500 Performance Point: %.1fmm', sdm), 'Color', red);
    legend('show','Location','southeast');
    grid on;
    grid minor;

    fprintf('%s\n', load_pattern);
    fprintf('Ra=%.2f\n', Ra);
    fprintf('R=%.2f\n', R);
    fprintf('\n');

end
