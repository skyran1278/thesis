function y = linear_interpolate(x, x1, x2, y1, y2)
    y = (y2 - y1) / (x2 - x1) * (x - x1) + y1;
end
