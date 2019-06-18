classdef Tradition

    properties
        filename = 'RSN1158_KOCAELI_DZC180';

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
            40	18.3496
            57.468	26.3628
            95.211	36.2108
            95.305	36.2264
        ];

        mode1 = [
            0	0
            40	112.4638
            69.135	194.3806
            107.052	256.7266
            126.405	272.7376
            191.642	288.5332
            231.583	295.5635
            249.324	298.7382
            248.68	195.6771
            254.835	204.0808
            255.771	204.8275
            255.819	204.9047
        ];

        mode2 = [
            0	0
            12.009	186.2547
            14.661	217.4314
            21.051	266.1492
            35.2	316.1655
            35.2	316.1655
        ];

        mode3 = [
            0	0
            -3.315	207.5116
            -4.373	261.4717
            -6.552	284.7325
            -10.063	300.9403
            -23.369	330.0678
            -24.602	331.6795
            -47.438	344.7351
            -47.442	287.3003
            -48.198	293.5135
            -48.753	294.4434
            -48.768	194.036
            -50.432	238.6262
            -50.728	239.0392
            -51.045	240.9103
            -51.129	241.9538
        ];

        inverted_triangle = [
            0	0
            40	113.2014
            69.48	196.6299
            105.545	256.9788
            125.933	274.2336
            189.378	289.6902
            229.326	296.794
            248.305	300.2494
            247.972	200.2417
            253.513	207.8939
            254.762	208.8619
            254.772	208.8743
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
