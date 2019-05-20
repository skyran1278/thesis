classdef Config

    properties
        structural_behavior_type = 'A';

        SDS_SD1 = [0.8, 0.675];
        SMS_SM1 = [1, 0.77];

        PF = [
            1.259, 1.138, 1.092
        ];

        effective_mass = [
            451, 52, 16
        ];

        % roof displacement(mm), V(tonf)
        mmc = [

        ];

        inverted_triangle = [
            0	0
            50	295.4289
            51.846	306.3361
            130.112	524.797
            185.339	608.214
            199.867	620.4891
            231.598	633.5047
            231.112	411.3437
            232.183	413.6121
            238.431	421.9039
            238.45	421.941
            238.45	421.9412
            238.451	421.9429

        ];

        mode1 = [
            0	0
            -50	295.2331
            -51.6	304.679
            -129.478	523.4368
            -184.381	606.3229
            -198.718	618.4193
            -230.099	630.7024
            -230.059	324.5601
            -240.798	332.8657
            -238.028	320.8003

        ];

        mode2 = [
            0	0
            -10.319	312.3838
            -13.688	365.2361
            -37.174	524.2957
            -69.263	652.2851
            -80.937	673.7215
            -84.38	677.4372
            -90.184	681.588
            -109.308	686.8458
            -94.724	210.3026

        ];

        mode3 = [

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
