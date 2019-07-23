classdef Tradition

    properties
        structural_behavior_type = 'A';

        % SDS_SD1 = [0.5, 0.3];
        % SMS_SM1 = [0.7, 0.4];
        SDS_SD1 = [0.66, 0.49];
        SMS_SM1 = [0.8, 0.54];
        % SDS_SD1 = [0.8, 0.675];
        % SMS_SM1 = [1, 0.77];

        PF = [
            1.377, 0.548, 0.295
        ];

        effective_mass = [
            4351, 817, 202
        ];

        % roof displacement(mm), V(tonf)
        mmc = [
            1.263E-12	0
            100	296.58
            120.711	358.0045
            133.117	389.472
            145.114	406.8871
            160.722	417.83
            313.285	462.7744
            483.44	493.3052
            561.012	503.9072
            672.35	513.4215
            680.06	513.8432
            680.069	395.8628
            701.064	413.7186
            721.611	422.8767
            722.103	423.1488
        ];

        mode1 = [
            1.263E-12	0
            110	186.8661
            202.436	343.8944
            231.478	389.111
            250.417	403.0368
            275.261	411.8754
            310.251	417.8224
            348.081	421.1601
            357.36	421.6201
            386.242	422.2856
            438.247	422.9825
            548.247	423.8192
            581.382	424.0387
            788.652	424.5133
            821.194	424.5823
            867.446	424.5749
            897.479	338.0969
            966.505	371.2854
            1055.922	391.999
            1113.873	398.2138
            1113.972	398.2321
        ];

        mode2 = [
            1.263E-12	0
            -36.352	230.8558
            -48.695	293.8746
            -48.704	293.7444
            -56.131	314.671
            -91.594	357.2903
            -116.044	373.6317
            -242.628	408.3662
            -276.355	414.2904
            -367.721	422.6133
            -367.731	358.7447
            -370.382	368.8574
            -370.392	347.6615
            -375.61	361.7726
            -369.709	287.7615
            -376.809	314.129
            -379.885	320.6864
            -389.954	332.8459
        ];

        mode3 = [
            1.263E-12	0
            14.582	135.4056
            18.99	166.4331
            36.914	217.4855
            45.099	231.3984
            45.098	231.3912
        ];

        inverted_triangle = [
            1.263E-12	0
            110	190.4685
            202.158	350.0439
            232.1	396.8176
            251.019	410.6069
            275.959	418.9691
            309.003	424.463
            355.769	428.6778
            368.214	429.3237
            410.34	430.3698
            470.36	431.197
            580.36	432.0508
            631.478	432.4404
            746.123	432.743
            856.123	432.9825
            883.7	433.0364
            936.445	432.9662
            936.437	432.7624
            939.875	432.8019
            1040.858	432.5847
            1040.908	432.5844
            1040.935	432.587
            1040.948	432.5873
            1040.954	432.5871
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
