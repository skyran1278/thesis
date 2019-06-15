"""
main
"""
# pylint: disable=missing-docstring
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
        ('Demand', 'Demand-Allowed-Cut', 'Consider $l_d$'),
        loc='best'
    )
    plt.title('Consider Ld Demand')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


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
        loc='best'
    )
    plt.title('Multi-Cut Workflow')
    plt.grid(True, which='both', linestyle=':')


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
        loc='best'
    )
    plt.title('Multi-Cut vs Tradition')
    plt.grid(True, which='both', linestyle=':')


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
        loc='best'
    )
    plt.title('Tradition Workflow')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def multicut_flow(data):
    plt.figure()
    data.zero_line()

    data.min_line()
    data.boundary_line(0.1)
    data.boundary_line(0.45)

    line1 = data.etabs_demand_line('blue')
    # line2 = data.rebar_number_line('red')

    line2 = data.add_ld_line('red')

    line3 = data.rebar_line('green', '多點斷筋')

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Consider $l_d$', 'Multi-Cut'),
        loc='best',
    )
    plt.title('Multi-Cut Workflow')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def multicut_compare_tradition(data):
    plt.figure()
    data.zero_line()
    # data.min_line()

    line1 = data.etabs_demand_line('blue')
    line4 = data.add_ld_line('orange')

    line2 = data.rebar_line('red', '傳統斷筋')
    line3 = data.rebar_line('green', '多點斷筋')

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line4, line2, line3),
        ('Demand', 'Consider Ld', 'Tradition', 'Multi-Cut'),
        loc='best'
    )
    plt.title('Multi-Cut vs Tradition')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


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


def f3_1():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    data = PlotDesign(
        f'{script_dir}/../data/LowSeismic 4Floor 12M.xlsx')

    data.put_index(0)

    plt.figure()

    data.zero_line(linestyle='-')
    # data.min_line()

    line1 = data.etabs_demand_line('gray', bot=False, linestyle='--')
    line2 = data.etabs_demand_line('gray', top=False, linestyle='-.')
    # line2 = data.rebar_number_line('red')

    # line3 = data.add_ld_line('green', label='Consider $l_d$')

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line2),
        ('Top', 'Bottom'),
        loc='best'
    )
    plt.title('Beam Reinforcement')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def f4_():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    data1 = PlotDesign(
        f'{script_dir}/../data/HighSeismic 4Floor 6M.xlsx')
    data2 = PlotDesign(
        f'{script_dir}/../data/MidSeismic 4Floor 6M.xlsx')

    data1.put_index(24)
    data2.put_index(24)

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
    plt.grid(True, which='both', linestyle=':')

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
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def f4_8():
    data1 = PlotDesign(
        'D:/GitHub/thesis/Models/MidSeismic 4Floor 6M/20190614 154236 Cut 2.xlsx')
    data2 = PlotDesign(
        'D:/GitHub/thesis/Models/MidSeismic 4Floor 9M/20190614 154307 Cut 2.xlsx')
    data3 = PlotDesign(
        'D:/GitHub/thesis/Models/MidSeismic 4Floor 12M/20190614 154334 Cut 2.xlsx')

    data1.put_index(24)
    data2.put_index(24)
    data3.put_index(24)

    plt.figure(figsize=(6.4, 8.6))

    plt.subplot(3, 1, 1)
    data1.zero_line()

    line1 = data1.etabs_demand_line('blue', top=False)

    line2 = data1.rebar_line('red', '傳統斷筋', top=False)
    line3 = data1.rebar_line('green', '多點斷筋', top=False)

    plt.ylabel('As($m^2$)')
    plt.xlabel('Length(m)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Tradition', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('(a)Mid Seismic Beam Length 6m Case')
    plt.grid(True, which='both', linestyle=':')

    plt.subplot(3, 1, 2)
    data2.zero_line()

    line1 = data2.etabs_demand_line('blue', top=False)

    line2 = data2.rebar_line('red', '傳統斷筋', top=False)
    line3 = data2.rebar_line('green', '多點斷筋', top=False)

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Tradition', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('(b)Mid Seismic Beam Length 9m Case')
    plt.grid(True, which='both', linestyle=':')

    plt.subplot(3, 1, 3)
    data3.zero_line()
    plt.grid(True, which='both', linestyle=':')

    line1 = data3.etabs_demand_line('blue', top=False)

    line2 = data3.rebar_line('red', '傳統斷筋', top=False)
    line3 = data3.rebar_line('green', '多點斷筋', top=False)

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Tradition', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('(c)Mid Seismic Beam Length 12m Case')
    plt.grid(True, which='both', linestyle=':')

    plt.tight_layout()


def f4_9():
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

    line2 = data1.rebar_line('red', '傳統斷筋', top=False)
    line3 = data1.rebar_line('green', '多點斷筋', top=False)

    plt.ylabel('As($m^2$)')
    plt.xlabel('Length(m)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Tradition', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('(a)High Seismic Case')
    plt.grid(True, which='both', linestyle=':')

    plt.subplot(3, 1, 2)
    data2.zero_line()

    line1 = data2.etabs_demand_line('blue', top=False)

    line2 = data2.rebar_line('red', '傳統斷筋', top=False)
    line3 = data2.rebar_line('green', '多點斷筋', top=False)

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Tradition', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('(b)Mid Seismic Case')
    plt.grid(True, which='both', linestyle=':')

    plt.subplot(3, 1, 3)
    data3.zero_line()

    line1 = data3.etabs_demand_line('blue', top=False)

    line2 = data3.rebar_line('red', '傳統斷筋', top=False)
    line3 = data3.rebar_line('green', '多點斷筋', top=False)

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Tradition', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('(c)Low Seismic Case')
    plt.grid(True, which='both', linestyle=':')

    plt.tight_layout()


def f3_3and3_4():
    data1 = PlotDesign(
        'D:/GitHub/thesis/Models/HighSeismic 4Floor 6M/Conservative/20190614 221325 Cut 29 無退縮.xlsx')
    data1.put_index(4)
    multicut_flow(data1)
    tradition_flow(data1)

    data1 = PlotDesign(
        'D:/GitHub/thesis/Models/HighSeismic 4Floor 6M/Conservative/20190614 203005 Cut 29.xlsx')
    data1.put_index(4)
    multicut_flow(data1)
    tradition_flow(data1)


def f3_5and3_6and3_7():
    data = PlotDesign(
        'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/20190615 104919 Cut 2 Procedure B.xlsx')
    data.put_index(0)

    plt.figure()
    data.zero_line()
    data.min_line()

    line1 = data.etabs_demand_line('blue')
    line2 = data.rebar_number_line('red')

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line2),
        ('Demand', 'Demand-Allowed-Cut'),
        loc='best'
    )
    plt.title('Demand-Allowed-Cut')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()

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
        ('Demand', 'Demand-Allowed-Cut', 'Consider $l_d$'),
        loc='best'
    )
    plt.title('Consider Ld Demand')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()

    multicut_flow(data)


def f4_1():
    data = PlotDesign(
        'D:/GitHub/thesis/EvaluationReport/data/20190520 104202 SmartCut 欣詮.xlsx')
    data.put_index(0)

    plt.figure()
    data.zero_line()
    data.min_line()

    line1 = data.etabs_demand_line('blue')
    # line2 = data.rebar_number_line('red')

    line2 = data.rebar_line('green', '多點斷筋')

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line2),
        ('Demand', 'Min: 2 Reinforcement'),
        loc='best'
    )
    plt.title('Demand less than code minimum limit')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def f4_3():
    data = PlotDesign(
        'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/20190615 103351 Cut 2.xlsx')
    data.put_index(0)

    plt.figure()

    data.zero_line()
    data.min_line()

    line1 = data.etabs_demand_line('blue')
    # line2 = data.rebar_number_line('red')

    line3 = data.add_ld_line('green', label='Consider $l_d$')

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line3),
        ('Demand', 'Consider $l_d$'),
        loc='best'
    )
    plt.title('Consider Ld Demand')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def f4_4():
    data = PlotDesign(
        'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/20190615 103351 Cut 2.xlsx')
    data.put_index(0)

    plt.figure()
    data.zero_line()
    # data.min_line(top=False)

    line1 = data.etabs_demand_line('blue', top=False)

    line2 = data.rebar_line('red', '傳統斷筋', top=False)
    line3 = data.rebar_line('green', '多點斷筋', top=False)

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Tradition', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('Multi-Cut vs Tradition')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def f4_5():
    data = PlotDesign(
        'D:/GitHub/thesis/Models/LowSeismic 4Floor 9M/20190614 154143 Cut 2.xlsx')
    data.put_index(12)

    plt.figure()
    data.zero_line()
    # data.min_line(top=False)

    line1 = data.etabs_demand_line('blue', top=False)

    line2 = data.rebar_line('red', '傳統斷筋', top=False)
    line3 = data.rebar_line('green', '多點斷筋', top=False)

    plt.xlabel('Length(m)')
    plt.ylabel('As($m^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Tradition', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('Multi-Cut vs Tradition')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def f4_6():
    data = PlotDesign(
        'D:/GitHub/thesis/Models/HighSeismic 4Floor 9M/20190614 154041 Cut 2.xlsx')
    data.put_index(28)

    plt.figure()
    data.zero_line()
    data.min_line()

    line1 = data.etabs_demand_line('blue')

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
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def f3_8():
    data = PlotDesign(
        'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/20190615 103351 Cut 2.xlsx')
    data.put_index(0)

    plt.figure()
    data.zero_line()
    data.seismic_line()
    data.v_min_line()

    line1 = data.etabs_v_demand_line('blue')
    # line2 = data.v_consider_vc_demand_line('red')

    line3 = data.v_rabar_line('green', '多點斷筋')

    plt.xlabel('Length(m)')
    plt.ylabel('Av/s(m)')
    plt.legend(
        (line1, line3),
        ('$V_u$', 'Multi-Cut'),
        loc='upper left'
    )
    plt.title('Multi-Cut Workflow')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def f4_7():
    data = PlotDesign(
        'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/20190615 103351 Cut 2.xlsx')
    data.put_index(0)

    plt.figure()
    data.zero_line()
    data.seismic_line()
    data.v_min_line()

    line1 = data.etabs_v_demand_line('blue')
    line2 = data.v_rabar_line('red', '傳統斷筋')
    line3 = data.v_rabar_line('green', '多點斷筋')

    plt.xlabel('Length(m)')
    plt.ylabel('Av/s(m)')
    plt.legend(
        (line1, line2, line3),
        ('Consider $V_c$ Demand', 'Tradition', 'Multi-Cut'),
        loc='best'
    )

    plt.title('Multi-Cut Workflow')
    plt.grid(True, which='both', linestyle=':')


def main():
    """
    test
    """
    f4_9()

    # script_dir = os.path.dirname(os.path.abspath(__file__))

    datas = [
        'D:/GitHub/thesis/Models/HighSeismic 4Floor 6M/Conservative/20190614 154022 Cut 2.xlsx',
        'D:/GitHub/thesis/Models/MidSeismic 4Floor 6M/20190614 154236 Cut 2.xlsx',
        'D:/GitHub/thesis/Models/LowSeismic 4Floor 6M/20190614 154117 Cut 2.xlsx',
        'D:/GitHub/thesis/Models/HighSeismic 4Floor 9M/20190614 154041 Cut 2.xlsx',
        'D:/GitHub/thesis/Models/MidSeismic 4Floor 9M/20190614 154307 Cut 2.xlsx',
        'D:/GitHub/thesis/Models/LowSeismic 4Floor 9M/20190614 154143 Cut 2.xlsx',
        'D:/GitHub/thesis/Models/HighSeismic 4Floor 12M/20190614 154055 Cut 2.xlsx',
        'D:/GitHub/thesis/Models/MidSeismic 4Floor 12M/20190614 154334 Cut 2.xlsx',
        'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/20190615 103351 Cut 2.xlsx'
    ]

    # data1 = PlotDesign(
    #     'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/20190615 103351 Cut 2.xlsx')
    # for index in range(0, data1.design.get_len(), 4):
    #     data1.put_index(index)
    #     multicut_flow(data1)
    #     # tradition_flow(data1)
    #     multicut_compare_tradition(data1)

    # v_workflow(data1)
    # for data in datas:
    #     data1 = PlotDesign(data)
    #     # for index in range(0, data1.design.get_len(), 24):
    #     data1.put_index(0)
    #     multicut_flow(data1)
    #     data1 = PlotDesign(data)
    # # data2 = PlotDesign(
    # #     f'{script_dir}/../data/MidSeismic 4Floor 9M.xlsx')
    # # data3 = PlotDesign(
    # #     f'{script_dir}/../data/LowSeismic 4Floor 9M.xlsx')

    # data2.put_index(24)
    # data3.put_index(24)

    # f4_11()
    # f3_1()
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
    # plt.tight_layout()

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
