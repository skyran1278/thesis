classdef Tradition

    properties
        structural_behavior_type = 'A';

        SDS_SD1 = [0.5, 0.3];
        SMS_SM1 = [0.7, 0.4];
        % SDS_SD1 = [0.66, 0.49];
        % SMS_SM1 = [0.8, 0.54];
        % SDS_SD1 = [0.8, 0.675];
        % SMS_SM1 = [1, 0.77];

        PF = [
            1.272, 0.381, 0.142
        ];

        effective_mass = [
            1768, 220, 69
        ];

        % roof displacement(mm), V(tonf)
        mmc = [
            0	0
            28.482	259.6524
            67.569	472.6143
            73.297	489.893
            115.062	550.9314
            117.92	554.4859
            117.895	360.0397
            118.919	363.945
            85.544	127.5796
        ];

        mode1 = [
            0	0
            39.285	213.6182
            82.149	336.3212
            117.659	412.6522
            128.503	423.4727
            181.23	446.928
            199.834	452.6785
            121.744	9.3672
        ];

        mode2 = [
            0	0
            -8.708	224.5041
            -9.145	234.0024
            -10.205	249.1635
            -42.281	460.4745
            -44.733	471.1626
            -59.451	505.62
            -77.18	523.1534
            -112.891	537.8158
            -112.894	303.8653
            -117.973	342.304
            -117.978	135.7579
            -130.116	244.4352
            -130.12	208.8647
            -136.325	255.1317
            -146.624	287.7505
            -149.839	292.4094
            -149.95	292.757
        ];

        mode3 = [

        ];

        inverted_triangle = [
            0	0
            39.511	213.737
            79.622	328.6849
            118.656	412.1531
            129.863	423.438
            177.876	444.7359
            202.123	452.1944
            123.703	9.4405
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
