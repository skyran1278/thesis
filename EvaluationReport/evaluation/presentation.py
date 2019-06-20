# pylint: disable=missing-docstring

import numpy as np
import matplotlib.pyplot as plt

from evaluation.plot_design import PlotDesign

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
    plt.ylabel('A_v/s(cm)')
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
    plt.ylabel('A_v/s(cm)')
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
    plt.ylabel('As($cm^2$)')
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
    plt.ylabel('As($cm^2$)')
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
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line4, line2, line3),
        ('Demand', 'Consider Ld', 'Tradition', 'Multi-Cut'),
        loc='best'
    )
    plt.title('Multi-Cut vs Tradition')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def p03():
    data = PlotDesign(data9[9])
    data.put_index(0)

    plt.figure()
    data.zero_line()
    # data.boundary_line(1/5)
    # data.boundary_line(1/3)

    line1 = data.rebar_line('red', '傳統斷筋')
    line2 = data.rebar_line('green', '多點斷筋')

    plt.xlabel('Length(m)')
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line2),
        ('Tradition', 'Optimization'),
        loc='upper center'
    )
    plt.title('Optimization vs Tradition')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def p04():
    data = PlotDesign(data9[9])
    data.put_index(0)

    plt.figure()
    data.zero_line()
    # data.min_line()
    data.boundary_line(1/3)
    data.boundary_line(1/5)

    line1 = data.etabs_demand_line('blue')

    line2 = data.rebar_line('green', '傳統斷筋')

    plt.xlabel('Length(m)')
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line2),
        ('Demand', 'Design'),
        loc='upper center'
    )
    plt.title('Tradition Workflow')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def p05():
    data = PlotDesign(
        'D:/GitHub/thesis/LinearCut/data/20190616 072555 Cut 2 欣詮.xlsx')
    data.put_index(1140)

    plt.figure()
    data.zero_line()
    data.boundary_line(1/3)

    line1 = data.etabs_demand_line('blue')

    line2 = data.rebar_line('green', '傳統斷筋')

    plt.xlabel('Length(m)')
    plt.ylabel('As($cm^2$)')
    plt.legend(
        (line1, line2),
        ('Demand', 'Design'),
        loc='upper left'
    )
    plt.title('Tradition Workflow')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def p08():
    data = PlotDesign(data9[9])
    data.put_index(0)

    plt.figure(figsize=(6.4, 2.4))
    data.zero_line()
    data.min_line(2, bot=False)

    data.etabs_demand_line('blue', bot=False)

    plt.xlabel('Length(m)')
    plt.ylabel('As($cm^2$)')
    plt.title('Demand')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()


def main():
    """
    test
    """
    p08()

    # data = PlotDesign(data9[9])

    # for index in range(0, data.design.get_len(), 4):
    # data.put_index(index)

    # etabs_to_addedld_sol(data)
    # tradition_flow(data)
    # multicut_flow(data)
    # multicut_compare_tradition(data)

    # v_workflow(data)
    # v_multicut_compare_tradition(data)

    # data.put_index(0)

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
