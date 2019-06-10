classdef Config

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
            -25	103.3608
            -34.14	141.1494
            -60.737	205.7108
            -87.035	248.7401
            -133.472	286.6006
            -160.033	299.6183
            -185.033	310.5336
            -193.55	314.2522
            49.209	-285.8989
        ];

        mode1 = [
            0	0
            -25	135.9426
            -39.285	213.6177
            -82.149	336.3213
            -107.869	388.814
            -122.854	408.3743
            -131.045	414.8143
            -174.701	430.5296
            -201.97	438.9048
            -206.558	440.2131
            -128.732	-1.5928
        ];

        mode2 = [
            0	0
            -8.708	224.5041
            -9.145	234.0024
            -10.293	248.8078
            -37.736	422.1467
            -47.675	455.9234
            -63.694	490.0757
            -80.523	507.0289
            -105.554	516.9009
            -107.017	517.5257
            -107.018	405.2543
            -108.13	423.8322
            -109.007	431.8461
            -109.009	312.5243
            -110.297	326.4495
            9.256	-484.6231
        ];

        mode3 = [
            0	0
            -3.075	268.0289
            -3.217	276.1225
            -3.515	287.1838
            -10.098	436.4354
            -10.376	453.9571
            -10.636	462.3335
            -15.974	502.7239
            -19.473	518.4023
            -21.799	524.3236
            -22.257	526.2678
            -22.257	526.2678
        ];

        inverted_triangle = [
            0	0
            25	135.2399
            39.511	213.7365
            79.622	328.685
            109.235	388.8944
            124.302	408.4365
            132.976	414.5505
            167.41	426.9538
            205.609	438.5048
            209.247	439.5679
            130.657	-4.1652
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
