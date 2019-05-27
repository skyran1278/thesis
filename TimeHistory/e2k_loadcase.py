"""
generate function and loadcase e2k with peernga data
"""
import shlex

low_seismic_4floor_12m = {
    'factors': [0.1, 0.297, 0.396, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 2, 2.5, 3, 4],
    'modal_participating_mass': [0.853, 0.106, 0.034],
    'period': [1.013, 0.3],
    'displacement': 0.4,
    'time_historys': {
        'RSN725_SUPER.B_B-POE360': {'sa': 0.548, 'pga': 0.463},
        'RSN900_LANDERS_YER270': {'sa': 0.448, 'pga': 0.224},
        'RSN953_NORTHR_MUL279': {'sa': 0.648, 'pga': 0.343},
        'RSN960_NORTHR_LOS000': {'sa': 0.388, 'pga': 0.426},
        'RSN1111_KOBE_NIS000': {'sa': 0.296, 'pga': 0.483},
        'RSN1116_KOBE_SHI000': {'sa': 0.486, 'pga': 0.336},
        'RSN1148_KOCAELI_ARE090': {'sa': 0.140, 'pga': 0.157},
        'RSN1158_KOCAELI_DZC180': {'sa': 0.343, 'pga': 0.248},
        'RSN1602_DUZCE_BOL090': {'sa': 0.791, 'pga': 0.574},
        'RSN1633_MANJIL_ABBAR--T': {'sa': 0.501, 'pga': 0.460},
        'RSN1787_HECTOR_HEC090': {'sa': 0.402, 'pga': 0.343},
    },
}

mid_seismic_4floor_12m = {
    'factors': [1.071, 1.181, 2, 3, 5, 7, 9, 11, 13, 15],
    'modal_participating_mass': [0.844, 0.111, 0.036],
    'period': [],
    'displacement': 0.4,
}

mid_seismic_12floor_9m = {
    'factors': [0.1, 0.264, 0.32, 0.5, 0.8, 1, 1.2, 1.5, 1.8, 2, 3],
    'modal_participating_mass': [0.792, 0.105, 0.039, 0.022],
    'period': [2.387, 0.787],
    'displacement': 1,
    'time_historys': {
        'RSN725_SUPER.B_B-POE360': {'sa': 0.278, 'pga': 0.463},
        'RSN900_LANDERS_YER270': {'sa': 0.130, 'pga': 0.224},
        'RSN953_NORTHR_MUL279': {'sa': 0.112, 'pga': 0.343},
        'RSN960_NORTHR_LOS000': {'sa': 0.227, 'pga': 0.426},
        'RSN1111_KOBE_NIS000': {'sa': 0.192, 'pga': 0.483},
        'RSN1116_KOBE_SHI000': {'sa': 0.223, 'pga': 0.336},
        'RSN1148_KOCAELI_ARE090': {'sa': 0.084, 'pga': 0.157},
        'RSN1158_KOCAELI_DZC180': {'sa': 0.201, 'pga': 0.248},
        'RSN1602_DUZCE_BOL090': {'sa': 0.101, 'pga': 0.574},
        'RSN1633_MANJIL_ABBAR--T': {'sa': 0.319, 'pga': 0.460},
        'RSN1787_HECTOR_HEC090': {'sa': 0.143, 'pga': 0.343},
    },
}

high_seismic_4floor_6m = {
    'factors': [0.5, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.5, 3],
    'modal_participating_mass': [0.88, 0.09, 0.02],
    'period': [0.763, 0.241],
    'displacement': 0.4,
    'time_historys': {
        'RSN725_SUPER.B_B-POE360': {'sa': 0.547, 'pga': 0.463},
        'RSN900_LANDERS_YER270': {'sa': 0.424, 'pga': 0.224},
        'RSN953_NORTHR_MUL279': {'sa': 0.607, 'pga': 0.343},
        'RSN960_NORTHR_LOS000': {'sa': 0.624, 'pga': 0.426},
        'RSN1111_KOBE_NIS000': {'sa': 0.637, 'pga': 0.483},
        'RSN1116_KOBE_SHI000': {'sa': 0.786, 'pga': 0.336},
        'RSN1148_KOCAELI_ARE090': {'sa': 0.202, 'pga': 0.157},
        'RSN1158_KOCAELI_DZC180': {'sa': 0.387, 'pga': 0.248},
        'RSN1602_DUZCE_BOL090': {'sa': 0.938, 'pga': 0.574},
        'RSN1633_MANJIL_ABBAR--T': {'sa': 0.554, 'pga': 0.460},
        'RSN1787_HECTOR_HEC090': {'sa': 0.345, 'pga': 0.343},
    },
}

CONFIG = low_seismic_4floor_12m


def put_timehistorys(time_historys, factors, peernga_folder):
    """
    put NPTS, DT
    """
    for time_history in time_historys:
        time_historys[time_history]['FACTORS'] = factors

        with open(f'{peernga_folder}/{time_history}.AT2') as f:
            words = shlex.split(f.readlines()[3])
            time_historys[time_history]['NPTS'] = int(words[1][:-1])
            time_historys[time_history]['DT'] = float(words[3])


def post_functions(time_historys, peernga_folder):
    """
    path folder same as time history

    @example
    FUNCTION "RSN169_IMPVALL.H_H-DLT262"  FUNCTYPE "HISTORY"
    FILE "path.AT2"  DATATYPE "EQUAL"  DT 0.01

    FUNCTION "RSN169_IMPVALL.H_H-DLT262"  HEADERLINES 4  POINTSPERLINE 5  FORMAT "FREE"
    """
    # post functions to list
    functions = []

    for time_history in time_historys:
        delta_t = time_historys[time_history]['DT']

        functions.append(
            f'FUNCTION "{time_history}"  FUNCTYPE "HISTORY"  '
            f'FILE "{peernga_folder}/{time_history}.AT2"  '
            f'DATATYPE "EQUAL"  DT {delta_t}\n'
        )

        functions.append(
            f'FUNCTION "{time_history}"  HEADERLINES 4  POINTSPERLINE 1  FORMAT "FREE"\n'
        )

    return functions


def post_previous_loadcases(initial_condition, dead_load, live_load):
    """
    LOADCASE "1.0DL + 0.5LL"  TYPE  "Nonlinear Static"  INITCOND  "NONE"
    MODALCASE  "Modal"  MASSSOURCE  "Previous"

    LOADCASE "1.0DL + 0.5LL"  LOADPAT  "DL"  SF  1

    LOADCASE "1.0DL + 0.5LL"  LOADPAT  "LL"  SF  0.5

    LOADCASE "1.0DL + 0.5LL"  NLGEOMTYPE  "PDelta"

    LOADCASE "1.0DL + 0.5LL"  LOADCONTROL  "Full"  DISPLTYPE  "Monitored"
    MONITOREDDISPL  "Joint"  DISPLMAG  0 DOF  "U3"  JOINT  "1"  "RF"

    LOADCASE "1.0DL + 0.5LL"  RESULTSSAVED  "Multiple"  MINSAVED  1 MAXSAVED  200

    LOADCASE "1.0DL + 0.5LL"  USEEVENTSTEPPING  "Yes"  MAXITERCS  4 MAXITERNR  10

    """
    # pylint: disable=line-too-long
    return (
        f'LOADCASE "{initial_condition}"  TYPE  "Nonlinear Static"  INITCOND  "NONE"  MODALCASE  "Modal"  MASSSOURCE  "Previous"\n',
        f'LOADCASE "{initial_condition}"  LOADPAT  "{dead_load}"  SF  1\n',
        f'LOADCASE "{initial_condition}"  LOADPAT  "{live_load}"  SF  0.5\n',
        f'LOADCASE "{initial_condition}"  NLGEOMTYPE  "PDelta"\n',
        f'LOADCASE "{initial_condition}"  LOADCONTROL  "Full"  DISPLTYPE  "Monitored"  MONITOREDDISPL  "Joint"  DISPLMAG  0 DOF  "U3"  JOINT  "1"  "RF"\n'
        f'LOADCASE "{initial_condition}"  RESULTSSAVED  "Multiple"  MINSAVED  1 MAXSAVED  200\n'
        f'LOADCASE "{initial_condition}"  USEEVENTSTEPPING  "Yes"  MAXITERCS  4 MAXITERNR  10\n'
    )


def post_pushover_loadcases(displacement, modal_participating_mass, initial_condition, direction):
    """
    LOADCASE "pushover x"  TYPE  "Nonlinear Static"  INITCOND  "1.0DL + 0.5LL"
    MODALCASE  "Modal"  MASSSOURCE  "Previous"

    LOADCASE "pushover x"  LOADPAT  "EQX"  SF  1

    LOADCASE "pushover x"  NLGEOMTYPE  "PDelta"

    LOADCASE "pushover x"  LOADCONTROL  "Displacement"  DISPLTYPE  "Conjugate"
    MONITOREDDISPL  "Joint"  DISPLMAG  0.2 DOF  "U1"  JOINT  "1"  "RF"

    LOADCASE "pushover x"  RESULTSSAVED  "Multiple"  MINSAVED  10 MAXSAVED  200

    LOADCASE "pushover x"  USEEVENTSTEPPING  "Yes"  MAXITERCS  4 MAXITERNR  10

    LOADCASE "MMC"  TYPE  "Nonlinear Static"  INITCOND  "PUSHDLLL"
    MODALCASE  "Modal"  MASSSOURCE  "Previous"

    LOADCASE "MMC"  MODE  1 SF  0.835511

    LOADCASE "MMC"  MODE  2 SF  0.112514

    LOADCASE "MMC"  NLGEOMTYPE  "PDelta"

    LOADCASE "MMC"  LOADCONTROL  "Displacement"  DISPLTYPE  "Conjugate"
    MONITOREDDISPL  "Joint"  DISPLMAG  0.2 DOF  "U1"  JOINT  "1"  "RF"

    LOADCASE "MMC"  RESULTSSAVED  "Multiple"  MINSAVED  10 MAXSAVED  200

    LOADCASE "MMC"  USEEVENTSTEPPING  "Yes"  MAXITERCS  4 MAXITERNR  10

    LOADCASE "PUSHXP1"  TYPE  "Nonlinear Static"  INITCOND  "PUSHDLLL"
    MODALCASE  "Modal"  MASSSOURCE  "Previous"

    LOADCASE "PUSHXP1"  MODE  1 SF  1

    LOADCASE "PUSHXP1"  NLGEOMTYPE  "PDelta"

    LOADCASE "PUSHXP1"  LOADCONTROL  "Displacement"  DISPLTYPE  "Conjugate"
    MONITOREDDISPL  "Joint"  DISPLMAG  0.2 DOF  "U1"  JOINT  "1"  "RF"

    LOADCASE "PUSHXP1"  RESULTSSAVED  "Multiple"  MINSAVED  10 MAXSAVED  200

    LOADCASE "PUSHXP1"  USEEVENTSTEPPING  "Yes"  MAXITERCS  4 MAXITERNR  10

    """
    def load(name, *load_pattern):
        return (
            (
                f'LOADCASE "{name}"  TYPE  "Nonlinear Static"  '
                f'INITCOND  "{initial_condition}"  MODALCASE  "Modal"  MASSSOURCE  "Previous"\n'
            ),
            *load_pattern,
            f'LOADCASE "{name}"  NLGEOMTYPE  "PDelta"\n',
            (
                f'LOADCASE "{name}"  LOADCONTROL  "Displacement"  DISPLTYPE  "Conjugate"  '
                f'MONITOREDDISPL  "Joint"  DISPLMAG  {displacement} '
                f'DOF  "{direction}"  JOINT  "1"  "RF"\n'
            ),
            f'LOADCASE "{name}"  RESULTSSAVED  "Multiple"  MINSAVED  10 MAXSAVED  200\n',
            f'LOADCASE "{name}"  USEEVENTSTEPPING  "Yes"  MAXITERCS  4 MAXITERNR  10\n',
        )

    loadcases = []

    loadcases.extend(
        load('Pushover X', f'LOADCASE "Pushover X"  LOADPAT  "EQX"  SF  1\n'))

    loadcases.extend(load(
        'MMC',
        *[
            f'LOADCASE "MMC"  MODE  {mode} SF  {factor}\n'
            for mode, factor in enumerate(modal_participating_mass, 1)
        ]
    ))

    for mode, factor in enumerate(modal_participating_mass, 1):
        loadcases.extend(load(
            f'Mode {mode}',
            f'LOADCASE "Mode {mode}"  MODE  {mode} SF  {factor}\n'
        ))

    return loadcases


def post_timehistorys_loadcases(time_historys, period, initial_condition, direction):
    """
    loadcase

    @example
    LOADCASE "timehistory"  TYPE  "Nonlinear Direct Integration History"
    INITCOND  "1.0DL + 0.5LL"  MODALCASE  "Modal"  MASSSOURCE  "Previous"

    LOADCASE "timehistory"  ACCEL  "U1"  FUNC  "chichi_TCU052_max"  SF  1

    LOADCASE "timehistory"  NLGEOMTYPE  "PDelta"  NUMBEROUTPUTSTEPS  100 OUTPUTSTEPSIZE  0.1

    LOADCASE "timehistory"  PRODAMPTYPE  "Period"  T1  0.344 DAMP1  0.05 T2  0.088 DAMP2  0.05

    # LOADCASE "timehistory"  MODALDAMPTYPE  "Constant"  CONSTDAMP  0.05
    # CONSIDERMAXMODALFREQ  "Yes"  MAXCONSIDEREDMODALFREQ  100

    LOADCASE "timehistory"  MODALDAMPTYPE  "None"

    LOADCASE "timehistory"  USEEVENTSTEPPING  "No"
    """
    loadcases = []

    for time_history in time_historys:
        sa = time_historys[time_history]['sa']
        factors = time_historys[time_history]['FACTORS']
        number_output_steps = time_historys[time_history]['NPTS']
        delta_t = time_historys[time_history]['DT']

        for factor in factors:
            name = f'{time_history}-{round(factor / sa, 2)}'

            # G to m/s2
            factor = round(factor / sa * 9.81, 2)

            loadcases.append(
                f'LOADCASE "{name}"  TYPE  "Nonlinear Direct Integration History"  '
                f'INITCOND  "{initial_condition}"  MODALCASE  "Modal"  MASSSOURCE  "Previous"\n'
            )

            loadcases.append(
                f'LOADCASE "{name}"  ACCEL  "{direction}"  '
                f'FUNC  "{time_history}"  SF  {factor}\n'
            )
            loadcases.append(
                f'LOADCASE "{name}"  NLGEOMTYPE  "PDelta"  NUMBEROUTPUTSTEPS  {number_output_steps} '
                f'OUTPUTSTEPSIZE  {delta_t}\n'
            )
            loadcases.append(
                f'LOADCASE "{name}"  PRODAMPTYPE  "Period"  T1  {period[0]} DAMP1  0.05 '
                f'T2  {period[1]} DAMP2  0.05\n'
            )
            loadcases.append(
                f'LOADCASE "{name}"  MODALDAMPTYPE  "None"\n'
            )
            # loadcases.append(
            #     f'LOADCASE "{name}"  PRODAMPTYPE  "Period"  T1  {period[0]} DAMP1  0.005 '
            #     f'T2  {period[1]} DAMP2  0.05\n'
            # )
            # loadcases.append(
            #     f'LOADCASE "{name}"  MODALDAMPTYPE  "Constant"  CONSTDAMP  0.05 '
            #     f'CONSIDERMAXMODALFREQ  "Yes"  MAXCONSIDEREDMODALFREQ  100 \n'
            # )
            loadcases.append(f'LOADCASE "{name}"  USEEVENTSTEPPING  "No"\n')

    return loadcases


def main():
    """
    test
    """
    import os

    # global
    script_folder = os.path.dirname(os.path.abspath(__file__))

    peernga_folder = script_folder + '/PEERNGARecords_Normalized'

    direction = 'U1'

    initial_condition = '1.0DL + 0.5LL'
    dead_load = 'DL'
    live_load = 'LL'

    # different by model
    displacement = CONFIG['displacement']

    modal_participating_mass = CONFIG['modal_participating_mass']

    period = CONFIG['period']

    factors = CONFIG['factors']

    time_historys = CONFIG['time_historys']

    put_timehistorys(time_historys, factors, peernga_folder)

    with open(script_folder + '/e2k_functions.e2k', mode='w', encoding='big5') as f:
        f.writelines(post_functions(time_historys, peernga_folder))

    with open(script_folder + '/e2k_loadcase.e2k', mode='w', encoding='big5') as f:
        f.writelines(post_previous_loadcases(
            initial_condition, dead_load, live_load))
        f.writelines(post_pushover_loadcases(
            displacement, modal_participating_mass, initial_condition, direction))

        f.writelines(post_timehistorys_loadcases(
            time_historys, period, initial_condition, direction))


if __name__ == "__main__":
    main()
