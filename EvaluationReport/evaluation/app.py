"""
main
"""
import os

import pandas as pd
import matplotlib.pyplot as plt

from evaluation.plot_design import PlotDesign


def etabs_to_addedld_sol(data):
    plt.figure()

    data.zero_line()
    data.min_line()

    data.etabs_demand_line('blue')

    data.demand_line('green')
    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')


def v_demand(data):
    plt.figure()
    plt.xlabel('Length(m)')
    plt.ylabel('Av/s(m)')
    data.zero_line()
    data.seismic_line()
    data.v_min_line()
    data.boundary_line(0.25)

    data.etabs_v_demand_line('blue')
    data.v_consider_vc_demand_line('blue')

    data.v_rabar_line('red', '傳統斷筋')
    data.v_rabar_line('green', '多點斷筋')


def tradition_flow(data):
    plt.figure()
    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    data.zero_line()

    data.tradition_boundary_line()
    data.min_line()

    data.etabs_demand_line('blue')

    data.rebar_line('green', '傳統斷筋')


def linearcut_flow(data):
    plt.figure()
    data.zero_line()
    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    data.min_line()
    data.boundary_line()

    data.etabs_demand_line('blue')

    data.demand_line('red')

    data.rebar_line('green', '多點斷筋')


def compare_linearcut_to_tradition(data):
    plt.figure()
    plt.xlabel('Length(m)')
    plt.ylabel(r'As($m^2$)')
    data.zero_line()
    data.min_line()
    data.boundary_line()

    data.etabs_demand_line('blue')
    data.demand_line('blue')

    data.rebar_line('red', '傳統斷筋')
    data.rebar_line('green', '多點斷筋')


def to_excel_orderby_effect(data, path):
    """
    order by effect
    """
    df = data.design.df.copy()
    tradition = data.tradition.df.copy()

    df['上下層主筋效果'] = df['主筋量'] / tradition['主筋量']
    df['主筋效果'] = (
        (df['主筋量'] + df['主筋量'].shift(periods=-3)) /
        (
            tradition['主筋量'] +
            tradition['主筋量'].shift(periods=-3)
        )
    )
    df['箍筋效果'] = df['箍筋量'] / tradition['箍筋量']

    grouped = df.groupby(
        lambda x: (df.loc[x // 4 * 4, '箍筋效果'].values[0], x // 4))

    df = pd.DataFrame()
    for _, group in grouped:
        df = df.append(group)
    df.to_excel(f'{path} OrderbyEffect.xlsx')


def main():
    """
    test
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))

    input_file = '../data/20190520 155805 SmartCut LowSeismic 4Floor 9M.xlsx'

    path = f'{script_dir}/{input_file}'

    data = PlotDesign(path)

    # to_excel_orderby_effect(data, path)

    # for index in (208, 1380, 1532, 124, 144, 1068, 72):
    #     # for index in (8, 1, 4, 40, 16, 24):
    # for index in range(0, data.design.get_len(), 4):
    # for index in (0, 620, 692, 764, 1472, 1324, 1204, 1332):
    data.put_index(12)

    # plt.figure()
    # data.zero_line()
    # plt.xlabel('Length(m)')
    # plt.ylabel('As($m^2$)')

    # # data.etabs_demand_line('blue')
    # # # data.rebar_line('green')
    # data.demand_line('green')
    # data.min_line()
    # data.boundary_line()
    # data.boundary_line(0.45)

    # v_demand(data)
    # plt.figure()
    # plt.xlabel('Length(m)')
    # plt.ylabel(r'As($m^2$)')
    # data.zero_line()
    # data.min_line()
    # data.boundary_line()

    # data.etabs_demand_line('green')
    # data.demand_line('gray')

    # data.rebar_line('gray', '傳統斷筋')
    # data.rebar_line('blue', '多點斷筋')
    # etabs_to_addedld_sol(data)
    # tradition_flow(data)
    # linearcut_flow(data)
    compare_linearcut_to_tradition(data)

    plt.show()


if __name__ == "__main__":
    main()
