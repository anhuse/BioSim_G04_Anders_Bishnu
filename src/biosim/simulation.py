# -*- coding: utf-8 -*-

__author__ = "Anders Huse"
__email__ = "huse.anders@gmail.com"

from biosim.Cycle import Cycle
from biosim.Geography import Geo
from biosim.Visualization import Visualization

class BioSim:
    def __init__(
        self,
        island_map,
        ini_pop,
        seed,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        self.seed = 1
        self.island_map = Geo(island_map)
        self.ini_pop = ini_pop
        # self.seed = 1
        self.object_matrix = self.island_map.object_matrix

        for one_location_list in self.ini_pop:
            x, y = one_location_list['loc'][0], one_location_list['loc'][1]
            self.object_matrix[x][y].set_population(one_location_list)

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """

        #animal, up_par
        # Herbivore.up_par()
        # Carnivore.up_par()

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        # if landscape == 'S':
        #     Savannah.params.update(params)
        # else:
        #     Jungle.params.update(params)


    def simulate(self, num_years=1, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """
        c = Cycle(self.object_matrix)
        c.food_grows()
        c.animals_eat()
        c.animals_reproduce()
        c.animals_migrate()

        v = Visualization(self.object_matrix)

        v._set_graphics()

#        for each year to simulate
  #          cycle
    #        v.update_graphics()


    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """


    @property
    def year(self):
        """Last year simulated."""

    @property
    def num_animals(self):
        """Total number of animals on island."""

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island."""

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""


if __name__ == "__main__":
    map = ("""\
        OOOOO
        OJSDO
        OJSMO
        OJSMO
        OOOOO""")
    ini_herbs = [{'loc': (1, 1), 'pop': [{'species': 'Herbivore', 'age': 5,
                                          'weight': 100} for _ in range(10)] + [
                                         {'species': 'Carnivore', 'age': 10,
                                          'weight': 500} for _ in range(4)
                                         ]}]

    s = BioSim(map, ini_herbs, seed = 1)

    print(s.object_matrix[1][1].animal_object_list[1].weight)

    s.simulate()

    print(s.object_matrix[1][1].animal_object_list[1].weight)

