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
            1.305, 1.315, 1.304
        ];

        effective_mass = [
            2771, 367, 136
        ];

        % roof displacement(mm), V(tonf)
        mmc = [
            3.429E-12	0
            25	57.8008
            50	115.6016
            75	173.4023
            100	231.2031
            107.599	248.7708
            135.377	297.1549
            167.129	325.598
            167.134	325.5922
            195.258	343.2923
            220.258	356.0579
            250.028	369.7309
        ];

        mode1 = [
            3.429E-12	0
            25	37.3269
            50	74.6539
            75	111.9808
            100	149.3078
            125	186.6347
            150	223.9617
            165.113	246.5264
            199.118	279.6751
            217.358	289.4222
            238.045	295.1082
            238.046	295.1055
            250.049	297.0251
        ];

        mode2 = [
            3.429E-12	0
            -25.001	126.8339
            -25.794	130.8609
            -34.374	166.7265
            -39.239	179.3311
            -58.709	208.852
            -80.707	228.5869
            -111.83	242.0741
            -138.048	250.9385
            -165.209	257.564
            -195.757	262.1649
            -224.579	266.0939
            -224.975	266.1449
        ];

        mode3 = [
            3.429E-12	0
            11.459	114.662
            15.587	139.2814
            36.866	200.3094
            50.281	220.379
            57.236	226.7722
        ];

        inverted_triangle = [
            3.429E-12	0
            25	37.047
            50	74.0939
            75	111.1409
            100	148.1879
            125	185.2349
            150	222.2818
            167.473	248.1752
            201.319	281.0575
            217.617	290.0972
            243.329	296.9971
            243.325	296.9911
            249.994	298.0054
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
