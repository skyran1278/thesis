function [sd, sa] = design_spectrum(SS, S1, damping_ratio, tn)
%
% description.
%
% @since 1.0.0
% @param {number} [SS] description.
% @param {number} [S1] description.
% @param {number} [damping_ratio] description.
% @param {array} [tn] description.
% @return {array} [sd] unit:mm.
% @return {array} [sa] unit:g.
% @see dependencies
%

    [BS, B1] = damping_factor(damping_ratio);

    T0 = S1 * BS / (SS * B1);

    tn_length = length(tn);
    sa = zeros(1, tn_length);

    for index = 1 : tn_length
        T = tn(index);

        if T <= 0.2 * T0
            sa(1, index) = SS * (0.4 + (1 / BS - 0.4) * T / (0.2 * T0));

        elseif T > (0.2 * T0) && T <= T0
            sa(1, index) = SS / BS;

        elseif T > T0 && T <= 2.5 * T0
            sa(1, index) = S1 / (B1 * T);

        else
            sa(1, index) = 0.4 * SS / BS;

        end
    end

    sd = period_to_sd(tn, sa);

end

function sd = period_to_sd(period, acceleration)
    sd = (period .^ 2) / (4 * pi ^ 2) .* acceleration * 9806.65;
end
