classdef Config

    properties
        structural_behavior_type = 'A';

        % SDS_SD1 = [0.5, 0.3];
        % SMS_SM1 = [0.7, 0.4];
        % SDS_SD1 = [0.66, 0.49];
        % SMS_SM1 = [0.8, 0.54];
        SDS_SD1 = [0.8, 0.675];
        SMS_SM1 = [1, 0.77];

        PF = [
            1.285, 1.2, 1.057
        ];

        effective_mass = [
            980, 140, 47
        ];

        % roof displacement(mm), V(tonf)
        mmc = [
            0	0
            40	142.4842
            47.914	170.6766
            78.548	233.0173
            95.966	251.533
            103.744	254.3574
            103.782	254.3574
            103.961	254.4105
        ];

        mode1 = [
            0	0
            40	112.3757
            69.098	194.1225
            105.387	253.9204
            126.929	270.4344
            183.147	282.9468
            223.086	289.3416
            243.155	292.1299
            263.396	293.3614
            172.075	25.8952
        ];

        mode2 = [
            0	0
            -12.01	186.2328
            -14.663	217.4068
            -21.033	265.9497
            -36.296	318.7361
            -37.474	321.3799
            -37.474	321.3799
        ];

        mode3 = [
            0	0
            -3.315	207.5265
            -4.373	261.4787
            -6.552	284.7421
            -10.061	300.9384
            -22.375	327.1695
            -22.846	327.7791
            -47.68	343.0896
            -47.817	301.4025
            -48.335	304.6673
            -48.935	305.9673
            -48.939	202.1092
            -50.265	239.3375
            -50.299	250.8395
            -51.053	256.0789
            -51.057	177.4679
            -52.36	197.8981
            -53.569	206.7069
            -56.114	216.3742
            -57.641	217.8822
            -63.035	219.7626
            -63.192	220.0578
            -63.197	220.0739
            -63.275	220.2208
            -63.276	220.2248
            -63.296	220.2615
        ];

        inverted_triangle = [
            0	0
            40	113.1146
            69.442	196.3716
            105.949	256.4253
            126.668	272.0503
            180.442	284.0593
            220.39	290.5324
            240.33	293.4001
            263.552	294.8691
            172.628	26.8053
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
