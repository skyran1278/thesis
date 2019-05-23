"""
plot
"""
from itertools import repeat

import numpy as np
import matplotlib.pyplot as plt

from evaluation.design import Design, etabs_design


class PlotDesign:
    """
    plot
    """

    def __init__(self, path):
        self.c = {
            'green': np.array([26, 188, 156]) / 256,
            'blue': np.array([52, 152, 219]) / 256,
            'red': np.array([233, 88, 73]) / 256,
            'orange': np.array([230, 126, 34]) / 256,
            'gray': np.array([0.5, 0.5, 0.5]),
            'background': np.array([247, 247, 247]) / 256
        }

        self.linewidth = 2.0

        print('Load Data...')

        self.design = Design(path, '多點斷筋')
        self.tradition = Design(path, '傳統斷筋')
        self.etabs_design, self.etabs_design_tradition = etabs_design(path)

        print('Load Data Done!')

        self.index = None

    def demand_line(self, color):
        """
        Real Solution
        """
        index = self.index

        index = index // 4 * 4
        df = self.etabs_design_on_index()

        top_size_area = self.design.get_area(index, ('主筋', '左1'))
        bot_size_area = self.design.get_area(index + 3, ('主筋', '左1'))

        plt.plot(
            df['StnLoc'],
            df['BarTopNumLd'] * top_size_area,
            color=self.c[color], linewidth=self.linewidth
        )
        plt.plot(
            df['StnLoc'],
            - df['BarBotNumLd'] * bot_size_area,
            color=self.c[color], linewidth=self.linewidth
        )

    def v_rabar_line(self, color, df='多點斷筋'):
        """
        v rebar line
        """
        index = self.index

        if df == '多點斷筋':
            df = self.design
        elif df == '傳統斷筋':
            df = self.tradition

        group_num = df.group_num

        index = index // 4 * 4

        area = []
        for col in ['左', '中', '右']:
            area.append(df.get_shear(index, ('箍筋', col)))
        area = np.repeat(area, 2)

        length = []
        for col in range(group_num * 2 + 9, group_num * 2 + 12):
            length.extend(df.get_abs_length(index, col, stirrup=True))

        plt.plot(length, area, color=self.c[color], linewidth=self.linewidth)

    def rebar_line(self, color, df='多點斷筋'):
        """
        plot top and bot line
        """
        index = self.index

        if df == '多點斷筋':
            df = self.design
        elif df == '傳統斷筋':
            df = self.tradition

        group_num = df.group_num

        index = index // 4 * 4

        area = []
        for col in range(5, group_num + 5):
            area.append(df.get_total_area(index, col))
        area = np.repeat(area, 2)

        length = []
        for col in range(5 + group_num, 2 * group_num + 5):
            length.extend(df.get_abs_length(index, col))

        plt.plot(length, area, color=self.c[color], linewidth=self.linewidth)

        index += 2

        area = []
        for col in range(5, group_num + 5):
            area.append(df.get_total_area(index, col))
        area = np.repeat(area, 2)

        length = []
        for col in range(5 + group_num, 2 * group_num + 5):
            length.extend(df.get_abs_length(index, col))

        plt.plot(length, -area, color=self.c[color], linewidth=self.linewidth)

    def tradition_boundary_line(self):
        """
        1/3 1/4 1/5
        """
        index = self.index

        start = self.design.get(index, ('支承寬', '左'))
        end = (
            self.design.get(index, ('梁長', '')) -
            self.design.get(index, ('支承寬', '右'))
        )

        plt.axvline(
            (end - start) / 4 + start, linestyle='--', color=self.c['gray'])
        plt.axvline(
            (end - start) / 3 + start, linestyle='--', color=self.c['gray'])
        plt.axvline(
            (end - start) / 3 * 2 + start, linestyle='--', color=self.c['gray'])
        plt.axvline(
            (end - start) / 4 * 3 + start, linestyle='--', color=self.c['gray'])
        plt.axvline(
            (end - start) / 5 + start, linestyle='--', color=self.c['gray'])
        plt.axvline(
            (end - start) / 5*4 + start, linestyle='--', color=self.c['gray'])

    def put_index(self, index):
        """
        change index
        """
        index = index // 4 * 4

        self.index = index

    def etabs_v_demand_line(self, color):
        """
        etabs v demand
        """

        # ETABS Demand
        df = self.etabs_design_on_index()

        plt.plot(
            df['StnLoc'], df['VRebar'], color=self.c[color], linewidth=self.linewidth)

    def v_consider_vc_demand_line(self, color):
        """
        etabs v demand
        """

        # ETABS Demand
        df = self.etabs_design_on_index()

        plt.plot(
            df['StnLoc'], df['VRebarConsiderVc'], color=self.c[color], linewidth=self.linewidth)

    def etabs_design_on_index(self, df='多點斷筋'):
        """
        on index
        """
        index = self.index

        if df == '多點斷筋':
            df = self.etabs_design
        elif df == '傳統斷筋':
            df = self.etabs_design_tradition

        index = index // 4 * 4

        df = df.loc[
            (df['Story'] == self.design.get(index, ('樓層', ''))) &
            (df['BayID'] == self.design.get(index, ('編號', '')))
        ].copy()

        return df

    def etabs_demand_line(self, color, *args, **kwargs):
        """
        ETABS Demand
        """
        df = self.etabs_design_on_index()

        plt.plot(
            df['StnLoc'], df['AsTop'], color=self.c['green'], linewidth=self.linewidth)
        plt.plot(
            df['StnLoc'], -df['AsBot'], color=self.c['blue'], linewidth=self.linewidth)

    def seismic_line(self):
        """
        圍束區
        """
        index = self.index

        start = self.design.get(index, ('支承寬', '左'))
        end = (
            self.design.get(index, ('梁長', '')) -
            self.design.get(index, ('支承寬', '右'))
        )

        H = self.design.get(index, ('RC 梁深', ''))

        plt.axvline(
            start + 2 * H,
            linestyle='--',
            color=self.c['gray']
        )

        plt.axvline(
            end - 2 * H,
            linestyle='--',
            color=self.c['gray']
        )

    def zero_line(self):
        """
        zero
        """
        index = self.index

        start = self.design.get(index, ('支承寬', '左'))
        end = (
            self.design.get(index, ('梁長', '')) -
            self.design.get(index, ('支承寬', '右'))
        )

        # 基準線
        plt.plot(
            [start, end],
            [0, 0],
            color=self.c['gray'],
            linewidth=self.linewidth
        )

    def min_line(self):
        """
        min area
        """
        index = self.index

        top_size_area = self.design.get_area(index, ('主筋', '左1'))
        bot_size_area = self.design.get_area(index + 3, ('主筋', '左1'))

        plt.axhline(2 * top_size_area, linestyle='--', color=self.c['gray'])
        plt.axhline(-2 * bot_size_area, linestyle='--', color=self.c['gray'])

    def boundary_line(self, boundary=0.1):
        """
        boundary
        """
        index = self.index

        start = self.design.get(index, ('支承寬', '左'))
        end = (
            self.design.get(index, ('梁長', '')) -
            self.design.get(index, ('支承寬', '右'))
        )

        plt.axvline(
            (end - start) * boundary + start,
            linestyle='--',
            color=self.c['gray']
        )
        plt.axvline(
            end - (end - start) * boundary,
            linestyle='--',
            color=self.c['gray']
        )

    def v_min_line(self):
        """
        v min
        """
        df = self.etabs_design_on_index()

        B = df['B'].iloc[0] * 100
        fc = df['Fc'].iloc[0] / 10
        fyt = df['Fy'].iloc[0] / 10

        Asmin = max(0.2 * np.sqrt(fc) * B / fyt, 3.5 * B / fyt) * 0.01

        Asmax = 4 * 0.53 * np.sqrt(fc) * B / fyt * 0.01

        plt.axhline(Asmin, linestyle='--', color=self.c['gray'])
        plt.axhline(Asmax, linestyle='--', color=self.c['gray'])
