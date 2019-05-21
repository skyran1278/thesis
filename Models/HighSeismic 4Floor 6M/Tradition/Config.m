classdef Config

    properties
        structural_behavior_type = 'A';

        SDS_SD1 = [0.8, 0.675];
        SMS_SM1 = [1, 0.77];

        PF = [
            1.259, 1.138, 1.092
        ];

        effective_mass = [
            451, 52, 16
        ];

        % roof displacement(mm), V(tonf)
        mmc = [
            0	0
            30	20.0132
            40.295	26.8811
            57.627	35.3258
            73.299	38.1296
            95.727	40.6629
            136.246	43.2297
            194.152	45.4337
            188.865	31.409
        ];

        inverted_triangle = [
            0	0
            30	56.0805
            54.612	102.089
            64.528	117.1341
            74.312	123.3909
            99.293	130.7849
            130.984	136.8281
            160.984	139.9993
            190.984	143.1009
            196.867	143.7066
            196.867	143.7066
            196.867	143.7066
            196.867	143.7066
            196.867	143.7066
        ];

        mode1 = [
            0	0
            30	57.0268
            55.85	106.1655
            63.974	118.4014
            72.218	124.2797
            107.426	135.078
            139.423	141.3145
            169.423	144.5272
            182.144	145.8703
            182.144	145.8703
            182.144	145.8703
        ];

        mode2 = [
            0	0
            8.06	61.8494
            10.187	75.1695
            11.224	79.0409
            17.019	89.7733
            19.67	92.689
            65.272	115.0885
            104.605	134.1313
            104.613	117.3546
            104.616	114.365
            107.472	122.819
            107.474	81.0983
            117.092	102.9796
            118.566	104.7528
            125.892	108.2029
            125.947	108.2728
        ];

        mode3 = [
            0	0
            -2.772	56.3748
            -4.075	72.7349
            -7.935	92.0268
            -23.676	131.2185
            -27.705	135.8781
            -36.703	141.8994
            -36.703	141.8994
            -36.703	141.8994
            -36.703	141.8994
            -36.703	141.8994
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
