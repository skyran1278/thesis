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
            1.319, 0.486, 0.276
        ];

        effective_mass = [
            2736, 415, 131
        ];

        % roof displacement(mm), V(tonf)
        mmc = [
            0.005	0
            50.005	90.0589
            68.779	123.8731
            106.567	169.733
            141.191	188.9205
            215.9	207.192
            270.193	216.9978
            283.342	218.4192
            295.909	219.2021
            346.624	220.4463
            347.327	220.5214
            347.328	206.8835
            350.492	208.5268
            352.426	209.0823
            355.11	209.3406
            355.114	192.9969
            356.677	194.0252
            361.364	195.6419
            362.927	195.9704
            378.943	196.8276
            380.506	196.862
            381.65	196.8719
            382.431	196.883
            382.801	196.8836
            384.737	196.9064
            384.92	196.9021
            386.031	196.9178
            386.032	196.9144
            386.325	196.919
        ];

        mode1 = [
            0.005	0
            50.005	102.8099
            100.005	205.6198
            113.343	233.0449
            126.925	257.3479
            131.25	261.5026
            143.718	267.8948
            198.035	277.0492
            278.254	285.0342
            360.817	290.9034
            419.264	294.4425
            479.588	297.5393
            491.78	298.0485
            491.769	277.1654
            496.706	280.1893
            499.955	281.4478
        ];

        mode2 = [
            0.005	0
            19.611	144.9674
            24.846	177.4017
            44.087	221.5168
            53.327	234.1151
            96.8	259.6619
            105.341	262.7043
            186.262	277.9862
            241.495	284.258
            280.824	287.0962
            280.827	227.2942
            285.054	243.3752
            288.555	249.7454
            288.56	248.2252
            290.686	251.5554
            292.423	252.8655
            293.984	253.5888
            301.524	255.635
            293.874	197.6045
        ];

        mode3 = [
            0.005	0
            9.131	114.262
            10.271	125.6907
            20.002	164.9126
            34.88	199.1023
            38.375	203.6319
            76.116	225.7337
            103.97	234.5485
            104.384	234.6233
            104.384	234.6233
            104.384	234.6233
            104.384	234.6233
        ];

        inverted_triangle = [
            0.005	0
            50.005	102.8333
            100.005	205.6665
            114.696	235.8811
            128.462	260.2643
            139.209	268.2854
            145.376	270.7711
            157.268	273.54
            214.884	281.4807
            279.561	287.44
            353.508	292.5927
            414.201	296.2957
            478.587	299.4982
            498.2	300.2934
            498.204	279.5774
            499.96	280.8321
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
