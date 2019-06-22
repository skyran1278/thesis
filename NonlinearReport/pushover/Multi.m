classdef Multi

    properties
        structural_behavior_type = 'A';

        % SDS_SD1 = [0.5, 0.3];
        % SMS_SM1 = [0.7, 0.4];
        SDS_SD1 = [0.66, 0.49];
        SMS_SM1 = [0.8, 0.54];
        % SDS_SD1 = [0.8, 0.675];
        % SMS_SM1 = [1, 0.77];

        PF = [
            1.285, 0.398, 0.146
        ];

        effective_mass = [
            975, 135, 45
        ];

        % roof displacement(mm), V(tonf)
        mmc = [
            0	0
            -40	36.8561
            -55.958	51.5596
            -65.047	59.2913
            -97.062	73.1906
            -117.087	78.5588
            -181.467	87.2482
            -181.589	87.2629
            -181.589	87.2629
        ];

        mode1 = [
            0	0
            -40	112.4638
            -69.135	194.3806
            -103.647	252.004
            -127.045	270.0672
            -153.566	276.5049
            -220.259	285.9552
            -245.114	289.2767
            -265.412	290.7954
            -174.171	23.3701
        ];

        mode2 = [
            0	0
            -12.009	186.2547
            -14.661	217.4314
            -21.051	266.1492
            -35.385	315.752
            -35.385	315.752
            -35.385	315.752
        ];

        mode3 = [

        ];

        inverted_triangle = [
            0	0
            40	113.2014
            69.48	196.6299
            105.411	255.8841
            126.569	271.4144
            152.976	277.8592
            217.591	287.1106
            242.35	290.4633
            265.481	292.2161
            174.607	24.093
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
