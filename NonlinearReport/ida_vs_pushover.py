"""
ida data and function
"""
import os
import pickle

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from plotlib import EnhancePlotlib


class IDA():
    """
    IDA data and function
    """

    def __init__(self, path, earthquakes, stories):
        self.base_shear_path = path['base_shear_path']
        self.story_drifts_path = path['story_drifts_path']
        self.story_displacements_path = path['story_displacements_path']
        self.earthquakes = earthquakes
        self.stories = stories

        self.base_shear = None
        self.story_drifts = None
        self.story_displacements = None

        self.plotlib = EnhancePlotlib()

    def __getattr__(self, attr):
        return getattr(self.plotlib, attr)

    def _story2level(self, df):
        for story in self.stories:
            df.loc[df['Story'] == story, 'StoryLevel'] = self.stories[story]

        return df

    def _init_damage(self):
        """
        init time history story drifts or story displacements
        damage_measure='story_drifts' or story_displacements
        """
        if self.plotlib.damage_measure == 'story_drifts':
            filepath = self.story_drifts_path
            sheet_name = 'Story Drifts'
        elif self.plotlib.damage_measure == 'story_displacements':
            filepath = self.story_displacements_path
            sheet_name = 'Story Max Avg Displacements'

        pkl_file = f'{filepath} for ida.pkl'

        if not os.path.exists(pkl_file):
            print("Reading excel...")

            read_file = f'{filepath}.xlsx'

            df = pd.read_excel(
                read_file, sheet_name=sheet_name, header=1, usecols=3, skiprows=[2])

            # convert story label to number
            df = self._story2level(df)

            # delete max and min string
            df.loc[:, 'Load Case/Combo'] = df['Load Case/Combo'].str[:-4]

            df = df.assign(
                StoryAndCase=lambda x: x['Story'] + ' ' + x['Load Case/Combo'])

            # combine max min
            df = df.groupby('StoryAndCase', as_index=False,
                            sort=False).agg('max')

            df['Load Case'], df['Scaled Factors'] = df['Load Case/Combo'].str.rsplit(
                '-', 1).str

            print("Creating pickle file ...")
            with open(pkl_file, 'wb') as f:
                pickle.dump(df, f, True)
            print("Done!")

        with open(pkl_file, 'rb') as f:
            df = pickle.load(f)

        if self.plotlib.damage_measure == 'story_drifts':
            self.story_drifts = df
        elif self.plotlib.damage_measure == 'story_displacements':
            self.story_displacements = df

    def _init_intensity(self):
        """
        get pushover base shear and acceleration
        """
        pkl_file = f'{self.base_shear_path} for ida.pkl'

        if not os.path.exists(pkl_file):
            print("Reading excel...")

            read_file = f'{self.base_shear_path}.xlsx'

            df = pd.read_excel(
                read_file, sheet_name='Base Reactions', header=1, usecols=3, skiprows=[2])

            # delete max and min string
            df.loc[:, 'Load Case/Combo'] = df['Load Case/Combo'].str[:-4]

            # combine max min
            df = df.groupby('Load Case/Combo', as_index=False,
                            sort=False).agg('max')

            df['Load Case'], df['Scaled Factors'] = df['Load Case/Combo'].str.rsplit(
                '-', 1).str

            df.loc[:, 'FX'] = np.abs(df['FX'])
            # df.loc[:, 'Accel'] = df['FX'] / 299.5941 / 0.81

            print("Creating pickle file ...")
            with open(pkl_file, 'wb') as f:
                pickle.dump(df, f, True)
            print("Done!")

        with open(pkl_file, 'rb') as f:
            df = pickle.load(f)

        self.base_shear = df

    def get_intensity(self):
        """
        get pushover base shear and acceleration
        """
        if self.base_shear is None:
            self._init_intensity()
        return self.base_shear

    def get_story_damage(self):
        """
        get every step pushover story drifts or story displacements
        """
        if self.plotlib.damage_measure == 'story_drifts':
            if self.story_drifts is None:
                self._init_damage()
            return self.story_drifts

        if self.plotlib.damage_measure == 'story_displacements':
            if self.story_displacements is None:
                self._init_damage()
            return self.story_displacements

        return None

    def _get_dm_col(self):
        """
        return 'Drift' or 'Maximum'
        """
        if self.plotlib.damage_measure == 'story_drifts':
            return 'Drift'
        if self.plotlib.damage_measure == 'story_displacements':
            return 'Maximum'

    def get_damage(self):
        """
        condense story drift to max drift
        """
        column = self._get_dm_col()

        story_damage = self.get_story_damage()

        damage = story_damage[story_damage.groupby(
            'Load Case/Combo')[column].transform(max) == story_damage[column]]

        damage = damage.drop_duplicates('Load Case/Combo')

        return damage

    def get_points(self, earthquake):
        """
        get damage and intensity by loadcase and damage_measure
        """
        if self.plotlib.intensity_measure == 'base_shear':
            intensity = self.get_intensity()
            damage = self.get_damage()

            damage = damage.loc[damage['Load Case'] == earthquake, :].copy()
            damage.loc[:, 'Scaled Factors'] = damage[
                'Scaled Factors'].astype('float64')
            damage = damage.sort_values(by=['Scaled Factors'])

            intensity = intensity.loc[
                intensity['Load Case'] == earthquake, :].copy()
            intensity.loc[:, 'Scaled Factors'] = intensity.loc[
                :, 'Scaled Factors'].astype('float64')
            intensity = intensity.sort_values(by=['Scaled Factors'])

            return (
                np.insert(damage[self._get_dm_col()].values, 0, 0),
                np.insert(intensity['FX'].values, 0, 0)
            )

        damage = self.get_damage()
        intensity_measure = self.earthquakes[
            earthquake][self.plotlib.intensity_measure]

        damage_intensity = damage.loc[damage['Load Case']
                                      == earthquake, :].copy()

        damage_intensity.loc[:, 'Scaled Factors'] = damage_intensity.loc[
            :, 'Scaled Factors'].astype('float64') * intensity_measure

        damage_intensity = damage_intensity.sort_values(by=['Scaled Factors'])

        return (
            np.insert(damage_intensity[self._get_dm_col()].values, 0, 0),
            np.insert(damage_intensity['Scaled Factors'].values, 0, 0)
        )

    def interp(self, num=1000):
        """
        use to interp intensity
        """
        damages = pd.DataFrame()
        intensities = pd.DataFrame()
        interp_dm = pd.DataFrame()

        for earthquake in self.earthquakes:
            damage, intensity = self.get_points(earthquake)

            # concat all drift and accel
            damages = pd.concat(
                [damages, pd.DataFrame({earthquake: damage})], axis=1)
            intensities = pd.concat(
                [intensities, pd.DataFrame({earthquake: intensity})], axis=1)

        # scaled to same intensities
        interp_im = np.linspace(
            intensities.min().max(), intensities.max().min(), num=num)

        # interp nan, to delete nan
        damages = damages.interpolate()
        intensities = intensities.interpolate()

        # interpolate to same intensities to damages
        for column in damages:
            interp_dm.loc[:, column] = np.interp(
                interp_im, intensities[column], damages[column])

        return interp_dm, interp_im

    def plot_all(self, *args, **kwargs):
        """
        plot ida in drift and acceleration by load case
        """
        for earthquake in self.earthquakes:
            damage, intensity = self.get_points(earthquake)

            if not damage.size == 0:
                # plt.plot(xnew, f(xnew), label=earthquake, marker='.')
                plt.plot(damage, intensity, label=earthquake,
                         marker='.', *args, **kwargs)
            else:
                print(f'{earthquake} is not in data')

    def plot(self, earthquake, *args, **kwargs):
        """
        plot pushover in drift and acceleration by load case
        """
        damage, intensity = self.get_points(earthquake)
        plt.plot(damage, intensity, *args, **kwargs)

    def plot_median(self, *args, **kwargs):
        """
        plot pushover in drift and acceleration by load case
        """
        damage, intensity = self.interp(num=1000)
        plt.plot(damage.quantile(0.5, axis=1, interpolation='nearest'),
                 intensity, label='median IDA curve', *args, **kwargs)
        # plt.plot(damage, intensity, *args, **kwargs)


def _main():
    stories = {
        'RF': 5,
        '4F': 4,
        '3F': 3,
        '2F': 2,
    }

    earthquakes = {
        'RSN725_SUPER.B_B-POE360': {'sa': 0.548, 'pga': 0.463},
        'RSN900_LANDERS_YER270': {'sa': 0.448, 'pga': 0.224},
        'RSN953_NORTHR_MUL279': {'sa': 0.648, 'pga': 0.343},
        'RSN960_NORTHR_LOS000': {'sa': 0.388, 'pga': 0.426},
        'RSN1111_KOBE_NIS000': {'sa': 0.296, 'pga': 0.483},
        'RSN1116_KOBE_SHI000': {'sa': 0.486, 'pga': 0.336},
        'RSN1148_KOCAELI_ARE090': {'sa': 0.140, 'pga': 0.157},
        'RSN1158_KOCAELI_DZC180': {'sa': 0.343, 'pga': 0.248},
        'RSN1602_DUZCE_BOL090': {'sa': 0.791, 'pga': 0.574},
        'RSN1633_MANJIL_ABBAR--T': {'sa': 0.501, 'pga': 0.460},
        'RSN1787_HECTOR_HEC090': {'sa': 0.402, 'pga': 0.343},
    }

    file_dir = os.path.dirname(os.path.abspath(__file__))

    path = {
        'base_shear_path': 'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/Tradition/base_shear',
        'story_drifts_path': 'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/Tradition/story_drifts',
        'story_displacements_path': 'D:/GitHub/thesis/Models/LowSeismic 4Floor 12M/Tradition/story_displacements'
    }

    pushover = np.array([
        [0, 0],
        [39.511, 213.737],
        [79.622, 328.6849],
        [119.045, 413.073],
        [129.802, 423.8039],
        [179.144, 445.1944],
        [202.067, 452.0568],
    ])

    pushover_sa_sd = np.array([
        [0.821, 0.003],
        [18.009, 0.070],
        [32.853, 0.125],
        [41.262, 0.142],
        [51.253, 0.163],
        [63.122, 0.183],
        [79.854, 0.208],
        [101.558, 0.228],
        [129.980, 0.246],
    ])

    color = {
        'green': np.array([26, 188, 156]) / 256,
        'blue': np.array([52, 152, 219]) / 256,
        'red': np.array([233, 88, 73]) / 256,
        'orange': np.array([230, 126, 34]) / 256,
        'gray': np.array([0.5, 0.5, 0.5]),
        'background': np.array([247, 247, 247]) / 256
    }

    ida = IDA(
        path=path,
        earthquakes=earthquakes,
        stories=stories
    )

    # print(ida.get_intensity())

    # ida.figure(xlim_max=0.025, intensity_measure='pga')
    # ida.plot_all()
    # ida.plot_median()
    # plt.legend(loc='upper left')

    # ida.figure(intensity_measure='sa')
    # ida.plot_median()
    # plt.legend(loc='upper left')

    ida.figure(
        ylim_max=800,
        xlim_max=300,
        intensity_measure='base_shear',
        damage_measure='story_displacements'
    )
    ida.plot_all(color=color['gray'])

    plt.plot(
        pushover[:, 0], pushover[:, 1],
        label='Pushover Curve', color=color['gray'], linestyle='--', marker='.')

    plt.grid(True, which='both', linestyle=':')
    plt.legend(loc='upper left')

    ida.figure(
        ylim_max=0.8,
        xlim_max=200,
        intensity_measure='sa',
        damage_measure='story_displacements'
    )
    ida.plot(
        'RSN1158_KOCAELI_DZC180',
        color=color['gray'], label='IDA Curve', marker='.'
    )

    plt.plot(
        pushover_sa_sd[:, 0], pushover_sa_sd[:, 1],
        label='Pushover Curve', color=color['gray'], linestyle='--', marker='.')

    plt.legend(loc='upper left')
    plt.grid(True, which='both', linestyle=':')

    plt.show()


if __name__ == "__main__":
    _main()
