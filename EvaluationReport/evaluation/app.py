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

    data.etabs_demand_line('blue')

    data.demand_line('green')


def v_demand(data):
    plt.figure()
    plt.xlabel('Length(m)')
    plt.ylabel('Av/s(m)')
    data.zero_line()
    data.seismic_line()
    data.v_min_line()

    data.etabs_v_demand_line('red')
    data.v_consider_vc_demand_line('blue')

    # data.v_rabar_line('blue', '傳統斷筋')
    data.v_rabar_line('green', '多點斷筋')


def tradition_flow(data):
    plt.figure()
    data.zero_line()

    data.tradition_boundary_line()
    data.min_line()

    data.etabs_demand_line('blue')

    data.rebar_line('green', '傳統斷筋')


def linearcut_flow(data):
    plt.figure()
    data.zero_line()
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
    data.demand_line('orange')

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
        lambda x: (df.loc[x // 4 * 4, '主筋效果'].values[0], x // 4))

    df = pd.DataFrame()
    for _, group in grouped:
        df = df.append(group)
    df.to_excel(f'{path} OrderbyEffect.xlsx')


def main():
    """
    test
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))

    input_file = '../data/20190518 170312 SmartCut LowSeismic 4Floor 12M.xlsx'

    path = f'{script_dir}/{input_file}'

    data = PlotDesign(path)

    # to_excel_orderby_effect(data, path)

    data.put_index(0)

    # plt.figure()
    # data.zero_line()

    # data.etabs_demand_line('blue')
    # # data.rebar_line('green')
    # data.demand_line('green')
    # data.min_line()
    # data.boundary_line()
    # data.boundary_line(0.45)

    v_demand(data)
    etabs_to_addedld_sol(data)
    tradition_flow(data)
    linearcut_flow(data)
    compare_linearcut_to_tradition(data)

    plt.show()


if __name__ == "__main__":
    main()
