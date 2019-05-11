classdef Config

    properties
        SDS_SD1 = [0.5, 0.3];
        SMS_SM1 = [0.7, 0.4];

        structural_behavior_type = 'A';

        PF = [
            1.272, 1.172, 1.073
        ];

        effective_mass = [
            1768.8, 219.8, 68.4
        ];

        % sd(mm), sa(g)
        mmc = [
            0	0
            8.904	0.280781
            19.535	0.452255
            31.077	0.48542
            35.436	0.498543
            38.481	0.501705
            50.036	0.50453
            61.594	0.508297
            73.152	0.512204
            84.712	0.516698
            96.272	0.52131
            104.945	0.525048
            105.44	0.267734
            113.717	0.322859
            116.571	0.3316
        ];

        inverted_triangle = [
            0.00	0.00
            31.07	0.12
            93.61	0.23
            102.10	0.24
            159.16	0.26
        ];

        mode1 = [
            30.89	0.12
            92.52	0.23
            101.02	0.24
            157.32	0.26
        ];

        mode2 = [
            0.00	0.00
            7.43	1.02
            7.80	1.06
            8.70	1.13
            35.92	2.09
            38.73	2.15
            50.81	2.30
            66.23	2.38
            96.01	2.44
            96.01	1.91
            96.02	1.34
            97.86	1.46
            100.13	1.55
        ];

        mode3 = [
            0	0
            2.87	3.92
            3.00	4.04
            3.49	4.32
            9.28	6.37
            9.54	6.63
            9.58	6.71
            9.82	6.83
            14.09	7.70
            15.09	7.77
            17.03	7.85
            27.48	8.01
            28.34	8.07
        ];

    end

    methods
        function [sd, sa] = load_pattern(obj, name)
                sd = obj.(name)(:, 1).';
                sa = obj.(name)(:, 2).';
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
