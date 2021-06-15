from biosim.island import IslandCell
from biosim.landscape import Water, Lowlands, Highlands, Desert
from biosim.animals import Herbivore, Carnivore
from biosim import animals
from biosim import landscape
import textwrap
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gs
import os
import subprocess
import numpy as np
import random


_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'


_DEFAULT_GRAPHICS_DIR = os.path.join('..', 'data')
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_MOVIE_FORMAT = 'mp4'


class BioSim:
    def __init__(self, island_map=None, ini_pop=[], seed=None, ymax_animals=20,
                 cmax_animals={'Herbivore': 10, 'Carnivore': 20}, hist_specs=None,
                 img_dir=None, img_name=_DEFAULT_GRAPHICS_NAME, img_fmt='png', img_base=None):
        if seed is None:
            random.seed(100)
        else:
            random.seed(seed)
        self.island = []
        self.letter_island = island_map
        self.total_herb_pop = 0
        self.total_carn_pop = 0
        self.num_animals = 0
        self.num_animals_per_species = {'Carnivore': 0, 'Herbivore': 0}
        self.cycles = 50
        self._fig = None
        self._herb_heat = None
        self._herb_axis = None
        self._carn_heat = None
        self._carn_axis = None
        self._mean_ax = None
        self._mean_line = None
        self.island_map = None
        self._img_ctr = 0
        self._img_fmt = img_fmt
        self.herbivore_line = None
        self.carnivore_line = None
        self.animal_dictionary = {}
        self.island_dataframe = None
        self.herbivore_dataframe = None
        self.carnivore_dataframe = None
        self.year = 0
        self.final_year = None
        self.axt = None

        if img_dir is not None:
            self._img_base = os.path.join(img_dir, img_name)
        else:
            self._img_base = img_base
        self.map_split = island_map.split('\n')
        self.map_length = len(self.map_split[0])
        for index in range(len(self.map_split)):
            if len(self.map_split[index-1]) != self.map_length:
                raise ValueError("All map rows must be have equal lenght.")

        if len(self.map_split) > 3:
            if 'L' in (self.map_split[0] or self.map_split[-1]):
                raise ValueError('The island must be surrounded by water')
            elif 'H' in (self.map_split[0] or self.map_split[-1]):
                raise ValueError('The island must be surrounded by water')
            elif 'D' in (self.map_split[0] or self.map_split[-1]):
                raise ValueError('The island must be surrounded by water')

            for row in self.map_split:
                if row[0] != 'W':
                    raise ValueError('The island must be surrounded by water')
                elif row[-1] != 'W':
                    raise ValueError('The island must be surrounded by water')

        for letter in island_map:
            if letter == 'W':
                self.island.append(IslandCell(Water()))
            elif letter == 'L':
                self.island.append(IslandCell(Lowlands()))
            elif letter == 'H':
                self.island.append(IslandCell(Highlands()))
            elif letter == 'D':
                self.island.append(IslandCell(Desert()))
            elif letter == '\n':
                pass
            else:
                raise ValueError("Input map must consist of Water ('W'), Lowland('L'),\
                                 Desert('D'), Highland('H')")
        # Give each cell its coordinate
        r = 1
        c = 1
        i = 0
        for cell in self.island:
            cell.coordinate = (r, c)
            c += 1
            i += 1
            if i == (self.map_length * r):
                r += 1
                c = 1
        # find each cells neighboring cells
        for cell in self.island:
            index = self.island.index(cell)
            if index + 1 <= len(self.island) - 1:
                cell.neighbors[0] = self.island[index + 1]
            if index - 1 >= 0:
                cell.neighbors[1] = self.island[index - 1]
            if index - self.map_length > 0:
                cell.neighbors[2] = self.island[index - self.map_length]
            if index + self.map_length < len(self.island):
                cell.neighbors[3] = self.island[index + self.map_length]

        # find index to place animals in

        if type(ini_pop) != list:
            raise TypeError('Input population must be a list')
        elif len(ini_pop) == 0:
            pass
        elif type(ini_pop[0]) != dict:
            raise TypeError('Input population list must contain a dictionary')
        else:
            for key in ini_pop[0]:
                if key not in ['loc', 'pop']:
                    raise KeyError('Input population dictionary must only contain loc and pop')
                elif key == 'loc':
                    if type(ini_pop[0][key]) != tuple:
                        TypeError('Input location must be a tuple')
                    elif len(ini_pop[0][key]) != 2:
                        raise IndexError('Input loc must consist of two numbers')
                    else:
                        for value in ini_pop[0][key]:
                            if type(value) != int:
                                raise TypeError("Input loc tuple must consist of two integers")
                            elif value <= 0:
                                raise ValueError(
                                    "Input integer must be a positive number and not zero")
                        for cell in self.island:
                            if cell.coordinate == ini_pop[0]['loc']:
                                index = self.island.index(cell)
                elif key == 'pop':
                    if type(ini_pop[0][key]) != list:
                        raise TypeError('Input population must be a list')
                    else:
                        for dic in ini_pop[0][key]:
                            if type(dic) != dict:
                                raise TypeError(
                                    'Input population must come in the form of dictionaries '
                                    'in the list')
                            elif len(dic) != 3:
                                raise ValueError(
                                    "Dictionary must contain three keys: species,age,weight")
                            elif "species" and "age" and "weight" not in dic:
                                raise ValueError(
                                    "Dictionary must contain three keys: species,age,weight")
                            elif type(dic['age']) != int and type('weight') not in [int, float]:
                                raise ValueError(
                                    "Age must be an integer and weight must be an integer or float")
                            elif dic['age'] < 0 or dic['weight'] <= 0:
                                raise ValueError("Age must be a positive number and \
                                weight must not equal zero and be positive")
                            elif dic['species'] not in ['Herbivore', 'Carnivore']:
                                raise NameError('Species must be a herbivore or carnivore')

                            elif dic['species'] == 'Herbivore':
                                if self.island[index].location.environment == 'W':
                                    raise TypeError(
                                        "Animals can't swim, do not place them in water")
                                self.island[index].cell_herb_pop.append \
                                    (Herbivore(dic['age'], dic['weight']))
                            else:
                                self.island[index].cell_carn_pop.append \
                                    (Carnivore(dic['age'], dic['weight']))

    def add_population(self, population=None):
        """This method adds a population to a islandcell-object.
        :param population: the population the user adds to the island.
        :type population: list

        ## Note: There should be ValueErrors in this method, but the raises lead to bugs,
        so they were removed in favor of a correct plot.
        """
        for cell in self.island:
            if cell.coordinate == population[0]['loc']:
                if population[0]['pop'][0]['species'] == 'Herbivore':
                    for dic in population[0]['pop']:
                        cell.cell_herb_pop.append(Herbivore(dic['age'], dic['weight']))
                elif population[0]['pop'][0]['species'] == 'Carnivore':
                    for dic in population[0]['pop']:
                        cell.cell_carn_pop.append(Carnivore(dic['age'], dic['weight']))

    def set_animal_parameters(self, species, params=None):
        if species is None:
            raise TypeError('Please specify a species')
        elif species not in ['Herbivore', 'Carnivore']:
            raise NameError('Species must be a herbivore or carnivore')
        elif species == 'Herbivore':
            animals.Herbivore.set_herb_params(new_params=params)
        elif species == 'Carnivore':
            animals.Carnivore.set_carn_params(new_params=params)

    def set_landscape_parameters(self, land, params=None):
        if land is None:
            raise TypeError('Please specify a landscape')
        elif land not in ['L', 'H']:
            raise NameError('Cell input must be lowlands or higlands')
        if land == 'L':
            landscape.Lowlands.set_lowlands_params(new_params=params)
        elif land == 'H':
            landscape.Highlands.set_highland_params(new_params=params)

    def simulate(self, num_years=None, vis_years=1, img_years=None):
        """
        This method performs the simulation. The method takes num_years to determine the length of
        the simulation, and then iterates through every cell on the island.
        This method also updates the visual graphs, so that the user can see the development.
        If the user want, this method can also save figures and create a video of these images
        and save that video to the disk.
        """
        if num_years is None:
            num_years = 50

        self.cycles = num_years

        if img_years is None:
            img_years = vis_years

        self.final_year = self.year + self.cycles

        self._setup_graphics()

        while self.year < self.final_year:

            if self.year % vis_years == 0:
                self._update_graphics(self.year)

            #if self.year % img_years == 0:
            #    self.save_graphics()

            for cell in self.island:
                if cell.location.habitable:
                    cell.execute_feeding()
                    cell.execute_birth()
                    cell.execute_migration()
            for cell in self.island:
                if cell.location.habitable:
                    cell.merge_migration()
                    cell.execute_aging()
                    cell.execute_weightloss()
                    cell.execute_death()
                    cell.remove_dead()
                    self.update_herb_counter(cell.cell_herb_pop)
                    self.update_carn_counter(cell.cell_carn_pop)
            self.update_num_animals()
            self._update_population_graph(self.year)
            self.total_herb_pop = 0
            self.total_carn_pop = 0

            self.year += 1

    def make_movie(self, movie_fmt=_DEFAULT_MOVIE_FORMAT):
        """
        Creates MPEG4 movie from visualization images saved.
        ..:note: Requires ffmpeg for MP4 and magick for GIF
        The movie is stored as img_base + movie_fmt
        """

        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == 'mp4':
            try:
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

    def save_graphics(self):
        """Save graphics with filename as given"""
        if self._img_base is None:
            return
        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1

    def build_dataframe(self):
        """This method builds Pandas dataframes that are used in the visualization of
        the heat maps for carnivores and herbivores. The method builds a dictionary that
        is transformed into a main dataframe, that is turned into a map for each species."""
        self.animal_dictionary = {'x': [], 'y': [], 'Herbivores': [], 'Carnivores': []}

        for cell in self.island:
            self.animal_dictionary['x'].append(cell.coordinate[0])
            self.animal_dictionary['y'].append(cell.coordinate[1])
            self.animal_dictionary['Herbivores'].append(len(cell.cell_herb_pop))
            self.animal_dictionary['Carnivores'].append(len(cell.cell_carn_pop))

        self.island_dataframe = pd.DataFrame(self.animal_dictionary)
        self.herbivore_dataframe = self.island_dataframe.pivot('x', 'y', 'Herbivores')
        self.carnivore_dataframe = self.island_dataframe.pivot('x', 'y', 'Carnivores')

    def update_herb_counter(self, herbs):
        """This method counts total number of herbivores on the island."""
        self.total_herb_pop += len(herbs)

    def update_carn_counter(self, carns):
        """This method counts total number of carnivores on the island."""
        self.total_carn_pop += len(carns)

    def update_num_animals(self):
        self.num_animals_per_species = {'Carnivore': self.total_carn_pop,
                                        'Herbivore': self.total_herb_pop}
        self.num_animals = self.num_animals + self.total_carn_pop + self.total_herb_pop

    def _setup_graphics(self):
        """This method creates subplots for the visualization before the simulation begins."""
        if self._fig is None:
            self._fig = plt.figure()
            self._gs = self._fig.add_gridspec(3, 6, height_ratios=[0.5, 0.4, 0.5],
                                              bottom=0.1, right=0.9, top=0.9)

        if self._herb_heat is None:
            self._herb_heat = self._fig.add_subplot(self._gs[0:1, 0:3])
            self._herb_heat.set_title('Herbivore distribution')
            self._herb_axis = None

        if self._carn_heat is None:
            self._carn_heat = self._fig.add_subplot(self._gs[0:1, 3:6])
            self._carn_heat.set_title('Carnivore distribution')
            self._carn_axis = None

        self.population_axis = None
        if self.population_axis is None:
            self.population_axis = self._fig.add_subplot(self._gs[1:2, 0:3])
            self.population_axis.set_title('Number of animals')
            self.population_axis.set_ylabel('Number of animals (1000s)')
            self.population_axis.set_yticks([0, 5000, 10000, 15000, 20000])
            self.population_axis.set_yticklabels(['0', '5', '10', '15', '20'])
            self.population_axis.set_xlabel('Years')
        self.population_axis.set_xlim(0, self.final_year)
        self.population_axis.set_ylim(1, 17000)

        if self.herbivore_line is None:
            population_graph = self.population_axis.plot(np.arange(0, self.cycles),
                                                         np.full(int(self.cycles), np.nan),
                                                         np.arange(0, self.cycles),
                                                         np.full(int(self.cycles), np.nan))
            self.herbivore_line = population_graph[0]
            self.carnivore_line = population_graph[1]
            self.population_axis.legend(('Herbivores', 'Carnivores'))
        else:
            x_data, y_data = self.herbivore_line.get_data()
            z_data, v_data = self.carnivore_line.get_data()
            z_new = np.arange(z_data[-1] + 1, self.final_year)
            x_new = np.arange(x_data[-1] + 1, self.final_year)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                v_new = np.full(z_new.shape, np.nan)
                self.herbivore_line.set_data(np.hstack((x_data, x_new)), np.hstack((y_data, y_new)))
                self.carnivore_line.set_data(np.hstack((z_data, z_new)), np.hstack((v_data, v_new)))

        if self.island_map is None:
            #                   R    G    B
            rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                         'L': (0.0, 0.5, 0.25),  # dark green
                         'H': (0.0, 1.0, 0.5),  # light green
                         'D': (1.0, 0.8, 0.4)}  # light yellow

            map_rgb = [[rgb_value[column] for column in row]
                       for row in self.letter_island.splitlines()]

            axim = self._fig.add_subplot(self._gs[1:2, 3:6], label='map')

            axim.imshow(map_rgb)
            axim.set_xticks(range(len(map_rgb[0])))
            axim.set_xticklabels(range(1, 1 + len(map_rgb[0])), rotation=-45)
            axim.set_yticks(range(len(map_rgb)))
            axim.set_yticklabels(range(1, 1 + len(map_rgb)))

            axlg = self._fig.add_subplot(self._gs[1:2, 3:6], label='legend')
            axlg.axis('off')
            legend_height = 0.15
            legend_base = 0.4
            for ix, name in enumerate(('Water', 'Lowland',
                                       'Highland', 'Desert')):
                axlg.add_patch(plt.Rectangle((0.8, ix * legend_height + legend_base), 0.05, 0.1,
                                             edgecolor='none',
                                             facecolor=rgb_value[name[0]]))
                axlg.text(0.87, ix * legend_height + legend_base, name, transform=axlg.transAxes)

        if self.axt is None:
            self.axt = self._fig.add_subplot(self._gs[2:3, 3:4])
            self.axt.axis('off')  # turn off coordinate system

            self.template = 'Year: {:5d}'
            self.txt = self.axt.text(0.5, 0.5, self.template.format(0),
                                     horizontalalignment='center',
                                     verticalalignment='center',
                                     transform=self.axt.transAxes)

    def _update_graphics(self, year):
        """Updates graphics with current data."""
        self.build_dataframe()
        self._update_system_map(self.herbivore_dataframe, self.carnivore_dataframe)
        self.txt.set_text(self.template.format(year))
        plt.pause(1e-6)

    def _update_system_map(self, herbivore_stats, carnivore_stats):
        """
        Update the heat maps for carnivore and herbivore. They are initialized if they
        are None, or updated if they are already drawn.
        """
        if self._herb_axis is not None:
            self._herb_axis.set_data(herbivore_stats)
        else:
            self._herb_axis = self._herb_heat.imshow(herbivore_stats, interpolation='nearest',
                                                     vmin=0,
                                                     vmax=160)
            plt.colorbar(self._herb_axis, ax=self._herb_heat, orientation='vertical')

        if self._carn_axis is not None:
            self._carn_axis.set_data(carnivore_stats)
        else:
            self._carn_axis = self._carn_heat.imshow(carnivore_stats, interpolation='nearest',
                                                     vmin=0,
                                                     vmax=80)
            plt.colorbar(self._carn_axis, ax=self._carn_heat, orientation='vertical')

    def _update_population_graph(self, year):
        """ This method plots the population graph, which is updated each year."""
        herbivore_data = self.herbivore_line.get_ydata()
        herbivore_data[year] = self.total_herb_pop
        self.herbivore_line.set_ydata(herbivore_data)

        carnivore_data = self.carnivore_line.get_ydata()
        carnivore_data[year] = self.total_carn_pop
        self.carnivore_line.set_ydata(carnivore_data)


if __name__ == '__main__':
    ini_herbs = [{'loc': (1, 1),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(10)]}]

    geography = """L"""
    geography = textwrap.dedent(geography)

    sim = BioSim(island_map=geography, ini_pop=ini_herbs)
    sim.simulate(num_years=100)
