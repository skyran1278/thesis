"""
ida data and function
"""
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# from plotlib import EnhancePlotlib


class IDA():
    """
    IDA data and function
    """

    def __init__(self, path, earthquakes):
        self.story_path = path['story_path']
        self.story_drifts_path = path['story_drifts_path']

        self.earthquakes = earthquakes

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

    def get_points(self, earthquake):
        """
        get damage and intensity by loadcase and damage_measure
        """
        intensity_measure = 'sa'

        damage = self.max_drifts
        intensity = self.earthquakes[earthquake][intensity_measure]

        # select earthquake
        df = damage.loc[damage['Case'] == earthquake, :].copy()

        # scaled to sa
        df.loc[:, 'Scaled Factors'] = (
            df.loc[:, 'Scaled Factors'].astype('float64') * intensity)

        # sort
        df = df.sort_values(by=['Scaled Factors'])

        # return pure numpy, convenience to plot figure
        return (
            df['Drift'].values,
            df['Scaled Factors'].values
        )

    def get_interp(self, percentage=0.5, num=1000):
        """
        use to interp intensity
        """
        damages = pd.DataFrame()
        intensities = pd.DataFrame()
        interp_dm = pd.DataFrame()

        for eq in self.earthquakes:
            damage, intensity = self.get_points(eq)

            # concat all drift and accel
            damages = pd.concat([damages, pd.DataFrame({eq: damage})], axis=1)
            intensities = pd.concat(
                [intensities, pd.DataFrame({eq: intensity})], axis=1)

        # scaled to same intensities
        interp_im = np.linspace(
            intensities.min().max(), intensities.max().min(), num=num)

        # interpolate to same intensities to damages
        for col in damages:
            interp_dm.loc[:, col] = (
                np.interp(interp_im, intensities[col], damages[col]))

        interp_dm = interp_dm.quantile(q=percentage, axis=1).values

        return interp_dm, interp_im

    def plot_all(self, *args, **kwargs):
        """
        plot ida in drift and acceleration by load case
        """
        for eq in self.earthquakes:
            damage, intensity = self.get_points(eq)

            plt.plot(damage, intensity, label=eq, marker='.', *args, **kwargs)

    def plot(self, earthquake, *args, **kwargs):
        """
        plot pushover in drift and acceleration by load case
        """
        damage, intensity = self.get_points(earthquake)
        plt.plot(damage, intensity, *args, **kwargs)

    def plot_interp(self, *args, percentage=0.5, **kwargs):
        """
        plot pushover in drift and acceleration by load case
        """
        damage, intensity = self.get_interp(percentage)
        plt.plot(damage, intensity, *args, **kwargs)


def _main():
    earthquakes = {
        'RSN725_SUPER.B_B-POE360': {'sa': 0.576},
        'RSN900_LANDERS_YER270': {'sa': 0.474},
        'RSN953_NORTHR_MUL279': {'sa': 0.697},
        'RSN960_NORTHR_LOS000': {'sa': 0.444},
        'RSN1111_KOBE_NIS000': {'sa': 0.358},
        'RSN1116_KOBE_SHI000': {'sa': 0.567},
        'RSN1148_KOCAELI_ARE090': {'sa': 0.166},
        'RSN1158_KOCAELI_DZC180': {'sa': 0.359},
        'RSN1602_DUZCE_BOL090': {'sa': 0.867},
        'RSN1633_MANJIL_ABBAR--T': {'sa': 0.495},
        'RSN1787_HECTOR_HEC090': {'sa': 0.375},
    }

    file_dir = os.path.dirname(os.path.abspath(__file__))

    path = {
        'story_path': file_dir + '/story',
        'story_drifts_path': file_dir + '/story_drifts',
    }

    ida = IDA(
        path=path,
        earthquakes=earthquakes,
    )

    plt.figure()
    plt.xlabel(r'Maximum interstorey drift ratio, $\theta_{max}$')
    plt.ylabel(r'"first-mode"spectral acceleration $S_a(T_1$, 5%)(g)')

    ida.plot_all(color=(0.5, 0.5, 0.5))
    ida.plot_interp(label='median', marker='.')

    plt.xlim(0, 0.05)
    plt.ylim(0, 5)
    plt.legend(loc='upper left')

    plt.show()


if __name__ == "__main__":
    _main()
