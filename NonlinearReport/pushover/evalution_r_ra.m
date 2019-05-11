function output = evalution_r_ra(config, load_pattern)
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

    [sdd, sad] = procedure_b(config, load_pattern, 'DBE');
    [sdm, sam] = procedure_b(config, load_pattern, 'MCE');

    % pushover curve
    [capacity_sd, capacity_sa] = config.load_pattern(load_pattern);

    % elastic line
    [elastic_sd, elastic_sa] = get_elastic_line(capacity_sd, capacity_sa);

    [max_sa, max_sa_index] = max(capacity_sa);

    max_sd = capacity_sd(max_sa_index);

    % use equal area to get yielding point
    [dy, ay] = get_yielding_point(elastic_sd, elastic_sa, capacity_sd, capacity_sa, max_sd, max_sa);

    % build bilinear curve
    [bilinear_sd, bilinear_sa] = get_bilinear_line(elastic_sd, elastic_sa, dy, ay, max_sd, max_sa, capacity_sd);

    Ra = sdd / dy
    R = sdm / dy

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

    % function [dy, ay] = get_yielding_point(config, load_pattern)
    %     bilinear_area = 0;

    %     % pushover curve
    %     [capacity_sd, capacity_sa] = config.load_pattern(load_pattern);

    %     [max_sa, max_sa_index] = max(capacity_sa);

    %     max_sd = capacity_sd(max_sa_index);

    %     [elastic_sd, elastic_sa] = get_elastic_line(capacity_sd, capacity_sa);

    %     dy = elastic_sd(1);
    %     ay = elastic_sa(1);

    %     capacity_area = trapz([capacity_sd(capacity_sd < max_sd), max_sd], [capacity_sa(capacity_sd < max_sd), max_sa]);

    %     while abs(bilinear_area - capacity_area) > 1e-4
    %         dy = dy + 1e-4;
    %         ay = linear_interpolate(dy, elastic_sd(1), elastic_sd(2), elastic_sa(1), elastic_sa(2));

    %         bilinear_area = trapz([elastic_sd(1), dy, max_sd], [elastic_sa(1), ay, max_sa]);
    %     end
    % end

end
