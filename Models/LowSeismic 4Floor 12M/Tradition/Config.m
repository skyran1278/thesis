classdef Config

    properties
        structural_behavior_type = 'A';

        SDS_SD1 = [0.5, 0.3];
        SMS_SM1 = [0.7, 0.4];

        PF = [
            1.272, 1.172, 1.073
        ];

        effective_mass = [
            1763, 228, 62
        ];

        % roof displacement(mm), V(tonf)
        mmc = [
            0	0
            -32.976	23.6792
            -82.336	42.1574
            -105.38	48.0743
            -161.273	55.5226
            -177.639	56.8897
            -204.521	58.1471
            -219.432	58.5177
            -219.438	35.2224
            -229.68	37.9599
            -229.683	35.6877
            -242.807	38.6374
            -249.971	39.4065
            -239.906	25.6047
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

        mode1 = [
            0	0
            -39.285	213.6182
            -82.149	336.3212
            -117.656	412.8723
            -128.434	423.655
            -180.713	446.7079
            -199.704	452.4423
            -121.603	9.0663
        ];

        mode2 = [
            0	0
            -8.708	224.5041
            -9.145	234.0024
            -10.205	249.1635
            -42.435	461.4134
            -59.407	505.1974
            -77.307	521.9798
            -112.796	535.0225
            -112.799	419.7305
            -112.803	292.3359
            -114.988	319.9725
            -117.671	339.2231
            -117.674	147.6321
            -133.29	271.317
        ];

        mode3 = [
            0	0
            3.075	268.0289
            3.217	276.1225
            3.74	295.516
            9.954	436.1947
            10.235	453.857
            10.285	459.0293
            10.542	467.3105
            15.118	527.027
            16.191	531.7736
            18.271	536.9634
            29.485	548.1375
            29.933	550.0373
            29.933	550.0373
            29.933	550.0373
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
