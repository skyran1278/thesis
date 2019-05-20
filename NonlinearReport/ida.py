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
        read_file = self.story_path
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

        read_file = self.story_drifts_path
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

            plt.plot(damage, intensity, marker='.', *args, **kwargs)

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
    from config import midseismic_4floor_12m as data

    multi = IDA(
        path={
            'story_path': data['story'],
            'story_drifts_path': data['multi'],
        },
        earthquakes=data['earthquakes'],
    )

    tradition = IDA(
        path={
            'story_path': data['story'],
            'story_drifts_path': data['tradition'],
        },
        earthquakes=data['earthquakes'],
    )

    tradition_end = IDA(
        path={
            'story_path': data['story'],
            'story_drifts_path': data['tradition_end'],
        },
        earthquakes=data['earthquakes'],
    )

    color = {
        'green': np.array([26, 188, 156]) / 256,
        'blue': np.array([52, 152, 219]) / 256,
        'red': np.array([233, 88, 73]) / 256,
        'orange': np.array([230, 126, 34]) / 256,
        'gray': np.array([0.5, 0.5, 0.5]),
        'background': np.array([247, 247, 247]) / 256
    }

    # plt.figure()
    # plt.xlabel(r'Maximum interstorey drift ratio, $\theta_{max}$')
    # plt.ylabel(r'"first-mode"spectral acceleration $S_a(T_1$, 5%)(g)')

    # multi.plot_all(color=color['gray'])
    # multi.plot_interp(label='Multi-Cut', linewidth=3.0)
    # tradition.plot_interp(label='Tradition', linewidth=3.0)
    # tradition_end.plot_interp(label='Tradition_end', linewidth=3.0)

    # plt.axvline(
    #     0.025,
    #     linestyle='--',
    #     color=color['gray']
    # )
    # plt.axvline(
    #     0.04,
    #     linestyle='--',
    #     color=color['gray']
    # )

    # plt.xlim(0, 0.05)
    # plt.ylim(0, 5)
    # plt.legend(loc='upper left')

    plt.figure()
    plt.xlabel(r'Maximum interstorey drift ratio, $\theta_{max}$')
    plt.ylabel(r'"first-mode"spectral acceleration $S_a(T_1$, 5%)(g)')

    tradition_end.plot_all(color=color['gray'])
    tradition_end.plot_interp(
        label='Median Capacity',
        linewidth=3.0, color=color['blue']
    )

    plt.axvline(
        0.025,
        linestyle='--',
        color=color['gray']
    )
    plt.axvline(
        0.04,
        linestyle='--',
        color=color['gray']
    )

    plt.xlim(0, 0.05)
    plt.ylim(0, 5)
    plt.legend(loc='upper left')

    plt.figure()
    plt.xlabel(r'Maximum interstorey drift ratio, $\theta_{max}$')
    plt.ylabel(r'"first-mode"spectral acceleration $S_a(T_1$, 5%)(g)')

    tradition.plot_all(color=color['gray'])
    tradition.plot_interp(
        label='Median Capacity',
        linewidth=3.0, color=color['green']
    )

    plt.axvline(
        0.025,
        linestyle='--',
        color=color['gray']
    )
    plt.axvline(
        0.04,
        linestyle='--',
        color=color['gray']
    )

    plt.xlim(0, 0.05)
    plt.ylim(0, 5)
    plt.legend(loc='upper left')

    plt.show()


if __name__ == "__main__":
    _main()
