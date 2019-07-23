"""
ida data and function
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics
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

    def get_interp(self, percentage=0.5, num=1000, mean=False):
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

        if not mean:
            interp_dm = interp_dm.quantile(q=percentage, axis=1).values
        else:
            # interp_dm = interp_dm.where(interp_dm < 0.5, np.nan)
            interp_dm = interp_dm.mean(axis=1).values

        return interp_dm, interp_im

    def plot_all(self, *args, log=False, **kwargs):
        """
        plot ida in drift and acceleration by load case
        """
        if log:
            plot = plt.loglog
        else:
            plot = plt.plot

        for eq in self.earthquakes:
            damage, intensity = self.get_points(eq)

            line, = plot(damage, intensity, marker='.', *args, **kwargs)

        return line

    def plot(self, earthquake, *args, log=False, **kwargs):
        """
        plot pushover in drift and acceleration by load case
        """
        if log:
            plot = plt.loglog
        else:
            plot = plt.plot

        damage, intensity = self.get_points(earthquake)
        plot(damage, intensity, *args, **kwargs)

    def plot_interp(self, *args, percentage=0.5, log=False, mean=False, **kwargs):
        """
        plot pushover in drift and acceleration by load case
        """
        if log:
            plot = plt.loglog
        else:
            plot = plt.plot

        damage, intensity = self.get_interp(percentage, mean=mean)
        plot(damage, intensity, *args, **kwargs)


def _main():
    from config import data

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

    color = {
        'green': np.array([26, 188, 156]) / 256,
        'blue': np.array([52, 152, 219]) / 256,
        'red': np.array([233, 88, 73]) / 256,
        'orange': np.array([230, 126, 34]) / 256,
        'gray': np.array([0.5, 0.5, 0.5]),
        'background': np.array([247, 247, 247]) / 256
    }

    # plt.figure()
    plt.figure(figsize=(6.4, 8.6))
    plt.subplot(2, 1, 1)
    plt.xlabel(r'Maximum interstorey drift ratio, $\theta_{max}$')
    plt.ylabel(r'"first-mode"spectral acceleration $S_a(T_1$, 5%)(g)')
    # plt.title('Convention versus Optimization eleven IDA curves')
    plt.title('(a) Convention versus Optimization eleven IDA curves')

    line_tradition = tradition.plot_all(color=color['gray'], linestyle='--')
    line_multi = multi.plot_all(color=color['gray'])

    plt.axvline(
        0.04,
        linestyle='-.',
        color=color['gray']
    )

    plt.xlim(0, 0.05)
    plt.ylim(0, 2.5)
    plt.grid(True, which='both', linestyle=':')
    plt.legend(
        (line_tradition, line_multi),
        ('Convention Curves', 'Optimization Curves'),
        loc='upper left'
    )
    plt.tight_layout()

    # tradition.plot_interp(
    #     label='Convention', linewidth=3.0, color=color['blue'])
    # multi.plot_interp(
    #     label='Optimization', linewidth=3.0, color=color['green'])
    print('Optimization')
    damage, intensity = multi.get_interp(0.16)
    print(round(np.interp(0.04, damage, intensity), 2))
    damage, intensity = multi.get_interp()
    print(round(np.interp(0.04, damage, intensity), 2))
    damage, intensity = multi.get_interp(0.84)
    print(round(np.interp(0.04, damage, intensity), 2))

    print('Convention')
    damage, intensity = tradition.get_interp(0.16)
    print(round(np.interp(0.04, damage, intensity), 2))
    damage, intensity = tradition.get_interp()
    print(round(np.interp(0.04, damage, intensity), 2))
    damage, intensity = tradition.get_interp(0.84)
    print(round(np.interp(0.04, damage, intensity), 2))
    plt.subplot(2, 1, 2)
    # plt.figure()
    plt.xlabel(r'Maximum interstorey drift ratio, $\theta_{max}$')
    plt.ylabel(r'"first-mode"spectral acceleration $S_a(T_1$, 5%)(g)')
    # plt.title('Convention versus Optimization median IDA curves')
    plt.title('(b) Convention versus Optimization median IDA curves')

    # multi.plot_all(log=True, color=color['gray'])
    # tradition.plot_all(log=True, color=color['gray'])
    multi.plot_interp(
        percentage=0.16,
        log=True, label='Optimization', linewidth=2.0, color=color['green'])
    tradition.plot_interp(
        percentage=0.16,
        log=True, label='Convention', linewidth=2.0, color=color['green'], linestyle='--')

    multi.plot_interp(
        log=True, label='Median Optimization', linewidth=2.0, color=color['blue'])
    tradition.plot_interp(
        log=True, label='Median Convention', linewidth=2.0, color=color['blue'], linestyle='--')

    # tradition.plot_interp(
    #     mean=True,
    #     log=True, label='Median Convention', linewidth=2.0, color=color['blue'], linestyle='--')
    # multi.plot_interp(
    #     mean=True,
    #     log=True, label='Median Optimization', linewidth=2.0, color=color['blue'])
    multi.plot_interp(
        percentage=0.84,
        log=True, label='Optimization', linewidth=2.0, color=color['red'])
    tradition.plot_interp(
        percentage=0.84,
        log=True, label='Convention', linewidth=2.0, color=color['red'], linestyle='--')

    plt.axvline(
        0.04,
        linestyle='-.',
        color=color['gray']
    )

    plt.xlim(right=0.15)
    plt.ylim(top=2.5)
    plt.grid(True, which='both', linestyle=':')
    plt.legend(
        ('16% Optimization', '16% Convention', '50% Optimization',
         '50% Convention', '84% Optimization', '84% Convention'),
        loc='upper left'
    )

    plt.tight_layout()

    # plt.figure()
    # plt.xlabel(r'Maximum interstorey drift ratio, $\theta_{max}$')
    # plt.ylabel(r'"first-mode"spectral acceleration $S_a(T_1$, 5%)(g)')
    # plt.title('Convention versus Optimization median IDA curves')

    # multi.plot_all(color=color['gray'])
    # tradition.plot_all(color=color['gray'], linestyle='--')
    # multi.plot_interp(
    #     percentage=0.16,
    #     label='Optimization', linewidth=2.0, color=color['green'])
    # tradition.plot_interp(
    #     percentage=0.16,
    #     label='Convention', linewidth=2.0, color=color['green'], linestyle='--')

    # multi.plot_interp(
    #     label='Median IDA Curve', linewidth=2.0, color=color['gray'])
    # tradition.plot_interp(
    #     label='Median Convention', linewidth=2.0, color=color['gray'], linestyle='--')

    # multi.plot_interp(
    #     percentage=0.84,
    #     label='Optimization', linewidth=2.0, color=color['red'])
    # tradition.plot_interp(
    #     percentage=0.84,
    #     label='Convention', linewidth=2.0, color=color['red'], linestyle='--')

    # plt.axvline(
    #     0.04,
    #     linestyle='-.',
    #     color=color['gray']
    # )

    # plt.xlim(0, 0.05)
    # plt.ylim(0, 1.5)
    # plt.grid(True, which='both', linestyle=':')
    # plt.legend(
    # ('16% Optimization', '16% Convention', '50% Optimization',
    #  '50% Convention', '84% Optimization', '84% Convention'),
    #     loc='upper left'
    # )

    plt.show()


if __name__ == "__main__":
    _main()
