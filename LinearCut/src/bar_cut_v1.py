"""
smart cut
"""
from itertools import combinations, product

import numpy as np
from scipy.signal import find_peaks


from src.bar_functions import concat_num_size, num_to_1st_2nd
from src.rebar import rebar_area, get_diameter


def cut_multiple(df, loc, boundary, group_num=5):
    """
    multiple cut
    """
    if group_num <= 3:
        return cut_3(df, loc, boundary)

    col = 'Bar' + loc + 'Num'

    # initial
    min_usage = float('Inf')
    num = np.empty(group_num)
    length = np.empty(group_num)

    amin = df['StnLoc'].min()
    amax = df['StnLoc'].max()

    boundarys = (
        (amax - amin) * boundary['left'][0] + amin,
        (amax - amin) * boundary['right'][1] + amin,
    )

    combination_area = (
        (df['StnLoc'] > boundarys[0]) &
        (df['StnLoc'] < boundarys[1])
    )

    diff_area = (
        (df[col].diff() != 0) |
        (df[col].diff().shift(-1) != 0)
    )

    idxs = np.unique((
        df.index[combination_area][0],
        *df.index[combination_area][0:-1:10],
        *df.index[diff_area & combination_area],
        df.index[combination_area][-1]
    ))

    # idxs = df.index[combination_area]

    for idx in combinations(idxs, group_num - 1):
        idx = (df['StnLoc'].idxmin(), *idx, df['StnLoc'].idxmax())
        new_idx = list(idx)
        i = 0

        for left, mid, right in zip(idx, idx[1:], idx[2:]):
            num[i] = df.loc[left:mid, col].max()
            num[i + 1] = df.loc[mid:right, col].max()

            new_idx[i + 1] = calc_mid_idx(df, loc, left, mid, right)
            # cancel 執行 this for loop
            if new_idx[i + 1] < new_idx[i]:
                break
            i += 1

        # # cause cancel, so need to continue next
        else:
            i = 0
            for id0, id1 in zip(new_idx, new_idx[1:]):
                length[i] = df.loc[id1, 'StnLoc'] - df.loc[id0, 'StnLoc']
                i += 1

            usage = np.sum(num * length)

            if usage < min_usage:
                min_usage = usage
                min_num = num.copy()
                min_length = length.copy()

    # for local maxima
    # for local minima
    # input should be numpy array
    # return tuple
    incompatible = ((min_usage == float('Inf')) or (
        (find_peaks(min_num)[0].size > 0) &
        (find_peaks(-min_num)[0].size > 0)
    ))

    if incompatible:
        print(
            f'{df["Story"].iat[0]} {df["BayID"].iat[0]} '
            f'{loc} Retreat to {group_num - 2} cut'
        )
        return cut_multiple(df, loc, boundary, group_num - 1)

    return min_num, min_length, min_usage


def calc_mid_idx(df, loc, left, mid, right):
    # pylint: disable=invalid-name
    maxstress_id = df.loc[left:right, 'As' + loc].idxmax()

    num_left = df.loc[left:mid, 'Bar' + loc + 'Num'].max()
    num_right = df.loc[mid:right, 'Bar' + loc + 'Num'].max()

    ld = df.at[maxstress_id, loc + 'Ld']
    db = get_diameter(df.at[mid, f'Bar{loc}Size'])
    if df.at[mid, f'Bar{loc}2nd'] == 0:
        d = (
            df.at[mid, 'H'] -
            0.04 -
            get_diameter(df.at[mid, 'RealVSize']) -
            0.5 * db
        )
    else:
        d = (
            df.at[mid, 'H'] -
            0.04 -
            get_diameter(df.at[mid, 'RealVSize']) -
            1.5 * db
        )
    max_d_12db = (
        abs(df.at[mid, 'StnLoc'] - df.at[maxstress_id, 'StnLoc']) +
        max(12 * db, d)
    )

    if num_left > num_right:
        station = max(ld, max_d_12db) + df.at[maxstress_id, 'StnLoc']
        idx = df.index[df['StnLoc'].gt(station)]
        if idx.empty or idx[0] >= right:
            return -1
        return idx[0]

    if num_left < num_right:
        station = df.at[maxstress_id, 'StnLoc'] - max(ld, max_d_12db)
        idx = df.index[df['StnLoc'].lt(station)]
        if idx.empty or idx[-1] <= left:
            return -1
        return idx[-1]
    return mid


def cut_3(df, loc, boundary):
    """
    cut 3, depands on boundary, ex: 0.1~0.45, 0.55~0.9
    """

    col = 'Bar' + loc + 'Num'

    # initial
    idxs = {}
    min_usage = float('Inf')
    num = np.empty(3)
    length = np.empty(3)

    amin = df['StnLoc'].min()
    amax = df['StnLoc'].max()

    for index in boundary:
        boundarys = (amax - amin) * boundary[index] + amin

        boundary_area = (
            (df['StnLoc'] >= boundarys[0]) &
            (df['StnLoc'] <= boundarys[1])
        )

        # diff_area = (
        #     (df[col].diff() != 0) |
        #     (df[col].diff().shift(-1) != 0)
        # )

        # idxs[index] = (
        #     df.index[boundary_area][0],
        #     *df.index[diff_area & boundary_area],
        #     df.index[boundary_area][-1]
        # )

        idxs[index] = df.index[boundary_area]

    for idx in product(idxs['left'], idxs['right']):
        num[0] = df.loc[:idx[0], col].max()
        num[1] = df.loc[idx[0]:idx[1], col].max()
        num[2] = df.loc[idx[1]:, col].max()

        idx0 = calc_mid_idx(df, loc, df['StnLoc'].idxmin(), idx[0], idx[1])
        if idx0 <= df['StnLoc'].idxmin():
            continue
        idx1 = calc_mid_idx(df, loc, idx[0], idx[1], df['StnLoc'].idxmax())
        if idx1 <= idx0:
            continue

        length[0] = df.loc[idx0, 'StnLoc'] - df['StnLoc'].min()
        length[1] = df.loc[idx1, 'StnLoc'] - df.loc[idx0, 'StnLoc']
        length[2] = df['StnLoc'].max() - df.loc[idx1, 'StnLoc']

        usage = np.sum(num * length)

        if usage < min_usage:
            min_usage = usage
            # by reference, so deep copy
            min_num = num.copy()
            min_length = length.copy()

    # if all none, use max
    if min_usage == float('Inf'):
        span = df['StnLoc'].max() - df['StnLoc'].min()

        min_num = np.full(3, df[col].max())
        min_length = np.full(3, span / 3)
        min_usage = np.sum(num * length)

    return min_num, min_length, min_usage


def cut_optimization(beam, etabs_design, const, group_num=3):
    """
    cut 3 or 5, optimization
    """
    rebar = const['rebar']

    output_loc = {
        'Top': {
            'START_LOC': 0,
            'TO_2nd': 1
        },
        'Bot': {
            'START_LOC': 3,
            'TO_2nd': -1
        }
    }

    for loc in rebar:
        row = output_loc[loc]['START_LOC']
        to_2nd = output_loc[loc]['TO_2nd']

        for _, group in etabs_design.groupby(['Story', 'BayID'], sort=False):
            output_num = {}
            output_length = {}
            # group capacity and size
            cap = group.at[group.index[0], 'Bar' + loc + 'Cap']
            size = group.at[group.index[0], 'Bar' + loc + 'Size']

            num, length, usage = cut_multiple(
                group, loc, const['boundary'], group_num)
            # group, 'Bar' + loc + 'Num', const['boundary'], group_num)

            # else:
            if len(num) % 2 == 1:
                mid = len(num) // 2
                output_num['中'] = num_to_1st_2nd(num[mid], cap)
                output_length['中'] = length[mid]

            for i in range(len(num) // 2):
                output_num[f'左{i+1}'] = num_to_1st_2nd(num[i], cap)
                output_length[f'左{i+1}'] = length[i]
                output_num[f'右{i+1}'] = num_to_1st_2nd(num[-(i+1)], cap)
                output_length[f'右{i+1}'] = length[-(i+1)]

            for col in output_num:
                loc_1st, loc_2nd = output_num[col]
                loc_length = output_length[col]
                beam.at[row, ('主筋', col)] = concat_num_size(
                    loc_1st, size)
                beam.at[row, ('主筋長度', col)] = round(loc_length * 100, 3)
                beam.at[row + to_2nd, ('主筋', col)
                        ] = concat_num_size(loc_2nd, size)

            beam.at[row, ('主筋量', '')] = usage * rebar_area(size) * 1000000

            row += 4

    return beam


def main():
    """
    test
    """
    from src.execution_time import Execution
    from tests.const import const
    from src.beam import init_beam
    from src.e2k import load_e2k
    from src.etabs_design import load_etabs_design, post_e2k
    from src.stirrups import calc_stirrups
    from src.bar_size_num import calc_db
    from src.bar_ld import calc_ld, add_ld

    execution = Execution()

    e2k = load_e2k(const['e2k_path'])
    etabs_design = load_etabs_design(const['etabs_design_path'])
    etabs_design = post_e2k(etabs_design, e2k)
    beam = init_beam(etabs_design)
    beam, etabs_design = calc_stirrups(beam, etabs_design, const)
    etabs_design = calc_db('BayID', etabs_design, const)
    etabs_design = calc_ld(etabs_design, const)
    # etabs_design = add_ld(etabs_design, 'Ld', const)

    execution.time('cut 3')
    # beam = output_3(beam, etabs_design, const)
    beam = cut_optimization(beam, etabs_design, const, 3)
    print(beam.head())
    beam = cut_optimization(beam, etabs_design, const, 5)
    print(beam.head())
    execution.time('cut 3')


if __name__ == '__main__':
    main()
