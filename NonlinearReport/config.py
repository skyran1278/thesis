midseismic_4floor_12m = {
    'scaled_facotrs': {
        'DBE': 1.071,
        'MCE': 1.181,
    },
    'earthquakes': [
        'RSN725_SUPER.B_B-POE360', 'RSN900_LANDERS_YER270', 'RSN953_NORTHR_MUL279',
        'RSN960_NORTHR_LOS000', 'RSN1111_KOBE_NIS000', 'RSN1116_KOBE_SHI000',
        'RSN1148_KOCAELI_ARE090', 'RSN1158_KOCAELI_DZC180', 'RSN1602_DUZCE_BOL090',
        'RSN1633_MANJIL_ABBAR--T', 'RSN1787_HECTOR_HEC090'
    ],
    'story': 'D:/GitHub/thesis/Models/MidSeismic 4Floor 12M/Multi/story.xlsx',
    'multi': 'D:/GitHub/thesis/Models/MidSeismic 4Floor 12M/Multi/story_drifts.xlsx',
    'tradition': 'D:/GitHub/thesis/Models/MidSeismic 4Floor 12M/Tradition/story_drifts.xlsx',
    'tradition_end': 'D:/GitHub/thesis/Models/MidSeismic 4Floor 12M/Tradition End/story_drifts.xlsx'
}

lowseismic_4floor_12m = {
    'scaled_facotrs': {
        'DBE': 0.297,
        'MCE': 0.396,
    },
    'earthquakes': [
        'RSN725_SUPER.B_B-POE360', 'RSN900_LANDERS_YER270', 'RSN953_NORTHR_MUL279',
        'RSN960_NORTHR_LOS000', 'RSN1111_KOBE_NIS000', 'RSN1116_KOBE_SHI000',
        'RSN1148_KOCAELI_ARE090', 'RSN1158_KOCAELI_DZC180', 'RSN1602_DUZCE_BOL090',
        'RSN1633_MANJIL_ABBAR--T', 'RSN1787_HECTOR_HEC090'
    ],
    'story': 'D:/GitHub/thesis/Models/MidSeismic 4Floor 12M/Multi/story.xlsx',
    'multi': 'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/Multi/story_drifts.xlsx',
    'tradition': 'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/Tradition/story_drifts.xlsx',
}

highseismic_4floor_6m = {
    'scaled_facotrs': {
        'DBE': 0.8,
        'MCE': 1,
    },
    'earthquakes': {
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
    'story': 'D:/GitHub/thesis/Models/HighSeismic 4Floor 6M/Conservative/Tradition/story.xlsx',
    'multi': 'D:/GitHub/thesis/Models/HighSeismic 4Floor 6M/Conservative/Multi/story_drifts.xlsx',
    'tradition': 'D:/GitHub/thesis/Models/HighSeismic 4Floor 6M/Conservative/Tradition/story_drifts.xlsx',
}

data = highseismic_4floor_6m
