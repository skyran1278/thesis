classdef Config

    properties
        structural_behavior_type = 'A';

        % SDS_SD1 = [0.5, 0.3];
        % SMS_SM1 = [0.7, 0.4];
        SDS_SD1 = [0.66, 0.49];
        SMS_SM1 = [0.8, 0.54];
        % SDS_SD1 = [0.8, 0.675];
        % SMS_SM1 = [1, 0.77];

        PF = [
            1.305, 1.326, 1.329
        ];

        effective_mass = [
            2771, 367, 136
        ];

        % roof displacement(mm), V(tonf)
        mmc = [
            0.004	0
            25.004	66.8283
            50.004	133.6566
            75.004	200.485
            88.938	237.7337
            113.557	303.9976
            116.53	308.7501
            138.343	332.3704
            161.78	344.9688
            177.405	349.196
        ];

        mode1 = [
            0.004	0
            25.004	37.2872
            50.004	74.5744
            75.004	111.8616
            100.004	149.1488
            125.004	186.4359
            150.004	223.7231
            165.014	246.1099
            172.853	256.4397
            172.854	256.4391
            191.602	269.1083
            200.977	272.5089
            213.477	275.0442
        ];

        mode2 = [
            0.004	0
            -24.997	126.7432
            -25.797	130.8005
            -34.373	166.6111
            -39.259	179.2333
            -56.666	206.2228
            -81.56	227.8346
            -107.604	238.3701
            -151.994	248.1445
            -182.624	253.475
            -222.512	258.5673
            -239.58	260.5227
            -239.58	260.5227
            -239.58	260.5227
        ];

        mode3 = [
            0.004	0
            -11.446	114.5119
            -15.571	139.1508
            -36.777	197.7629
            -47.102	210.7274
            -57.318	217.926
            -57.318	217.926
            -57.318	217.926
            -57.318	217.926
            -57.318	217.926
        ];

        inverted_triangle = [
            0.004	0
            25.004	37.0071
            50.004	74.0142
            75.004	111.0214
            100.004	148.0285
            125.004	185.0356
            150.004	222.0427
            167.375	247.756
            175.594	258.527
            175.594	258.5261
            194.344	270.8867
            206.844	274.9017
            213.094	276.1546
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
