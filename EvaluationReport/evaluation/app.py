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
    # data.min_line()

    line1 = data.etabs_demand_line('blue', bot=False)
    line4 = data.add_ld_line('orange', bot=False)

    line2 = data.rebar_line('red', '傳統斷筋', bot=False)
    line3 = data.rebar_line('green', '多點斷筋', bot=False)

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line4, line2, line3),
        ('Demand', 'Consider Ld', 'Tradition', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('Mid Seismic Multi-Cut vs Tradition')
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


def f4_9(data1, data2):
    plt.figure()
    plt.subplot(2, 1, 1)
    data1.zero_line()
    line1 = data1.etabs_demand_line('blue', bot=False)
    line4 = data1.add_ld_line('orange', bot=False)

    line2 = data1.rebar_line('red', '傳統斷筋', bot=False)
    line3 = data1.rebar_line('green', '多點斷筋', bot=False)

    plt.ylabel('As($m^2$)')
    # plt.xlabel('Length(m)')
    plt.legend(
        (line1, line4, line2, line3),
        ('Demand', 'Consider Ld', 'Tradition', 'Multi-Cut'),
        loc='lower right'
    )
    plt.title('(a)High Seismic Case')

    plt.subplot(2, 1, 2)
    data2.zero_line()

    line1 = data2.etabs_demand_line('blue', bot=False)
    line4 = data2.add_ld_line('orange', bot=False)

    line2 = data2.rebar_line('red', '傳統斷筋', bot=False)
    line3 = data2.rebar_line('green', '多點斷筋', bot=False)

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line4, line2, line3),
        ('Demand', 'Consider Ld', 'Tradition', 'Multi-Cut'),
        loc='lower right'
    )
    plt.title('(b)Mid Seismic Case')
    plt.tight_layout()


def f4_10():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    data1 = PlotDesign(
        f'{script_dir}/../data/MidSeismic 4Floor 6M.xlsx')
    data2 = PlotDesign(
        f'{script_dir}/../data/MidSeismic 4Floor 9M.xlsx')
    data3 = PlotDesign(
        f'{script_dir}/../data/MidSeismic 4Floor 12M.xlsx')

    data1.put_index(24)
    data2.put_index(24)
    data3.put_index(24)

    plt.figure(figsize=(6.4, 8))

    plt.subplot(3, 1, 1)
    data1.zero_line()

    line1 = data1.etabs_demand_line('blue', top=False)
    line4 = data1.add_ld_line('orange', top=False)

    line2 = data1.rebar_line('red', '傳統斷筋', top=False)
    line3 = data1.rebar_line('green', '多點斷筋', top=False)

    plt.ylabel('As($m^2$)')
    plt.xlabel('Length(m)')
    plt.legend(
        (line1, line4, line2, line3),
        ('Demand', 'Consider Ld', 'Tradition', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('(a)Beam Length 6m Case')

    plt.subplot(3, 1, 2)
    data2.zero_line()

    line1 = data2.etabs_demand_line('blue', top=False)
    line4 = data2.add_ld_line('orange', top=False)

    line2 = data2.rebar_line('red', '傳統斷筋', top=False)
    line3 = data2.rebar_line('green', '多點斷筋', top=False)

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line4, line2, line3),
        ('Demand', 'Consider Ld', 'Tradition', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('(b)Beam Length 9m Case')

    plt.subplot(3, 1, 3)
    data3.zero_line()

    line1 = data3.etabs_demand_line('blue', top=False)
    line4 = data3.add_ld_line('orange', top=False)

    line2 = data3.rebar_line('red', '傳統斷筋', top=False)
    line3 = data3.rebar_line('green', '多點斷筋', top=False)

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line4, line2, line3),
        ('Demand', 'Consider Ld', 'Tradition', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('(c)Beam Length 12m Case')

    plt.tight_layout()


def f4_11():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    data1 = PlotDesign(
        f'{script_dir}/../data/HighSeismic 4Floor 9M.xlsx')
    data2 = PlotDesign(
        f'{script_dir}/../data/MidSeismic 4Floor 9M.xlsx')
    data3 = PlotDesign(
        f'{script_dir}/../data/LowSeismic 4Floor 9M.xlsx')

    data1.put_index(24)
    data2.put_index(24)
    data3.put_index(24)

    plt.figure(figsize=(6.4, 8))

    plt.subplot(3, 1, 1)
    data1.zero_line()

    line1 = data1.etabs_demand_line('blue', top=False)
    line4 = data1.add_ld_line('orange', top=False)

    line2 = data1.rebar_line('red', '傳統斷筋', top=False)
    line3 = data1.rebar_line('green', '多點斷筋', top=False)

    plt.ylabel('As($m^2$)')
    plt.xlabel('Length(m)')
    plt.legend(
        (line1, line4, line2, line3),
        ('Demand', 'Consider Ld', 'Tradition', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('(a)High Seismic Case')

    plt.subplot(3, 1, 2)
    data2.zero_line()

    line1 = data2.etabs_demand_line('blue', top=False)
    line4 = data2.add_ld_line('orange', top=False)

    line2 = data2.rebar_line('red', '傳統斷筋', top=False)
    line3 = data2.rebar_line('green', '多點斷筋', top=False)

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line4, line2, line3),
        ('Demand', 'Consider Ld', 'Tradition', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('(b)Mid Seismic Case')

    plt.subplot(3, 1, 3)
    data3.zero_line()

    line1 = data3.etabs_demand_line('blue', top=False)
    line4 = data3.add_ld_line('orange', top=False)

    line2 = data3.rebar_line('red', '傳統斷筋', top=False)
    line3 = data3.rebar_line('green', '多點斷筋', top=False)

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line4, line2, line3),
        ('Demand', 'Consider Ld', 'Tradition', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('(c)Low Seismic Case')

    plt.tight_layout()


def main():
    """
    test
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))

    data1 = PlotDesign(
        f'{script_dir}/../data/HighSeismic 4Floor 9M.xlsx')
    data2 = PlotDesign(
        f'{script_dir}/../data/MidSeismic 4Floor 9M.xlsx')
    data3 = PlotDesign(
        f'{script_dir}/../data/LowSeismic 4Floor 9M.xlsx')

    data1.put_index(24)
    data2.put_index(24)
    data3.put_index(24)

    f4_11()

    # data3.put_index(24)

    # plt.figure()
    # data1.zero_line()
    # data1.boundary_line(1/3)

    # data1.etabs_demand_line('gray')
    # data1.add_ld_line('gray', label='Consider $l_d$')
    # data2.add_ld_line('gray', label='Consider $l_d$')

    # line2 = data1.rebar_line('orange', '傳統斷筋')
    # line3 = data1.rebar_line('blue', '多點斷筋')
    # line2 = data2.rebar_line('red', '傳統斷筋')
    # line3 = data2.rebar_line('green', '多點斷筋')

    # plt.xlabel('Length(m)')
    # plt.ylabel('As($m^2$)')
    # plt.subplots_adjust(left=0.15)

    # to_excel_orderby_effect(
    #     data1,
    #     f'{script_dir}/../data/20190520 104202 SmartCut 欣詮'
    # )

    # etabs_to_addedld_sol(data1)
    # v_multicut_compare_tradition(data1)
    # v_multicut_compare_tradition(data2)
    # v_multicut_compare_tradition(data3)
    # tradition_flow(data1)
    # multicut_flow(data1)
    # multicut_compare_tradition(data1)
    # tradition_flow(data2)

    # etabs_to_addedld_sol(data2)
    # multicut_compare_tradition(data2)
    # multicut_compare_tradition(data3)

    # v_workflow(data1)

    plt.show()


if __name__ == "__main__":
    main()
