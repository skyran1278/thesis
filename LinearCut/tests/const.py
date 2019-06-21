""" const from user. """
# pylint: disable=invalid-name
import os

import numpy as np

_test_dir = os.path.dirname(os.path.abspath(__file__))

"""
公尺的輸出一律四捨五入到小數點下第五位，公分一律第三位。
"""
const = {
    'etabs_design_path': 'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/Concrete Design 2 - Beam Summary Data - ACI 318-05_IBC 2003.xlsx',
    'e2k_path': 'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/LowSeismic 4Floor 12M.e2k',

    'beam_name_path': _test_dir + '/LowSeimic 4Floor 12M 20190416 174732 SmartCut.xlsx',

    'output_dir': 'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M',

    'stirrup_rebar': ['#4', '2#4', '2#5', '2#6'],
    'stirrup_spacing': np.array([10, 12, 15, 18, 20, 22, 25, 30]),

    'rebar': {
        'Top': ['#8', '#10', '#11', '#14'],
        'Bot': ['#8', '#10', '#11', '#14']
    },

    'db_spacing': 1.5,

    'boundary': {
        'left': np.array([0, 0.45]),
        'right': np.array([0.55, 1])
    },

    'cover': 0.04,
    'cut_num': 2
}
