function [dy, ay] = get_yielding_point(elastic_sd, elastic_sa, capacity_sd, capacity_sa, d_star, a_star)
    bilinear_area = 0;
    dy = elastic_sd(1);
    ay = elastic_sa(1);

    capacity_area = trapz([capacity_sd(capacity_sd < d_star), d_star], [capacity_sa(capacity_sd < d_star), a_star]);

    while abs(bilinear_area - capacity_area) > 1e-2
        dy = dy + 1e-4;
        ay = linear_interpolate(dy, elastic_sd(1), elastic_sd(2), elastic_sa(1), elastic_sa(2));

        bilinear_area = trapz([elastic_sd(1), dy, d_star], [elastic_sa(1), ay, a_star]);
    end
end
