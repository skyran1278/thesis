classdef Config

    properties
        structural_behavior_type = 'A';

        SDS_SD1 = [0.66, 0.49];
        SMS_SM1 = [0.8, 0.54];

        PF = [
            1.279, 1.187, 1.065
        ];

        effective_mass = [
            1742, 228, 83
        ];

        % roof displacement(mm), V(tonf)
        mmc = [
            0	0
            -40	1.0322
            -44.696	1.1533
            -95.618	1.8041
            -108.375	1.9343
            -153.701	2.1918
            -189.495	2.3105
            -211.982	2.3462
            -211.985	1.3664
            -218.981	1.4004
            -218.973	1.3102
            -225.22	1.3435
            -238.646	1.3797
            -238.602	1.4426
            -239.787	1.4574
            -242.157	1.4658
            -251.636	1.4792
            -284.777	1.5036
            -284.807	1.5038
        ];

        inverted_triangle = [
            0	0
            40	236.3431
            51.845	306.3304
            92.949	437.0775
            130.71	522.5147
            159.5	552.819
            213.326	577.3674
            244.061	587.8442
            238.897	346.0685
        ];

        mode1 = [
            0	0
            -40	236.1865
            -51.599	304.6733
            -94.95	441.9126
            -130.092	521.0493
            -158.873	551.6941
            -203.905	572.5485
            -241.25	585.9008
            -241.244	341.9704
            -264.563	402.0129
            -266.763	405.1971
            -261.999	343.9087
        ];

        mode2 = [
            0	0
            -10.319	312.3838
            -13.688	365.2361
            -37.174	524.2957
            -45.266	555.8903
            -49.388	564.8141
            -66.731	586.5786
            -117.433	608.3598
            -117.437	345.1137
            -119.364	377.4627
            -120.102	385.0744
            -120.105	231.4074
            -125.49	293.7945
            -125.494	247.2837
            -127.172	265.2477
            -127.93	269.7476
            -128.436	271.3006
            -128.44	225.297
            -129.13	230.9622
            -135.155	253.5923
            -135.159	213.8888
            -136.439	225.6785
            -146.089	263.5301
            -147.699	266.962
            -148.349	267.6654
        ];

        mode3 = [
            0	0
            3.325	374.1394
            3.507	386.8847
            3.723	395.6907
            4.145	403.5144
            19.073	541.2025
            23.311	558.3738
            28.458	570.7841
            42.746	584.3709
            42.754	429.1878
            43.369	471.6258
            43.558	478.7923
            43.935	485.4926
            43.939	355.8635
            44.912	390.0211
            45.52	400.0558
            47.41	417.7216
            48.144	419.1827
            52.606	421.9977
            52.877	351.5039
            53.16	356.7284
            54.21	362.0758
            54.517	370.6436
            58.394	380.6292
            62.819	382.5477
            63.407	383.4258
        ];

    end

    methods
        function [sd, sa] = load_pattern(obj, name)
            [~, index] = max(obj.(name)(:, 2));
            [pf, mass] = obj.parameter(name);
            sd = abs(obj.(name)(1:index, 1).' ./ pf);
            sa = abs(obj.(name)(1:index, 2).' ./ mass);
        end

        function [ss, s1] = spectrum(obj, name)
            if name == "DBE"
                ss = obj.SDS_SD1(1);
                s1 = obj.SDS_SD1(2);
            elseif name == "MCE"
                ss = obj.SMS_SM1(1);
                s1 = obj.SMS_SM1(2);
            end
        end

        function [PF, effective_mass] = parameter(obj, name)
            if name == "mmc" || name == "inverted_triangle"
                index = 1;
            else
                index = str2double(name(end));
            end

            PF = obj.PF(index);
            effective_mass = obj.effective_mass(index);

        end
    end

end
