function [elastic_sd, elastic_sa] = get_elastic_line(capacity_sd, capacity_sa)
    elastic_sd = [capacity_sd(1), capacity_sd(2), capacity_sd(end)];
    elastic_sa_end = linear_interpolate(capacity_sd(end), capacity_sd(1), capacity_sd(2), capacity_sa(1), capacity_sa(2));
    elastic_sa = [capacity_sa(1), capacity_sa(2), elastic_sa_end];
end
