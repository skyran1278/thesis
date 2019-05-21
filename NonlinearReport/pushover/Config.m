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
            28.352	312.2435
            54.437	517.0216
            59.971	539.2643
            101.053	614.2404
            102.233	615.9996
            60.332	115.0328
        ];

        inverted_triangle = [
            0	0
            39.511	213.737
            79.622	328.6849
            121.627	405.9537
            133.023	414.5973
            180.649	431.2546
            209.33	439.5346
            130.781	-3.9664
        ];

        mode1 = [
            0	0
            39.285	213.6182
            82.149	336.3212
            120.195	405.8963
            131.093	414.8716
            187.238	434.6065
            206.644	440.2319
            127.76	-7.5501
        ];

        mode2 = [
            0	0
            -8.708	224.5041
            -9.145	234.0024
            -10.293	248.8078
            -37.736	422.1467
            -47.675	455.9234
            -63.694	490.0757
            -80.594	507.1679
            -106.86	517.5051
            -106.863	405.2707
            -107.973	423.8187
            -108.925	432.5143
            -108.929	313.1947
            -110.188	326.8069
            9.32	-484.3738
        ];

        mode3 = [
            0	0
            3.075	268.0289
            3.217	276.1225
            3.515	287.1838
            10.098	436.4354
            10.376	453.9571
            10.636	462.3335
            15.974	502.7238
            19.473	518.4023
            21.799	524.3237
            22.437	527.0315
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
