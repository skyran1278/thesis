"""
read multiple rebar
"""
import os
import pickle

import pandas as pd

from evaluation.rebar import get_diameter, get_area


def etabs_design(path):
    """
    load etabs design
    """
    if not os.path.exists(f'{path} etabs design.pkl'):
        df = pd.read_excel(path, sheet_name='etabs_design')
        tradition = pd.read_excel(
            path, sheet_name='etabs_design_trational')
        with open(f'{path} etabs design.pkl', 'wb') as f:
            pickle.dump((df, tradition), f, True)

    with open(f'{path} etabs design.pkl', 'rb') as f:
        df, tradition = pickle.load(f)

    return df, tradition


class Design:
    """
    excel beam design
    """

    def __init__(self, path, sheet_name):
        if not os.path.exists(f'{path} {sheet_name}.pkl'):
            df = pd.read_excel(path, sheet_name=sheet_name, header=[0, 1])
            df = df.rename(
                columns=lambda x: x if 'Unnamed' not in str(x) else '')

            with open(f'{path} {sheet_name}.pkl', 'wb') as f:
                pickle.dump(df, f, True)

        with open(f'{path} {sheet_name}.pkl', 'rb') as f:
            self.df = pickle.load(f)

        self.group_num = self.get_group_num()

    def get_group_num(self):
        """
        get group num
        """
        index = 1
        while ('主筋', f'左{index}') in self.df.columns:
            index += 1

        index -= 1

        index *= 2

        if ('主筋', '中') in self.df.columns:
            index += 1

        return index

    def get_abs_length(self, index, col, stirrup=False):
        """
        get absolute length
        return start length and end length
        """
        group_num = self.group_num

        length = self.get(index, ('支承寬', '左'))

        if not isinstance(col, int):
            raise Exception('col is not int')

        if stirrup:
            for iter_col in range(9 + 2 * group_num, col):
                length = length + self.get(index, iter_col)

            end_length = length + self.get(index, col)

            return length, end_length

        if pd.isnull(self.get(index, col)):
            return None

        for iter_col in range(5 + group_num, col):
            if not pd.isnull(self.get(index, iter_col)):
                length = length + self.get(index, iter_col)

        end_length = length + self.get(index, col)

        return length, end_length

    def get_len(self):
        """
        get index length
        """
        return len(self.df.index)

    def get(self, index, col):
        """
        get by index or col
        """
        if isinstance(col, int):
            col = self.df.columns[col]

        # for 主筋 to get its row
        if '主筋' in col:
            return self.df.loc[index, col]

        # for 主筋長度 to get first and last row
        if '主筋長度' in col:
            if index % 4 == 1:
                index -= 1
            elif index % 4 == 2:
                index += 1
            return self.df.loc[index, col] / 100

        # for others to normalize to first row
        index = index // 4 * 4

        if col[0] in ['RC 梁寬', 'RC 梁深', '箍筋長度', '梁長', '支承寬']:
            return self.df.loc[index, col] / 100

        return self.df.loc[index, col]

    def get_total_area(self, index, col):
        """
        get total rebar area
        """
        if index % 4 <= 1:
            index = index // 4 * 4
        else:
            index = index // 4 * 4 + 2

        if pd.isnull(self.get_num(index, col)):
            return None

        row1 = self.get_num(index, col) * self.get_area(index, col)
        row2 = self.get_num(index + 1, col) * self.get_area(index + 1, col)

        return round(row1 + row2, 8)

    def get_num(self, index, col):
        """
        get '主筋' num
        """
        num_and_size = self.get(index, col)

        if pd.isnull(num_and_size):
            return None

        if num_and_size == 0:
            return 0

        return int(num_and_size.split('-')[0])

    def get_diameter(self, index, col):
        """
        get diameter
        """
        size = self.get(index, col)

        if pd.isnull(size):
            return None

        if size == 0:
            return 0

        # 主筋
        if '-' in size:
            size = size.split('-')[1]

        # 箍筋
        elif '@' in size:
            size = size.split('@')[0]

        return get_diameter(size)

    def get_area(self, index, col):
        """
        get area
        """
        size = self.get(index, col)

        if pd.isnull(size):
            return None

        if size == 0:
            return 0

        # 主筋
        if '-' in size:
            size = size.split('-')[1]

        # 箍筋
        elif '@' in size:
            size = size.split('@')[0]

        return get_area(size)

    def get_spacing(self, index, col):
        """
        get spacing
        """
        stirrup = self.get(index, col)

        if '@' not in stirrup:
            raise Exception("Invalid index!", (index, col))

        return float(stirrup.split('@')[1]) / 100

    def get_shear(self, index, col):
        """
        get shear design
        """
        area = self.get_area(index, col) * 2
        spacing = self.get_spacing(index, col)
        return area / spacing


def main():
    """
    test
    """
    path = 'D:/GitHub/thesis/EvaluationReport/data/LowSeismic 4Floor 12M 三點.xlsx'

    design = Design(path, '多點斷筋')

    print(design.get_len())
    print(design.get(1, ('主筋', '中')))
    # print(design.get(3, ('主筋', '左')))
    # print(design.get(2, ('主筋長度', '左')))
    # print(design.get_total_area(11, ('主筋', '左')))
    # print(design.get_length_area(11, 0.24))
    # print(design.get_num(6, ('主筋', '右')))
    # print(design.get_diameter(6, ('箍筋', '右')))
    # print(design.get_diameter(6, ('主筋', '右')))
    # print(design.get_area(6, ('主筋', '右')))
    # print(design.get_area(6, ('箍筋', '右')))
    # print(design.get_spacing(10, ('箍筋', '右')))
    # print(design.get_shear(10, ('箍筋', '右')))
    # print(design.get_shear(10, ('箍筋', '中')))


if __name__ == "__main__":
    main()
