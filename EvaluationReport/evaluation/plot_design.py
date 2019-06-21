"""
plot
"""
import math
from itertools import repeat


import numpy as np
import pandas as pd
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

    def add_ld_line(self, color, *args, top=True, bot=True, **kwargs):
        """
        Real Solution
        """
        index = self.index

        index = index // 4 * 4
        df = self.etabs_design_on_index()

        top_size_area = self.design.get_area(index, ('主筋', '左1'))
        bot_size_area = self.design.get_area(index + 3, ('主筋', '左1'))

        if top:
            line, = plt.plot(
                df['StnLoc'],
                df['BarTopNumLd'] * top_size_area * 10000,
                color=self.c[color], linewidth=self.linewidth,
                *args, **kwargs
            )

        if bot:
            line, = plt.plot(
                df['StnLoc'],
                - df['BarBotNumLd'] * bot_size_area * 10000,
                color=self.c[color], linewidth=self.linewidth,
                *args, **kwargs
            )

        return line

    def rebar_number_line(self, color, *args, top=True, bot=True, **kwargs):
        """
        Real Solution
        """
        index = self.index

        index = index // 4 * 4
        df = self.etabs_design_on_index()

        top_size_area = self.design.get_area(index, ('主筋', '左1'))
        bot_size_area = self.design.get_area(index + 3, ('主筋', '左1'))
        if top:
            line, = plt.plot(
                df['StnLoc'],
                df['BarTopNum'] * top_size_area * 10000,
                color=self.c[color], linewidth=self.linewidth,
                *args, **kwargs
            )
        if bot:
            line, = plt.plot(
                df['StnLoc'],
                - df['BarBotNum'] * bot_size_area * 10000,
                color=self.c[color], linewidth=self.linewidth,
                *args, **kwargs
            )

        return line

    def v_rabar_line(self, color, df='多點斷筋'):
        """
        v rebar line
        return line
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

        line, = plt.plot(
            length, area * 100, color=self.c[color], linewidth=self.linewidth)

        return line

    def rebar_line(self, color, df='多點斷筋', top=True, bot=True):
        """
        plot top and bot line
        reutnr line
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
            col_area = df.get_total_area(index, col)
            if col_area is not None:
                area.append(col_area)
        area = np.repeat(area, 2)

        length = []
        for col in range(5 + group_num, 2 * group_num + 5):
            col_length = df.get_abs_length(index, col)
            if col_length is not None:
                length.extend(col_length)
        if top:
            line, = plt.plot(
                length, area * 10000, color=self.c[color], linewidth=self.linewidth)

        # 下層筋，取負號
        index += 2

        area = []
        for col in range(5, group_num + 5):
            col_area = df.get_total_area(index, col)
            if col_area is not None:
                area.append(col_area)
        area = np.repeat(area, 2)

        length = []
        for col in range(5 + group_num, 2 * group_num + 5):
            col_length = df.get_abs_length(index, col)
            if col_length is not None:
                length.extend(col_length)

        if bot:
            line, = plt.plot(
                length, -area * 10000, color=self.c[color], linewidth=self.linewidth
            )

        return line

    def tradition_boundary_line(self):
        """
        1/3 1/4 1/5
        """
        self.boundary_line(1/5)
        self.boundary_line(1/4)
        self.boundary_line(1/3)

    def put_index(self, index):
        """
        change index
        """
        index = index // 4 * 4

        self.index = index

    def etabs_v_demand_line(self, color):
        """
        etabs v demand
        return line
        """

        # ETABS Demand
        df = self.etabs_design_on_index()

        line, = plt.plot(
            df['StnLoc'], df['VRebar'] * 100,
            color=self.c[color], linewidth=self.linewidth
        )

        return line

    def v_consider_vc_demand_line(self, color):
        """
        etabs v demand
        return line
        """

        # ETABS Demand
        df = self.etabs_design_on_index()

        line, = plt.plot(
            df['StnLoc'], df['VRebarConsiderVc'] * 100,
            color=self.c[color], linewidth=self.linewidth
        )

        return line

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

    def etabs_demand_line(self, color, *args, top=True, bot=True, **kwargs):
        """
        ETABS Demand
        reuturn line
        """
        df = self.etabs_design_on_index()

        if top:
            line, = plt.plot(
                df['StnLoc'], df['AsTop'] * 10000,
                color=self.c[color], linewidth=self.linewidth,
                *args, **kwargs
            )
        if bot:
            line, = plt.plot(
                df['StnLoc'], -df['AsBot'] * 10000,
                color=self.c[color], linewidth=self.linewidth,
                *args, **kwargs
            )

        return line

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

    def zero_line(self, *args, **kwargs):
        """
        zero
        """
        # 基準線
        plt.axhline(
            0,
            color=self.c['gray'],
            linewidth=self.linewidth,
            *args, **kwargs
        )

    def min_line(self, cover=6.5, top=True, bot=True):
        """
        min area
        """
        df = self.etabs_design_on_index()

        top_size_area = self.design.get_area(self.index, ('主筋', '左1'))
        bot_size_area = self.design.get_area(self.index + 3, ('主筋', '左1'))

        b = df['B'].iloc[0] * 100
        d = df['H'].iloc[0] * 100 - cover  # 假設保護層 10cm
        fc = df['Fc'].iloc[0] / 10
        fy = df['Fy'].iloc[0] / 10

        asmin = max(0.8 * math.sqrt(fc) / fy * b * d, 14 / fy * b * d)

        if top:
            plt.axhline(
                max(asmin, 2 * top_size_area * 10000), linestyle='--', color=self.c['gray'])

        if bot:
            plt.axhline(
                min(-asmin, -2 * bot_size_area * 10000), linestyle='--', color=self.c['gray'])

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

        asmin = max(0.2 * np.sqrt(fc) * B / fyt, 3.5 * B / fyt)

        asmax = 4 * 0.53 * np.sqrt(fc) * B / fyt

        plt.axhline(asmin, linestyle='--', color=self.c['gray'])
        plt.axhline(asmax, linestyle='--', color=self.c['gray'])
