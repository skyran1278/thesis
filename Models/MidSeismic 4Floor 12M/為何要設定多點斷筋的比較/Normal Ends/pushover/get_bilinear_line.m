function [bilinear_sd, bilinear_sa] = get_bilinear_line(elastic_sd, elastic_sa, dy, ay, d_star, a_star, capacity_sd)
    bilinear_sd = [elastic_sd(1), dy, d_star, capacity_sd(end)];
    bilinear_sa_end = linear_interpolate(capacity_sd(end), dy, d_star, ay, a_star);
    bilinear_sa = [elastic_sa(1), ay, a_star, bilinear_sa_end];
end
