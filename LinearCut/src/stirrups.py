""" calc stirrups
"""
from itertools import combinations
import numpy as np


from src.rebar import double_area, get_area, rebar_db


def _calc_vc(df):
    # pylint: disable=invalid-name
    # pylint: disable=no-member

    amin = df.groupby(['Story', 'BayID'])['StnLoc'].transform('min')
    amax = df.groupby(['Story', 'BayID'])['StnLoc'].transform('max')

    seismic_area = 2 * df['H']

    B = df['B'] * 100
    fc = df['Fc'] / 10
    fyt = df['Fy'] / 10

    # 不確定到底要不要 phi
    new_av = np.maximum.reduce([
        df['VRebar'] - 0.53 * np.sqrt(fc) * B / fyt * 0.01,
        0.2 * np.sqrt(fc) * B / fyt * 0.01,
        3.5 * B / fyt * 0.01
    ])

    df['VRebarConsiderVc'] = np.where(
        (
            (df['StnLoc'] > seismic_area + amin) &
            (df['StnLoc'] < amax - seismic_area)
        ),
        new_av,
        df['VRebar']
    )

    return df


def _calc_init_dbt_spacing(etabs_design, stirrup_rebar, v_rebar):
    # print('Start calculate stirrup spacing and size...')
    # first calc VSize to spacing
    return etabs_design.assign(VSize=stirrup_rebar[0], Spacing=(
        lambda x: double_area(stirrup_rebar[0]) / x[v_rebar]))


def _upgrade_size(etabs_design, stirrup_rebar, stirrup_spacing, v_rebar):
    # print('Start upgrade stirrup size...')

    for _, group in etabs_design.groupby(['Story', 'BayID'], sort=False):
        loc = 1

        # if spacing < min => upgrade size and recalculate spcaing
        while np.any(group['Spacing'] < stirrup_spacing[0]):
            rebar_num, rebar_size = stirrup_rebar[loc].split(sep='#')
            rebar_size = '#' + rebar_size

            if rebar_num == '2':
                # double stirrups so double * 2
                spacing = double_area(rebar_size) * 2 / group[v_rebar]
            else:
                spacing = double_area(rebar_size) / group[v_rebar]

            group = group.assign(VSize=stirrup_rebar[loc], Spacing=spacing)

            loc += 1

        etabs_design.loc[
            group.index, ['VSize', 'Spacing']] = group[['VSize', 'Spacing']]

    return etabs_design


def check_seismic_spacing(df, usr_spacing):
    """
    seismic check 15.4.3.2
    but 有效深度不確定 and 主筋直徑不確定, so 先不用
    """
    # pylint: disable=no-member

    amin = df.groupby(['Story', 'BayID'])['StnLoc'].transform('min')
    amax = df.groupby(['Story', 'BayID'])['StnLoc'].transform('max')

    seismic_area = 2 * df['H']

    # 第一個閉合箍筋距支承構材面不得超過 5 cm。閉合箍筋最大間距不得超過
    # (1)d / 4，(2)最小主鋼筋直徑之 8 倍，(3)閉合箍筋直徑之 24 倍，及(4)30 cm。
    seismic_spacing = np.minimum(
        (df['H'] - 0.065) / 4,
        df['VSize'].apply(lambda x: rebar_db(x) * 24),
    )

    # 由於 reduce 陣列不相等會造成問題，就算可以 broadcase 也是一樣。
    # 所以分成兩次
    seismic_spacing = np.minimum(
        seismic_spacing,
        0.3,
    )

    # 由於可能會遇到小梁，而小梁不用做耐震。
    # 但現在程式還無法判斷小梁，所以設立最小間距 > usr defind spacing
    seismic_spacing = np.maximum(
        seismic_spacing,
        usr_spacing[0],
    )


    spacing = (df['H'] - 0.065) / 2

    # x = df['Spacing'].copy()
    # print(df['Spacing'])

    df['Spacing'] = np.where(
        df['VSize'].str[0] == '2',
        np.minimum(spacing * 2, df['Spacing']),
        df['Spacing']
    )

    # print(df['Spacing'].equals(x))

    df['Spacing'] = np.where(
        df['VSize'].str[0] != '2',
        np.minimum(spacing, df['Spacing']),
        df['Spacing']
    )
    # print(df['Spacing'].equals(x))

    df['Spacing'] = np.where(
        (
            (
                (df['StnLoc'] < seismic_area + amin) |
                (df['StnLoc'] > amax - seismic_area)
            ) & (
                df['VSize'].str[0] == '2'
            )
        ),
        np.minimum(seismic_spacing * 2, df['Spacing']),
        df['Spacing']
    )

    df['Spacing'] = np.where(
        (
            (
                (df['StnLoc'] < seismic_area + amin) |
                (df['StnLoc'] > amax - seismic_area)
            ) & (
                df['VSize'].str[0] != '2'
            )
        ),
        np.minimum(seismic_spacing, df['Spacing']),
        df['Spacing']
    )

    # # 圍束區
    # # pandas where 與 numpy where 相反
    # # Replace values where the condition is False.
    # df['Spacing'].where(
    #     (
    #         (df['StnLoc'] > seismic_area + amin) &
    #         (df['StnLoc'] < amax - seismic_area)
    #     ),
    #     spacing
    # )

    return df


def _drop_size(rebar_size, spacing, stirrup_spacing):
    if (np.amin(spacing) / 2) >= stirrup_spacing[0]:
        return rebar_size[1:], spacing / 2
    return rebar_size, spacing


def _get_spacing(group, loc_min, loc_max):
    return group['Spacing'][(group['StnLoc'] >= loc_min) & (group['StnLoc'] <= loc_max)]


def _merge_segments(beam, etabs_design, stirrup_spacing):
    # print('Start merge to 3 segments...')

    etabs_design = etabs_design.assign(RealVSize='', RealSpacing=0)

    row = 0
    for _, group in etabs_design.groupby(['Story', 'BayID'], sort=False):
        usage = 0

        group_max = np.amax(group['StnLoc'])
        group_min = np.amin(group['StnLoc'])

        clear_span = (group_max - group_min)

        # 1/4, 2h 取大值
        side_length = max(
            clear_span * 1/4,
            2 * group['H'].iloc[0]
        )

        if 2 * side_length >= clear_span:
            side_length = clear_span * 1/4

        # x < 1/4
        left = side_length + group_min
        # x > 3/4
        right = group_max - side_length

        # rebar size with double
        rebar_size = group['VSize'].iloc[0]

        # spacing depands on loc_min, loc_max
        group_spacing = {
            '左': _get_spacing(group, group_min, left),
            '中': _get_spacing(group, left, right),
            '右': _get_spacing(group, right, group_max)
        }

        # 這裡可能會有不保守的狀況，但沒關係，其實差不多
        # 因為不是真的落在有限的點上。
        group_length = {
            '左': side_length,
            '中': (group_max - group_min) - 2 * side_length,
            '右': side_length
        }

        for loc in ('左', '中', '右'):
            loc_size = rebar_size
            loc_spacing = group_spacing[loc]

            # if double, judge size can drop or not
            if rebar_size[0] == '2':
                loc_size, loc_spacing = _drop_size(
                    loc_size, loc_spacing, stirrup_spacing)

            # all spacing reduce to usr defined
            loc_spacing_max = np.amax(
                stirrup_spacing[np.amin(loc_spacing) >= stirrup_spacing])

            # for next convinience get
            etabs_design.loc[
                loc_spacing.index, 'RealSpacing'] = loc_spacing_max

            # windows: UnicodeEncodeError so add .encode('utf-8', 'ignore').decode('utf-8')
            # remove numpy array, use default array instead
            etabs_design.loc[
                loc_spacing.index, 'RealVSize'] = loc_size

            beam.loc[row, ('箍筋', loc)] = (
                f'{loc_size}@{int(loc_spacing_max * 100)}'
            )

            beam.loc[row, ('箍筋長度', loc)] = round(group_length[loc] * 100, 3)

            usage = usage + (
                group_length[loc] / loc_spacing_max) * get_area(loc_size)

        beam.loc[row, ('箍筋量', '')] = round(usage * 10000, 3)

        row = row + 4

    return beam, etabs_design


def _calc_spacing_length(df, idx):
    idx0, idx1 = idx

    spacing = np.empty(3)
    length = np.empty(3)

    spacing[0] = df.loc[:idx0, 'UsrSpacing'].min()
    spacing[1] = df.loc[idx0:idx1, 'UsrSpacing'].min()
    spacing[2] = df.loc[idx1:, 'UsrSpacing'].min()

    length[0] = df.loc[idx0, 'StnLoc'] - df['StnLoc'].min()
    length[1] = df.loc[idx1, 'StnLoc'] - df.loc[idx0, 'StnLoc']
    length[2] = df['StnLoc'].max() - df.loc[idx1, 'StnLoc']

    return spacing, length


def _cut_3(beam, etabs_design, usr_spacing):
    """
    轉換成 usr defined spacing
    排列組合
    drop size
    輸出
    """

    def _drop_size(v_size, spacing):
        if (v_size[0] == '2') & (spacing / 2 >= usr_spacing[0]):
            return v_size[1:], usr_spacing[spacing / 2 >= usr_spacing][-1]
        return v_size, spacing

    # etabs_design['UsrSpacing'] = etabs_design['Spacing'].apply(
    #     lambda x: usr_spacing[x >= usr_spacing][-1])

    etabs_design = etabs_design.assign(
        RealVSize='',
        RealSpacing=0
    )

    row = 0
    for _, group in etabs_design.groupby(['Story', 'BayID'], sort=False):
        group = group.copy()

        # initial
        min_usage = float('Inf')

        # rebar size with double
        v_size = group['VSize'].iloc[0]

        # 如果是雙箍，代表有潛力可以 drop，所以放寬 usr spacing 變成兩倍。
        # 反正到最後也會被 drop 掉，不會超過 30。
        # 這裡其實有等值的意涵存在。
        group_spacing = np.copy(usr_spacing)

        if v_size[0] == '2':
            group_spacing = np.sort(
                np.unique(np.append(usr_spacing, usr_spacing * 2)))

        # 轉換成指定的間距
        group.loc[:, 'UsrSpacing'] = group['Spacing'].apply(
            lambda x, spacing=group_spacing: spacing[x >= spacing][-1])

        seismic_area = 2 * group['H'].iloc[0]

        combination_area = (
            (group['StnLoc'] > seismic_area + group['StnLoc'].min()) &
            (group['StnLoc'] < group['StnLoc'].max() - seismic_area)
        )

        diff_area = (
            (group['UsrSpacing'].diff() != 0) |
            (group['UsrSpacing'].diff().shift(-1) != 0)
        )

        # 梁深太深，例外處理
        # 1/4, 3/4
        if not any(combination_area):
            amin = group['StnLoc'].min()
            amax = group['StnLoc'].max()

            # x < 1/4
            combination_area.loc[
                combination_area[group['StnLoc'] >= ((amax - amin) * 1/4 + amin)].index[0]] = True
            # x > 3/4
            combination_area.loc[
                combination_area[group['StnLoc'] <= ((amax - amin) * 3/4 + amin)].index[-1]] = True

        idx = (
            group.index[combination_area][0],
            *group.index[diff_area & combination_area],
            group.index[combination_area][-1]
        )

        for idx0, idx1 in combinations(idx, 2):
            spacing, length = _calc_spacing_length(group, (idx0, idx1))

            # 簡單算法 直接四捨五入
            usage = np.sum(length / spacing)

            if usage < min_usage:
                min_usage = usage
                min_spacing = spacing
                min_length = length
                min_idx0, min_idx1 = idx0, idx1

        # group index
        index = [group.index[0], min_idx0, min_idx1, group.index[-1]]

        for i, position in enumerate(('左', '中', '右')):
            local_size, local_spacing = _drop_size(v_size, min_spacing[i])

            # 雙重保護，免得我有想錯。
            if local_spacing > usr_spacing[-1]:
                raise Exception('Spacing Exceed Limit.')

            etabs_design.loc[
                index[i]:index[i+1], 'RealVSize'] = local_size
            etabs_design.loc[
                index[i]:index[i+1], 'RealSpacing'] = local_spacing

            beam.loc[row, ('箍筋', position)] = (
                f'{local_size}@{int(local_spacing * 100)}')

            beam.loc[row, ('箍筋長度', position)] = (
                round(min_length[i] * 100, 3))

        beam.loc[row, ('箍筋量', '')] = (
            round(min_usage * get_area(v_size) * 10000, 3))

        row = row + 4

    return beam, etabs_design


def calc_stirrups(beam, etabs_design, const, consider_vc=False):
    """ calc stirrups
    """
    v_rebar = 'VRebarConsiderVc' if consider_vc else 'VRebar'

    stirrup_rebar = const['stirrup_rebar']
    stirrup_spacing = const['stirrup_spacing']

    # change m to cm
    stirrup_spacing = stirrup_spacing / 100

    etabs_design = _calc_vc(etabs_design)

    etabs_design = _calc_init_dbt_spacing(etabs_design, stirrup_rebar, v_rebar)
    etabs_design = _upgrade_size(
        etabs_design, stirrup_rebar, stirrup_spacing, v_rebar)
    etabs_design = check_seismic_spacing(etabs_design, stirrup_spacing)
    beam, etabs_design = _merge_segments(beam, etabs_design, stirrup_spacing)

    return beam, etabs_design


def calc_stirrups_3(beam, etabs_design, const, consider_vc=False):
    """ calc stirrups
    """
    v_rebar = 'VRebarConsiderVc' if consider_vc else 'VRebar'

    stirrup_rebar = const['stirrup_rebar']
    stirrup_spacing = const['stirrup_spacing']

    # change m to cm
    stirrup_spacing = stirrup_spacing / 100

    etabs_design = _calc_vc(etabs_design)

    etabs_design = _calc_init_dbt_spacing(etabs_design, stirrup_rebar, v_rebar)
    etabs_design = _upgrade_size(
        etabs_design, stirrup_rebar, stirrup_spacing, v_rebar)
    etabs_design = check_seismic_spacing(etabs_design, stirrup_spacing)
    beam, etabs_design = _cut_3(beam, etabs_design, stirrup_spacing)

    return beam, etabs_design


def _main():
    from tests.const import const
    from src.beam import init_beam
    from src.e2k import load_e2k
    from src.etabs_design import load_etabs_design, post_e2k
    from src.execution_time import Execution

    execution = Execution()

    e2k = load_e2k(const['e2k_path'])
    etabs_design = load_etabs_design(const['etabs_design_path'])
    etabs_design = post_e2k(etabs_design, e2k)
    beam = init_beam(etabs_design)

    execution.time('Stirrup Time')
    beam, dh_design = calc_stirrups(beam, etabs_design, const)
    print(beam.head())
    print(dh_design.head())
    execution.time()

    execution.time()
    beam, dh_design = calc_stirrups(beam, etabs_design, const, True)
    print(beam.head())
    print(dh_design.head())
    execution.time()

    execution.time()
    beam, dh_design = calc_stirrups_3(beam, etabs_design, const)
    print(beam.head())
    print(dh_design.head())
    execution.time()

    execution.time()
    beam, dh_design = calc_stirrups_3(beam, etabs_design, const, True)
    print(beam.head())
    print(dh_design.head())
    execution.time()


if __name__ == "__main__":
    _main()
