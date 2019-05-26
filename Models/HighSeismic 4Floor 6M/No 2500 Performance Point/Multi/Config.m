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
            30	100.3406
            44.168	147.7292
            70.122	193.2825
            71.997	194.8782
            104.311	209.2452
            112.163	211.9623
            142.122	218.2451
        ];

        inverted_triangle = [
            0	0
            30	56.0763
            54.568	101.9991
            62.458	114.757
            70.847	121.4458
            98.902	129.986
            127.598	135.4866
            157.598	138.7601
            187.598	142.0336
            199.321	143.2551
            199.321	143.2551
            199.321	143.2551
        ];

        mode1 = [
            0	0
            30	57.022
            55.805	106.0697
            64.032	118.3963
            70.72	123.3147
            106.653	134.2553
            135.71	139.9187
            165.71	143.2586
            184.868	145.3911
            184.868	145.3911
            184.868	145.3911
            184.871	145.3966
        ];

        mode2 = [
            0	0
            -8.06	61.8485
            -10.179	75.1213
            -12.828	82.8461
            -18.301	90.5293
            -19.795	91.8665
            -49.795	106.9821
            -93.905	128.4386
            -93.907	110.3811
            -93.91	106.16
            -94.118	107.2859
            -97.592	116.8974
            -98.775	118.8505
            -98.779	115.0072
            -98.782	95.556
            -100.699	101.2919
            -100.702	78.7083
            -105.698	91.8199
            -105.701	87.8042
            -108.045	92.7069
            -109.92	95.1188
            -111.442	96.1649
            -116.567	98.4639
        ];

        mode3 = [
            0	0
            2.772	56.3775
            4.06	72.5938
            7.587	90.3794
            23.588	131.573
            27.604	136.3194
            36.461	142.2925
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
