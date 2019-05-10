classdef Config

    properties
        SDS_SD1 = [0.5, 0.3];
        SMS_SM1 = [0.7, 0.4];

        structural_behavior_type = 'A';

        triangle = [
            0	0
            31.004	0.121049
            81.273	0.218159
            95.44	0.233885
            104.382	0.238064
            164.546	0.247432

        ];

        power = [
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

        uniform = [
            0	0
            9.396	0.38995
            15.281	0.519193
            26.946	0.567329
            32.438	0.596899
            35.346	0.605905
            46.583	0.627426
            58.142	0.63554
            69.704	0.643323
            81.266	0.650824
            92.83	0.658184
            97.418	0.661245
            97.913	0.360103
            105.008	0.415368
            108.148	0.427034
            117.199	0.431398
        ];

    end

    methods
        function [sd, sa] = load_pattern(obj, name)
            if name == "triangle"
                sd = obj.triangle(:, 1).';
                sa = obj.triangle(:, 2).';
            elseif name == "uniform"
                sd = obj.uniform(:, 1).';
                sa = obj.uniform(:, 2).';
            elseif name == "power"
                sd = obj.power(:, 1).';
                sa = obj.power(:, 2).';
            end
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
    end

end
