"""
normalize
"""
import shlex


def main():
    """
    test
    """
    import os

    # global
    script_folder = os.path.dirname(os.path.abspath(__file__))

    peernga_folder = script_folder + '/PEERNGARecords_Unscaled'

    normalized_folder = script_folder + '/PEERNGARecords_Normalized'

    time_historys = {
        'RSN725_SUPER.B_B-POE360': 1.614,
        'RSN900_LANDERS_YER270': 0.916,
        'RSN953_NORTHR_MUL279': 0.702,
        'RSN960_NORTHR_LOS000': 1.055,
        'RSN1111_KOBE_NIS000': 1.000,
        'RSN1116_KOBE_SHI000': 1.495,
        'RSN1148_KOCAELI_ARE090': 1.169,
        'RSN1158_KOCAELI_DZC180': 0.795,
        'RSN1602_DUZCE_BOL090': 0.711,
        'RSN1633_MANJIL_ABBAR--T': 0.926,
        'RSN1787_HECTOR_HEC090': 1.046,
    }


    for time_history in time_historys:
        normalized_data = []

        with open(f'{peernga_folder}/{time_history}.AT2') as f:
            contents = f.readlines()

        for line in contents[4:]:
            normalized_data.extend([
                float(i) * time_historys[time_history] for i in shlex.split(line)
            ])

        with open(f'{normalized_folder}/{time_history}.AT2', mode='w', encoding='big5') as f:
            f.writelines(contents[:4])
            f.writelines([f'{i:.7E}\n' for i in normalized_data])


if __name__ == "__main__":
    main()
