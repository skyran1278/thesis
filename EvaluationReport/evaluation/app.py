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
    plt.ylabel('As($cm^2$)')
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
    plt.ylabel('Av/s(cm)')
    plt.legend(
        (line1, line2, line3),
        ('$V_u$', 'Consider $V_c$ Demand', 'Optimization'),
        loc='best'
    )
    plt.title('Optimization Workflow')
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
    plt.ylabel('Av/s(cm)')
    plt.legend(
        (line1, line2, line3),
        ('Consider $V_c$ Demand', 'Convention', 'Optimization'),
        loc='best'
    )
    plt.title('Optimization vs Convention')
    plt.grid(True, which='both', linestyle=':')


def tradition_flow(data):
    plt.figure()

    data.zero_line()
    data.min_line()
    data.tradition_boundary_line()

    line1 = data.etabs_demand_line('blue')

    line2 = data.rebar_line('green', '傳統斷筋')

    plt.xlabel('Length(m)')
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line2),
        ('Demand', 'Convention'),
        loc='best'
    )
    plt.title('Convention Workflow')
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
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Consider $l_d$', 'Optimization'),
        loc='best',
    )
    plt.title('Optimization Workflow')
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
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line4, line2, line3),
        ('Demand', 'Consider Ld', 'Convention', 'Optimization'),
        loc='best'
    )
    plt.title('Optimization vs Convention')
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
    data = PlotDesign(
        'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/20190615 103351 Cut 2.xlsx')

    data.put_index(0)

    plt.figure()

    data.zero_line(linestyle='-')
    # data.min_line()

    line1 = data.etabs_demand_line('gray', bot=False, linestyle='--')
    line2 = data.etabs_demand_line('gray', top=False, linestyle='-.')
    # line2 = data.rebar_number_line('red')

    # line3 = data.add_ld_line('green', label='Consider $l_d$')

    plt.xlabel('Length(m)')
    plt.ylabel('As($cm^2$)')
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

    plt.ylabel('As($cm^2$)')
    # plt.xlabel('Length(m)')
    plt.legend(
        (line1, line4, line2, line3),
        ('Demand', 'Consider Ld', 'Convention', 'Optimization'),
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
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line4, line2, line3),
        ('Demand', 'Consider Ld', 'Convention', 'Optimization'),
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

    plt.ylabel('As($cm^2$)')
    plt.xlabel('Length(m)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Convention', 'Optimization'),
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
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Convention', 'Optimization'),
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
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Convention', 'Optimization'),
        loc='upper left'
    )
    plt.title('(c)Mid Seismic Beam Length 12m Case')
    plt.grid(True, which='both', linestyle=':')

    plt.tight_layout()


def f4_9():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    data1 = PlotDesign(
        'D:/GitHub/thesis/Models/HighSeismic 4Floor 9M/20190614 154041 Cut 2.xlsx')
    data2 = PlotDesign(
        'D:/GitHub/thesis/Models/MidSeismic 4Floor 9M/20190614 154307 Cut 2.xlsx')
    data3 = PlotDesign(
        'D:/GitHub/thesis/Models/LowSeismic 4Floor 9M/20190614 154143 Cut 2.xlsx')

    data1.put_index(24)
    data2.put_index(24)
    data3.put_index(24)

    plt.figure(figsize=(6.4, 8.6))

    plt.subplot(3, 1, 1)
    data1.zero_line()

    line1 = data1.etabs_demand_line('blue', top=False)

    line2 = data1.rebar_line('red', '傳統斷筋', top=False)
    line3 = data1.rebar_line('green', '多點斷筋', top=False)

    plt.ylabel('As($cm^2$)')
    plt.xlabel('Length(m)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Convention', 'Optimization'),
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
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Convention', 'Optimization'),
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
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Convention', 'Optimization'),
        loc='upper left'
    )
    plt.title('(c)Low Seismic Case')
    plt.grid(True, which='both', linestyle=':')

    plt.tight_layout()


def f4_10():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    data1 = PlotDesign(
        'D:/GitHub/thesis/Models/HighSeismic 4Floor 12M/20190614 154055 Cut 2.xlsx')
    data2 = PlotDesign(
        'D:/GitHub/thesis/Models/MidSeismic 4Floor 12M/20190614 154334 Cut 2.xlsx')
    data3 = PlotDesign(
        'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/20190615 103351 Cut 2.xlsx')

    data1.put_index(36)
    data2.put_index(36)
    data3.put_index(36)

    plt.figure(figsize=(6.4, 8.6))

    plt.subplot(3, 1, 1)
    data1.zero_line()

    line1 = data1.etabs_demand_line('blue', top=False)

    line2 = data1.rebar_line('red', '傳統斷筋', top=False)
    line3 = data1.rebar_line('green', '多點斷筋', top=False)

    plt.ylabel('As($cm^2$)')
    plt.xlabel('Length(m)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Convention', 'Optimization'),
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
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Convention', 'Optimization'),
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
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Convention', 'Optimization'),
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

def f3_5():
    data = PlotDesign(
        'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/20190615 103351 Cut 2.xlsx')
    data.put_index(0)

    plt.figure()
    data.zero_line()
    # data.min_line(top=False)

    line1 = data.etabs_demand_line('blue', top=False)

    # line2 = data.rebar_line('red', '傳統斷筋', top=False)
    line3 = data.rebar_line('green', '多點斷筋', top=False)

    plt.xlabel('Length(m)')
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line3),
        ('Demand', 'Optimization'),
        loc='upper left'
    )
    plt.title('Optimization vs Convention')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()

def f3_6and3_7and3_8():
    data = PlotDesign(
        'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/20190615 104919 Cut 2 Procedure B.xlsx')
    data.put_index(0)

    plt.figure()
    data.zero_line()
    data.min_line()

    line1 = data.etabs_demand_line('blue')
    line2 = data.rebar_number_line('red')

    plt.xlabel('Length(m)')
    plt.ylabel('As($cm^2$)')
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
    plt.ylabel('As($cm^2$)')
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
    data.min_line(10)

    line1 = data.etabs_demand_line('blue')
    # line2 = data.rebar_number_line('red')

    line2 = data.rebar_line('green', '多點斷筋')

    plt.xlabel('Length(m)')
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line2),
        ('Demand', 'Minimum reinforcement'),
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
    data.min_line(2)

    line1 = data.etabs_demand_line('blue')
    # line2 = data.rebar_number_line('red')

    line3 = data.add_ld_line('green', label='Consider $l_d$')

    plt.xlabel('Length(m)')
    plt.ylabel('As($cm^2$)')
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
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Convention', 'Optimization'),
        loc='upper left'
    )
    plt.title('Optimization vs Convention')
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
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Convention', 'Optimization'),
        loc='upper left'
    )
    plt.title('Optimization vs Convention')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def f4_6():
    data = PlotDesign(
        'D:/GitHub/thesis/Models/HighSeismic 4Floor 9M/20190614 154041 Cut 2.xlsx')
    data.put_index(28)

    plt.figure()
    data.zero_line()
    data.min_line(-23)

    line1 = data.etabs_demand_line('blue')

    line2 = data.rebar_line('red', '傳統斷筋')
    line3 = data.rebar_line('green', '多點斷筋')

    plt.xlabel('Length(m)')
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Convention', 'Optimization'),
        loc='upper left'
    )
    plt.title('Optimization vs Convention')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def f3_9():
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
    plt.ylabel('Av/s(cm)')
    plt.legend(
        (line1, line3),
        ('$V_u$', 'Optimization'),
        loc='upper left'
    )
    plt.title('Optimization Workflow')
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
    plt.ylabel('Av/s(cm)')
    plt.legend(
        (line1, line2, line3),
        ('Consider $V_c$ Demand', 'Convention', 'Optimization'),
        loc='best'
    )

    plt.title('Optimization Workflow')
    plt.grid(True, which='both', linestyle=':')


def f4_11():
    data = PlotDesign(
        'D:/GitHub/thesis/Models/MidSeismic 20Floor 9M/20190614 170819 Cut 2.xlsx')
    data.put_index(160)

    plt.figure()
    data.zero_line()
    # data.min_line()

    line1 = data.etabs_demand_line('blue')

    line2 = data.rebar_line('red', '傳統斷筋')
    line3 = data.rebar_line('green', '多點斷筋')

    plt.xlabel('Length(m)')
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line2, line3),
        ('Demand', 'Convention', 'Optimization'),
        loc='best'
    )
    plt.title('Optimization vs Convention')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def main():
    """
    test
    """
    f4_7()

    data9 = {
        1: 'D:/GitHub/thesis/Models/HighSeismic 4Floor 6M/Conservative/20190614 154022 Cut 2.xlsx',
        2: 'D:/GitHub/thesis/Models/HighSeismic 4Floor 9M/20190614 154041 Cut 2.xlsx',
        3: 'D:/GitHub/thesis/Models/HighSeismic 4Floor 12M/20190614 154055 Cut 2.xlsx',
        4: 'D:/GitHub/thesis/Models/MidSeismic 4Floor 6M/20190614 154236 Cut 2.xlsx',
        5: 'D:/GitHub/thesis/Models/MidSeismic 4Floor 9M/20190614 154307 Cut 2.xlsx',
        6: 'D:/GitHub/thesis/Models/MidSeismic 4Floor 12M/20190614 154334 Cut 2.xlsx',
        7: 'D:/GitHub/thesis/Models/LowSeismic 4Floor 6M/20190614 154117 Cut 2.xlsx',
        8: 'D:/GitHub/thesis/Models/LowSeismic 4Floor 9M/20190614 154143 Cut 2.xlsx',
        9: 'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/20190615 103351 Cut 2.xlsx'
    }

    data2 = {
        1: 'D:/GitHub/thesis/Models/MidSeismic 12Floor 9M/20190614 170742 Cut 2.xlsx',
        2: 'D:/GitHub/thesis/Models/MidSeismic 20Floor 9M/20190614 170819 Cut 2.xlsx'
    }

    # script_dir = os.path.dirname(os.path.abspath(__file__))

    data = PlotDesign(data9[9])

    # for index in range(0, data.design.get_len(), 4):
        # data.put_index(index)

    # etabs_to_addedld_sol(data)
    # tradition_flow(data)
    # multicut_flow(data)
        # multicut_compare_tradition(data)

    # v_workflow(data)
    # v_multicut_compare_tradition(data)

    data.put_index(0)

    # etabs_to_addedld_sol(data)
    # tradition_flow(data)
    # multicut_flow(data)
    # multicut_compare_tradition(data)

    # v_workflow(data)
    # v_multicut_compare_tradition(data)

    # to_excel_orderby_effect(
    #     data,
    #     'D:/GitHub/thesis/LinearCut/data/20190616 072555 Cut 2 欣詮'
    # )

    plt.show()


if __name__ == "__main__":
    main()
