"""
ida data and function
"""
import os

import pandas as pd
import matplotlib.pyplot as plt


class Dynamic():
    """
    IDA data and function
    """

    def __init__(self, path, earthquakes, scaled_facotrs):
        self.story_path = path['story_path']
        self.story_drifts_path = path['story_drifts_path']

        self.earthquakes = earthquakes
        self.scaled_facotrs = scaled_facotrs

        self.story_drifts = self._init_story_damage()
        self.max_drifts = self._init_max_damage()

    def _init_story(self):
        read_file = f'{self.story_path}.xlsx'
        sheet_name = 'Story Data'

        df = pd.read_excel(
            read_file, sheet_name=sheet_name, header=1, usecols=[0, 2], skiprows=[2])

        # mm => m
        df.loc[:, 'Elevation'] = df.loc[:, 'Elevation'] / 1000

        return df

    def _init_story_damage(self):
        """
        init time history story drifts
        damage_measure='story_drifts'
        """
        story = self._init_story()

        read_file = f'{self.story_drifts_path}.xlsx'
        sheet_name = 'Story Drifts'

        df = pd.read_excel(
            read_file, sheet_name=sheet_name, header=1, usecols=[0, 1, 3], skiprows=[2])

        # convert story label to story height
        df = df.merge(story, how='outer', left_on='Story', right_on='Name')
        df = df.drop(columns='Name')

        # delete max and min string
        df.loc[:, 'Load Case/Combo'] = df['Load Case/Combo'].str[:-4]

        # combine two columns
        df = df.assign(
            StoryAndCase=lambda x: x['Story'] + ' ' + x['Load Case/Combo'])

        # combine max min
        df = df.groupby('StoryAndCase', sort=False).agg('max')

        # split case and factors
        df['Case'], df['Scaled Factors'] = (
            df['Load Case/Combo'].str.rsplit('-', 1).str)

        # delete na
        df = df.dropna()

        return df

    def _init_max_damage(self):
        """
        condense story drift to max drift
        """
        df = self.story_drifts.groupby(
            'Load Case/Combo', sort=False).agg('max')

        # drop columns
        df = df.drop(columns=['Story', 'Elevation'])

        return df

    def get_points(self, earthquake, kind='DBE'):
        """
        get damage and intensity by loadcase and damage_measure
        """
        df = self.story_drifts

        case = f'{earthquake}-{self.scaled_facotrs[kind]}'

        # select earthquake
        df = df.loc[df['Load Case/Combo'] == case, :].copy()

        # sort
        df = df.sort_values(by=['Elevation'], ascending=False)

        # return pure numpy, convenience to plot figure
        return (
            df['Drift'].values,
            df['Elevation'].values
        )

    def get_interp(self, percentage=0.5, kind='DBE'):
        """
        use to get median
        """
        damages = pd.DataFrame()

        for eq in self.earthquakes:
            damage, intensity = self.get_points(eq, kind=kind)

            # concat all drift
            damages = pd.concat([damages, pd.DataFrame({eq: damage})], axis=1)

        damage = damages.quantile(q=percentage, axis=1).values

        return damage, intensity

    def get_mean(self, kind='DBE'):
        """
        use to get mean
        """
        damages = pd.DataFrame()

        for eq in self.earthquakes:
            damage, intensity = self.get_points(eq, kind=kind)

            # concat all drift
            damages = pd.concat([damages, pd.DataFrame({eq: damage})], axis=1)

        damage = damages.mean(axis=1).values

        return damage, intensity

    def plot_all(self, *args, kind='DBE', **kwargs):
        """
        plot ida in drift and acceleration by load case
        """
        for eq in self.earthquakes:
            damage, intensity = self.get_points(eq, kind=kind)

            plt.plot(damage, intensity, label=eq, marker='.', *args, **kwargs)

    def plot(self, earthquake, *args, kind='DBE', **kwargs):
        """
        plot pushover in drift and acceleration by load case
        """
        damage, intensity = self.get_points(earthquake, kind=kind)
        plt.plot(damage, intensity, *args, **kwargs)

    def plot_interp(self, *args, percentage=0.5, kind='DBE', **kwargs):
        """
        plot pushover in drift and acceleration by load case
        """
        damage, intensity = self.get_interp(percentage, kind=kind)
        plt.plot(damage, intensity, *args, **kwargs)

    def plot_mean(self, *args, kind='DBE', **kwargs):
        """
        plot pushover in drift and acceleration by load case
        """
        damage, intensity = self.get_mean(kind=kind)
        plt.plot(damage, intensity, *args, **kwargs)


def _main():
    scaled_facotrs = {
        'DBE': 0.772,
        'MCE': 1.029,
    }
    earthquakes = {
        'RSN68_SFERN_PEL090': {'sa': 0.510},
        'RSN125_FRIULI.A_A-TMZ270': {'sa': 0.440},
        'RSN169_IMPVALL.H_H-DLT262': {'sa': 0.392},
        'RSN174_IMPVALL.H_H-E11230': {'sa': 0.238},
        'RSN721_SUPER.B_B-ICC090': {'sa': 0.269},
        'RSN725_SUPER.B_B-POE360': {'sa': 0.520},
        'RSN752_LOMAP_CAP000': {'sa': 0.585},
        'RSN767_LOMAP_G03090': {'sa': 0.375},
        'RSN848_LANDERS_CLW-TR': {'sa': 0.370},
        'RSN900_LANDERS_YER270': {'sa': 0.426},
        'RSN953_NORTHR_MUL279': {'sa': 0.617},
        'RSN960_NORTHR_LOS000': {'sa': 0.368},
        'RSN1111_KOBE_NIS000': {'sa': 0.281},
        'RSN1116_KOBE_SHI000': {'sa': 0.462},
        'RSN1148_KOCAELI_ARE090': {'sa': 0.133},
        'RSN1158_KOCAELI_DZC180': {'sa': 0.327},
        'RSN1244_CHICHI_CHY101-N': {'sa': 0.383},
        'RSN1485_CHICHI_TCU045-E': {'sa': 0.256},
        'RSN1602_DUZCE_BOL090': {'sa': 0.751},
        'RSN1633_MANJIL_ABBAR--T': {'sa': 0.477},
        'RSN1787_HECTOR_HEC090': {'sa': 0.384},
    }

    file_dir = os.path.dirname(os.path.abspath(__file__))

    path = {
        'story_path': file_dir + '/活頁簿3',
        'story_drifts_path': file_dir + '/Normal 1',
    }

    ida = Dynamic(path, earthquakes, scaled_facotrs)

    plt.figure()
    plt.xlabel(r'Maximum interstorey drift ratio, $\theta_{max}$')
    plt.ylabel(r'"first-mode"spectral acceleration $S_a(T_1$, 5%)(g)')

    # ida.plot('RSN68_SFERN_PEL090')
    ida.plot_all(color='k', kind='MCE')
    ida.plot_interp(label='median', kind='MCE')
    ida.plot_mean(label='mean', kind='MCE')

    plt.legend(loc='upper right')
    plt.show()


if __name__ == "__main__":
    _main()
