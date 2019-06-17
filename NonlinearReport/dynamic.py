"""
ida data and function
"""
import os

import numpy as np
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

    def get_points(self, earthquake, kind='DBE'):
        """
        get damage and intensity by loadcase and damage_measure
        """
        df = self.story_drifts

        sa = self.earthquakes[earthquake]['sa']

        case = f'{earthquake}-{round(self.scaled_facotrs[kind] / sa, 2)}'

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

            plt.plot(damage, intensity, marker='.', *args, **kwargs)

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
        plt.plot(damage, intensity, marker='.', *args, **kwargs)

    def plot_mean(self, *args, kind='DBE', **kwargs):
        """
        plot pushover in drift and acceleration by load case
        """
        damage, intensity = self.get_mean(kind=kind)
        plt.plot(damage, intensity, marker='.', *args, **kwargs)


def _main():
    from config import data

    multi = Dynamic(
        path={
            'story_path': data['story'],
            'story_drifts_path': data['multi'],
        },
        earthquakes=data['earthquakes'],
        scaled_facotrs=data['scaled_facotrs']
    )

    tradition = Dynamic(
        path={
            'story_path': data['story'],
            'story_drifts_path': data['tradition'],
        },
        earthquakes=data['earthquakes'],
        scaled_facotrs=data['scaled_facotrs']
    )

    color = {
        'green': np.array([26, 188, 156]) / 256,
        'blue': np.array([52, 152, 219]) / 256,
        'red': np.array([233, 88, 73]) / 256,
        'orange': np.array([230, 126, 34]) / 256,
        'gray': np.array([0.5, 0.5, 0.5]),
        'background': np.array([247, 247, 247]) / 256
    }

    plt.figure(figsize=(6.4, 8.6))
    plt.subplot(2, 1, 1)
    plt.xlabel(r'Interstorey drift ratio, $\theta_{max}$')
    plt.ylabel('Height(m)')

    multi.plot_all(color=color['gray'], kind='DBE')
    multi.plot_interp(
        color=color['green'], label='Median', kind='DBE')
    multi.plot_mean(
        color=color['blue'], label='Mean', kind='DBE')

    plt.axvline(
        0.015,
        linestyle='--',
        color=color['gray']
    )
    plt.title('(a) Multi-Cut')
    plt.legend(loc='upper right')
    plt.grid(True, which='both', linestyle=':')

    plt.subplot(2, 1, 2)
    plt.xlabel(r'Interstorey drift ratio, $\theta_{max}$')
    plt.ylabel('Height(m)')

    tradition.plot_all(color=color['gray'], kind='DBE')
    tradition.plot_interp(
        color=color['green'], label='Median', kind='DBE')
    tradition.plot_mean(
        color=color['blue'], label='Mean', kind='DBE')

    plt.axvline(
        0.015,
        linestyle='--',
        color=color['gray']
    )
    plt.title('(b) Tradition')
    plt.legend(loc='upper right')
    plt.grid(True, which='both', linestyle=':')

    plt.tight_layout()

    plt.figure(figsize=(6.4, 8.6))
    plt.subplot(2, 1, 1)
    plt.xlabel(r'Interstorey drift ratio, $\theta_{max}$')
    plt.ylabel('Height(m)')

    multi.plot_all(color=color['gray'], kind='MCE')
    multi.plot_interp(
        color=color['green'], label='Median', kind='MCE')
    multi.plot_mean(
        color=color['blue'], label='Mean', kind='MCE')

    plt.axvline(
        0.02,
        linestyle='--',
        color=color['gray']
    )
    plt.title('(a) Multi-Cut')

    plt.legend(loc='upper right')
    plt.grid(True, which='both', linestyle=':')

    plt.subplot(2, 1, 2)
    plt.xlabel(r'Interstorey drift ratio, $\theta_{max}$')
    plt.ylabel('Height(m)')

    tradition.plot_all(color=color['gray'], kind='MCE')
    tradition.plot_interp(
        color=color['green'], label='Median', kind='MCE')
    tradition.plot_mean(
        color=color['blue'], label='Mean', kind='MCE')

    plt.axvline(
        0.02,
        linestyle='--',
        color=color['gray']
    )
    plt.title('(b) Tradition')
    plt.legend(loc='upper right')
    plt.grid(True, which='both', linestyle=':')
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    _main()
