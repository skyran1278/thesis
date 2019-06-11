function [capacity_sd, ap] = epa(config, load_pattern)

    % pushover curve
    [capacity_sd, capacity_sa] = config.load_pattern(load_pattern);

    % remove 0
    capacity_sd = capacity_sd(2:end);
    capacity_sa = capacity_sa(2:end);

    Teq = 2 * pi * sqrt(capacity_sd ./ (capacity_sa * 9806.65));

    Es0 = 1 / 2 * capacity_sd .* capacity_sa;

    ED = 8 * cumtrapz(capacity_sd, capacity_sa) - 4 * capacity_sd .* capacity_sa;

    beta_0 = 1 / (4 * pi) * ED ./ Es0;

    kappa = 1;

    beta_eff = kappa .* beta_0 + 5;

    beta_eff_length = length(beta_eff);
    Teq_length = length(Teq);

    ap = zeros(1, Teq_length);

    [SS, S1] = config.spectrum('DBE');

    for index = 1 : beta_eff_length
        [BS, B1] = damping_factor(beta_eff(index) / 100);

        T0 = S1 * BS / (SS * B1);

        T = Teq(index);

        if T <= 0.2 * T0
            ap(1, index) = capacity_sa(index) / (1 + (2.5 / BS - 1) * T / (0.2 * T0));

        elseif T > (0.2 * T0) && T <= T0
            ap(1, index) = BS / 2.5 * capacity_sa(index);

        else
            ap(1, index) = BS * Teq(index) / (2.5 * T0) * capacity_sa(index);

        end

    end

    capacity_sd = [0 capacity_sd];
    ap = [0 ap];

    green = [26 188 156] / 256;
    blue = [52 152 219] / 256;
    red = [233 88 73] / 256;
    orange = [230 126 34] / 256;
    gray = [0.5 0.5 0.5];
    background = [247 247 247] / 256;

    figure;
    hold on;
    title('EPA Curve');
    xlabel('Displacement(mm)');
    ylabel('Effective Peak Acceleration(g)');

    plot(capacity_sd, ap, 'DisplayName', 'EPA Curve', 'Color', green, 'LineWidth', 1.5,'Marker','o')
    plot(capacity_sd, [0 capacity_sa], 'DisplayName', 'Capacity Curve', 'Color', red, 'LineWidth', 1.5,'Marker','o')

    legend('show','Location','northwest');
    grid on;
    grid minor;

end


