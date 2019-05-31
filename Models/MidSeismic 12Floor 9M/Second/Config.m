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
            1.319, 1.28, 1.31
        ];

        effective_mass = [
            2736, 416, 133
        ];

        % roof displacement(mm), V(tonf)
        mmc = [

        ];

        mode1 = [

        ];

        mode2 = [

        ];

        mode3 = [

        ];

        inverted_triangle = [
            0.005	0
            100.005	205.6666
            114.696	235.8811
            128.462	260.2644
            139.209	268.2855
            145.376	270.7712
            157.268	273.5401
            279.561	287.4402
            384.277	294.6222
            496.902	301.1143
            496.912	280.4022
            502.46	283.791
            509.636	286.598
            509.637	277.2164
            513.73	279.1098
            521.915	280.781
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
