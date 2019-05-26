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
            1.252, 1.116, 1.103
        ];

        effective_mass = [
            456, 47, 10
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
