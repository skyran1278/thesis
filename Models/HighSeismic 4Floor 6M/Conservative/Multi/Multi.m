classdef Multi

    properties
        structural_behavior_type = 'A';

        % SDS_SD1 = [0.5, 0.3];
        % SMS_SM1 = [0.7, 0.4];
        % SDS_SD1 = [0.66, 0.49];
        % SMS_SM1 = [0.8, 0.54];
        SDS_SD1 = [0.8, 0.675];
        SMS_SM1 = [1, 0.77];

        PF = [
            1.252, 0.35, 0.126
        ];

        effective_mass = [
            457, 47, 12
        ];

        % roof displacement(mm), V(tonf)
        mmc = [
            -0.0003791	0
            -33.641	123.6258
            -42.153	144.2048
            -55.175	161.8676
            -70.283	173.3136
            -72.074	174.0311
            -112.139	181.8308
            -140.973	186.3897
            -142.135	186.5036
            -142.135	186.5036
            -142.135	186.5036
            -142.135	186.5036
        ];

        mode1 = [
            -0.0003791	0
            -40	100.7798
            -42.493	107.0591
            -51.537	122.3229
            -55.27	125.8569
            -90.338	140.681
            -131.811	149.7594
            -134.62	150.1559
            -174.579	152.7968
            -215.866	155.4294
            -218.522	155.5552
            -262.572	156.2518
            -262.504	139.6325
            -269.993	144.7682
        ];

        mode2 = [
            -0.0003791	0
            6.021	55.9491
            8.913	78.1461
            16.169	96.862
            26.388	108.7045
            44.694	117.6807
            50.177	119.3707
            54.906	120.3243
            127.26	123.1222
            133.098	123.3647
            133.101	104.3188
            135.8	112.8689
            135.804	109.4638
            136.299	110.9097
            136.303	108.1319
            136.706	109.3065
            136.71	103.8738
            137.512	106.39
            137.528	106.5141
            139.093	110.3526
        ];

        mode3 = [

        ];

        inverted_triangle = [
            -0.0003791	0
            40	98.3819
            42.643	104.8825
            52.354	120.8063
            56.965	124.6888
            85.364	136.3164
            140.655	147.6587
            143.782	148.0852
            183.741	150.6456
            196.88	151.4574
            236.836	152.0852
            276.773	152.6064
            276.895	152.6143
            276.842	136.6573
            278.866	138.5858
            282.94	140.935
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
