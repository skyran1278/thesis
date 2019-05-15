function [sd, sa] = procedure_b(config, load_pattern, spectrum)
%
% Procedure B assumes ay, dy and the post-yield slope remains constant that is not made in the other two procedures.
% Procedure A have to judge equal-acceleration or equal-velocity, so not applicable to real time history.
% Procedure C most convenient for hand analysis.
%
% @since 1.0.0
% @param {object} [config] description.
% @return {type} [load_pattern] description.
% @return {type} [scaled_factor] description.
% @see dependencies
%

    sd = NaN;
    sa = NaN;

    green = [26 188 156] / 256;
    blue = [52 152 219] / 256;
    red = [233 88 73] / 256;
    orange = [230 126 34] / 256;
    gray = [0.5 0.5 0.5];
    background = [247 247 247] / 256;

    % pushover curve
    [capacity_sd, capacity_sa] = config.load_pattern(load_pattern);

    % elastic line
    [elastic_sd, elastic_sa] = get_elastic_line(capacity_sd, capacity_sa);

    [ss, s1] = config.spectrum(spectrum);

    % 5% spectrum
    [demand_sd, demand_sa] = design_spectrum(ss, s1, 0.05, 0.001:0.01:2);

    % get elastic intersection with 5% spectrum
    % and get vertical line intersection with pushover curve on d_star, a_star
    [d_star, a_star] = get_star_point(elastic_sd, elastic_sa, capacity_sd, capacity_sa, demand_sd, demand_sa);

    % use equal area to get yielding point
    [dy, ay] = get_yielding_point(elastic_sd, elastic_sa, capacity_sd, capacity_sa, d_star, a_star);

    % build bilinear curve
    [bilinear_sd, bilinear_sa] = get_bilinear_line(elastic_sd, elastic_sa, dy, ay, d_star, a_star, capacity_sd);

    % use bilinear curve get beta_eff, dpi
    [beta_eff, dpi] = get_beff_and_dpi(min(max(demand_sd), max(capacity_sd)), d_star, a_star, dy, ay, config.structural_behavior_type);

    % use beta_eff, dpi get sd, sa on figure
    [single_demand_sd, single_demand_sa] = get_single_demand(config, beta_eff, dpi, spectrum);

    % single demand curve intersection with bilinear curve to get performance point
    [sd, sa] = get_performance_point(single_demand_sd, single_demand_sa, bilinear_sd, bilinear_sa);

    figure;
    hold on;
    title('ADRS');
    xlabel('sd(mm)');
    ylabel('sa(g)');
    axis([0 max(capacity_sd) 0 inf]);
    plot(elastic_sd, elastic_sa, 'DisplayName', 'Elastic', 'Color', gray, 'LineWidth', 1.5);
    plot(bilinear_sd, bilinear_sa, 'DisplayName', 'Bilinear', 'Color', gray, 'LineWidth', 1.5);
    plot(capacity_sd, capacity_sa, 'DisplayName', 'Capacity', 'Color', green, 'LineWidth', 1.5);
    plot(demand_sd, demand_sa, 'DisplayName', 'Demand', 'Color', blue, 'LineWidth', 1.5);
    plot(single_demand_sd, single_demand_sa, 'DisplayName', 'Single Demand', 'Color', red, 'LineWidth', 1.5);
    plot(d_star, a_star, 'o', 'DisplayName', '(d*, a*)', 'Color', green);
    plot(dy, ay, 'o', 'DisplayName', '(dy, ay)', 'Color', gray);
    plot(sd, sa, 'o', 'DisplayName', 'Performance Point', 'Color', red);
    text(sd * 1.1, sa, ['(', num2str(sd), ', ', num2str(sa), ')'], 'Color', red)
    legend('show')

end

function [d_star, a_star] = get_star_point(elastic_sd, elastic_sa, capacity_sd, capacity_sa, demand_sd, demand_sa)
    d_star = NaN;
    a_star = NaN;

    point_temp = InterX([elastic_sd; elastic_sa], [demand_sd; demand_sa]);

    if size(point_temp, 2) == 1

        point_star = InterX([capacity_sd; capacity_sa], [[point_temp(1, :), point_temp(1, :)]; [0, point_temp(2, :)]]);

        d_star = point_star(1, :);
        a_star = point_star(2, :);

        if size(point_star, 2) ~= 1
            fprintf('star point not only 1 intersection.\n')
        end

    elseif isempty(point_temp)
        fprintf('Without star point\n');

    else
        fprintf('star point not only 1 intersection.\n')

    end

end

function [beta_eff, dpi] = get_beff_and_dpi(max_sd, d_star, a_star, dy, ay, structural_behavior_type)
    % dpi have to intersection with demand curve, so choose max demand curve 5%
    % but if damand curve too large, limit in max pushover curve is reasonable
    dpi = dy : 0.1 : max_sd; % matrix

    api = linear_interpolate(dpi, dy, d_star, ay, a_star); % matrix

    beta_0 = 63.7 * (ay * dpi - dy * api) ./ (api .* dpi); % matrix

    if structural_behavior_type == 'A'
        kappa = get_kappa(beta_0, dpi, api, dy, ay);
    end

    beta_eff = kappa .* beta_0 + 5;

end

function kappa = get_kappa(beta_0, dpi, api, dy, ay)
    beta_0_length = length(beta_0);

    kappa = zeros(1, beta_0_length);

    for index = 1 : beta_0_length

        if beta_0(index) <= 16.5
            kappa(index) = 1.0;
        else
            kappa(index) = 1.13 - 0.51 * (ay * dpi(index) - dy * api(index)) / (api(index) * dpi(index));
        end

    end

end

function [sd, sa] = get_single_demand(config, beta_eff, dpi, spectrum)
    beta_eff_length = length(beta_eff);

    sd = NaN(1, beta_eff_length);
    sa = NaN(1, beta_eff_length);

    for index = 1 : beta_eff_length
        [ss, s1] = config.spectrum(spectrum);

        [demand_sd, demand_sa] = design_spectrum(ss, s1, beta_eff(index) / 100, 0.001:0.01:5);

        single_demand = InterX([demand_sd; demand_sa], [[dpi(index), dpi(index)]; [0, max(demand_sa)]]);

        if ~isempty(single_demand)
            % may be multi intersection, so select max sa
            sd(index) = max(single_demand(1, :));
            sa(index) = max(single_demand(2, :));
        end

    end

end

function [sd, sa] = get_performance_point(single_demand_sd, single_demand_sa, bilinear_sd, bilinear_sa)
    sd = NaN;
    sa = NaN;

    point_temp = InterX([single_demand_sd; single_demand_sa], [bilinear_sd; bilinear_sa]);

    if size(point_temp, 2) == 1
        sd = point_temp(1, :);
        sa = point_temp(2, :);

    elseif isempty(point_temp)
        fprintf('Without Performance Point.\n');

    else
        fprintf('Performance Point not only 1 intersection.\n');
        sd = point_temp(1, :);
        sa = point_temp(2, :);
    end

end
