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
            32.976	23.6792
            82.336	42.1574
            105.38	48.0745
            161.322	55.5518
            177.608	56.916
            204.414	58.1727
            219.42	58.5464
            219.428	35.3559
            229.779	38.1117
            229.782	35.8614
            241.474	38.5178
            251.049	39.6044
            185.813	4.1209
        ];

        mode1 = [
            0	0
            39.285	213.6182
            82.149	336.3212
            117.656	412.8722
            128.435	423.6549
            182.508	447.2438
            199.722	452.4232
            121.731	9.6717
        ];

        mode2 = [
            0	0
            8.708	224.5041
            9.145	234.0024
            10.205	249.1635
            42.113	459.4406
            45.412	472.5911
            59.571	505.5671
            77.646	522.47
            112.581	535.1451
            112.584	420.2018
            112.588	292.8502
            114.721	319.9272
            117.42	339.4014
            114.393	109.4134
        ];

        mode3 = [
            0	0
            -3.075	268.0289
            -3.217	276.1225
            -3.74	295.516
            -9.954	436.1947
            -10.235	453.857
            -10.285	459.0293
            -10.542	467.3105
            -15.118	527.027
            -16.191	531.7736
            -18.271	536.9634
            -29.486	548.1386
            -29.934	550.0384
        ];

        inverted_triangle = [
            0	0
            39.511	213.737
            79.622	328.6849
            119.045	413.073
            129.802	423.8039
            179.144	445.1944
            202.067	452.0568
            123.513	8.5381
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
