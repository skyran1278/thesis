classdef Multi

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
            28.482	259.6524
            66.507	468.2724
            73.966	488.4974
            117.083	546.5124
            118.689	548.0428
            118.672	353.2891
            119.421	356.2401
            85.787	117.9416
        ];

        mode1 = [
            0	0
            39.285	213.6182
            82.149	336.3212
            120.178	405.916
            130.952	414.9245
            190.951	437.0698
            206.326	441.3993
            128.476	-0.5612
        ];

        mode2 = [
            0	0
            -8.708	224.5041
            -9.145	234.0024
            -10.293	248.8078
            -38.574	427.3954
            -45.404	451.0364
            -63.652	489.7831
            -80.786	506.862
            -107.569	517.5117
            -107.572	405.2761
            -108.683	423.8322
            -111.232	447.1318
            -111.235	332.2464
            -111.239	278.4193
            -112.08	288.1407
            4.943	-475.6192
        ];

        mode3 = [

        ];

        inverted_triangle = [
            0	0
            39.511	213.737
            79.622	328.6849
            121.599	405.9926
            131.844	414.3654
            187.186	434.5411
            208.96	440.6328
            130.543	-2.1207
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
