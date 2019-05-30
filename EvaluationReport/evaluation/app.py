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

    line1 = data.etabs_demand_line('blue')
    line2 = data.rebar_number_line('red')

    line3 = data.add_ld_line('green', label='Consider $l_d$')

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Demand Change To Rebar Number', 'Consider $l_d$'),
        loc='upper left'
    )
    plt.title('Moment Demand and Add Ld Demand')
    plt.subplots_adjust(left=0.15)


def v_workflow(data):
    plt.figure()
    data.zero_line()
    data.seismic_line()
    data.v_min_line()

    line1 = data.etabs_v_demand_line('blue')
    line2 = data.v_consider_vc_demand_line('red')

    line3 = data.v_rabar_line('green', '多點斷筋')

    plt.xlabel('Length(m)')
    plt.ylabel('Av/s(m)')
    plt.legend(
        (line1, line2, line3),
        ('$V_u$', 'Consider $V_c$ Demand', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('Multi-Cut Workflow')


def v_multicut_compare_tradition(data):
    plt.figure()
    data.zero_line()
    data.seismic_line()
    data.v_min_line()
    data.boundary_line(0.25)

    line1 = data.v_consider_vc_demand_line('blue')

    line2 = data.v_rabar_line('red', '傳統斷筋')
    line3 = data.v_rabar_line('green', '多點斷筋')

    plt.xlabel('Length(m)')
    plt.ylabel('Av/s(m)')
    plt.legend(
        (line1, line2, line3),
        ('Consider $V_c$ Demand', 'Tradition', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('Multi-Cut vs Tradition')


def tradition_flow(data):
    plt.figure()

    data.zero_line()
    data.min_line()
    data.tradition_boundary_line()

    line1 = data.etabs_demand_line('blue')

    line2 = data.rebar_line('green', '傳統斷筋')

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line2),
        ('Demand', 'Tradition'),
        loc='upper left'
    )
    plt.title('Tradition Workflow')
    plt.subplots_adjust(left=0.15)


def multicut_flow(data):
    plt.figure()
    data.zero_line()

    data.min_line()
    data.boundary_line(0.1)
    data.boundary_line(0.45)

    line1 = data.etabs_demand_line('blue')

    line2 = data.add_ld_line('red')

    line3 = data.rebar_line('green', '多點斷筋')

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Consider $l_d$', 'Multi-Cut'),
        loc='upper left',
    )
    plt.title('Multi-Cut Workflow')
    plt.subplots_adjust(left=0.15)


def multicut_compare_tradition(data):
    plt.figure()
    data.zero_line()
    data.min_line()

    line1 = data.etabs_demand_line('blue')
    data.add_ld_line('blue')

    line2 = data.rebar_line('red', '傳統斷筋')
    line3 = data.rebar_line('green', '多點斷筋')

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Tradition', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('Multi-Cut vs Tradition')
    plt.subplots_adjust(left=0.15)


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

    data1 = PlotDesign(
        f'{script_dir}/../data/LowSeismic 4Floor 12M.xlsx')

    data1.put_index(0)

    # to_excel_orderby_effect(
    #     data1,
    #     f'{script_dir}/../data/20190520 104202 SmartCut 欣詮'
    # )

    etabs_to_addedld_sol(data1)
    tradition_flow(data1)
    multicut_flow(data1)
    multicut_compare_tradition(data1)

    v_workflow(data1)
    v_multicut_compare_tradition(data1)

    plt.show()


if __name__ == "__main__":
    main()
