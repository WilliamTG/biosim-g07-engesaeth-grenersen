from biosim.simulation import BioSim
import textwrap
import pytest


class TestErrorsInit:

    @pytest.fixture(autouse=True)
    def create_island_map(self):
        """
        Creating an island for all tests in this class.
        """
        self.geogr = """\
        WWWWW
        WHLHW
        WDHDW
        WWWWW"""
        self.geogr = textwrap.dedent(self.geogr)

    def test_wrong_letter_islad(self):
        """
        The test will see if Biosim raises error if anything else than W, H, L or D is
        inserted in island
        """
        self.geogr = """\
                WWWWWWWWW
                WWWHLHWWW
                WWLHLHLWW
                WHHQQQHHW
                WWDDLDDWW
                WWWDDDWWW
                WWWWWWWWW"""
        self.geogr = textwrap.dedent(self.geogr)
        with pytest.raises(ValueError):
            BioSim(island_map=self.geogr)

    def test_ini_pop_non_list(self):
        """
        Test to see if an error is raised if initial_population is not a list.
        """
        ini_herb = {'loc': (2, 3), 'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 20}]}

        with pytest.raises(TypeError):
            BioSim(island_map=self.geogr, ini_pop=ini_herb)

    def test_ini_pop_non_dict(self):
        """
        Test to see if an error is raised if initial_population is not a dict in a list
        """
        ini_herb = [[{'loc': (2, 3), 'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 20}]}]]

        with pytest.raises(TypeError):
            BioSim(island_map=self.geogr, ini_pop=ini_herb)

    def test_ini_pop_wrong_keys(self):
        """
        Test to see if an error is raised if keys loc and pop not in initial_population
        """
        ini_herb = [{'coordinate': (2, 3), 'animals': [{'species': 'Herbivore', 'age': 1, 'weight': 20}]}]

        with pytest.raises(KeyError):
            BioSim(island_map=self.geogr, ini_pop=ini_herb)

    def test_loc_not_tuple(self):
        """
        Test to see if an error is raised if loc is not a tuple
        """
        ini_herb = [{'loc': [2, 3], 'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 20}]}]

        with pytest.raises(TypeError):
            BioSim(island_map=self.geogr, ini_pop=ini_herb)

    def test_loc_tuple_three_numbers(self):
        """
        Test to see if an error is raised if loc tuple is more than two numbers
        """
        ini_herb = [{'loc': (2, 3, 2), 'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 20}]}]

        with pytest.raises(IndexError):
            BioSim(island_map=self.geogr, ini_pop=ini_herb)

    def test_loc_tuple_float(self):
        """
        Test to see if an error is raised if loc tuple is not int
        """
        ini_herb = [{'loc': (1.4, 1.6), 'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 20}]}]

        with pytest.raises(TypeError):
            BioSim(island_map=self.geogr, ini_pop=ini_herb)

    def test_loc_tuple_zero(self):
        """
        Test to see if an error is raised if loc tuple is equal zero
        """
        ini_herb = [{'loc': (0, 0), 'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 20}]}]

        with pytest.raises(ValueError):
            BioSim(island_map=self.geogr, ini_pop=ini_herb)

    def test_pop_not_list(self):
        """
        Test to see if an error is raised if pop is not a list
        """
        ini_herb = [{'loc': (2, 3), 'pop': {'species': 'Herbivore', 'age': 1, 'weight': 20}}]

        with pytest.raises(TypeError):
            BioSim(island_map=self.geogr, ini_pop=ini_herb)

    def test_pop_not_list_in_dict(self):
        """
        Test to see if an error is raised if pop is not a dict in a list
        """
        ini_herb = [{'loc': (2, 3), 'pop': [['species', 'Herbivore', 'age', 1, 'weight', 20]]}]

        with pytest.raises(TypeError):
            BioSim(island_map=self.geogr, ini_pop=ini_herb)

    def test_pop_dict_four_values(self):
        """
        Test to see if an error is raised if dict in pop has four values
        """
        ini_herb = [{'loc': (2, 3), 'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 20, 'fitness': 0.70}]}]

        with pytest.raises(ValueError):
            BioSim(island_map=self.geogr, ini_pop=ini_herb)

    def test_pop_dict_age_weight_not_int_float(self):
        """
        Test to see if an error is raised if age and/or weight in dict in pop is not an int or float
        """
        ini_herb = [{'loc': (2, 3), 'pop': [{'species': 'Herbivore', 'age': 1.5, 'weight': 'four'}]}]

        with pytest.raises(ValueError):
            BioSim(island_map=self.geogr, ini_pop=ini_herb)

    def test_pop_dict_age_weight_negative_or_zero(self):
        """
        Test to see if an error is raised if age and/or weight in dict in pop equals zero
        """
        ini_herb = [{'loc': (2, 3), 'pop': [{'species': 'Herbivore', 'age': -5, 'weight': 0}]}]

        with pytest.raises(ValueError):
            BioSim(island_map=self.geogr, ini_pop=ini_herb)

    def test_pop_dict_species_not_herb_or_carn(self):
        """
        Test to see if an error is raised if species is not herb or carn
        """
        ini_herb = [{'loc': (2, 3), 'pop': [{'species': 'Fish', 'age': 5, 'weight': 20}]}]

        with pytest.raises(NameError):
            BioSim(island_map=self.geogr, ini_pop=ini_herb)

    def test_place_animal_in_water(self):
        """
        Test to see if an error is raised if species is not herb or carn
        """
        ini_herb = [{'loc': (1, 1), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}]

        with pytest.raises(TypeError):
            BioSim(island_map=self.geogr, ini_pop=ini_herb)


class TestMapNeighborCoordinateMigrate:

    @pytest.fixture(autouse=True)
    def create_island_map(self):
        """
        Creating the map and population so we don't have to in every test
        """
        self.geogr = """\
            WWWWW
            WHLHW
            WDHDW
            WWWWW"""
        self.geogr = textwrap.dedent(self.geogr)
        self.ini_herbs = [{'loc': (2, 3),
                           'pop': [{'species': 'Herbivore',
                                    'age': 5,
                                    'weight': 50}
                                   for _ in range(100)]}]
        self.sim = BioSim(island_map=self.geogr, ini_pop=self.ini_herbs)

    def test_islandcell_correct_object(self):
        """
        Test to see if the map is created correctly, and that a specific cell
        has the correct environment.
        """
        assert self.sim.island[13].location.environment == 'D'

    def test_islandcell_correct_coordiante(self):
        """
        Test to see if the coordinate given to a specific cell is the correct one
        """
        assert self.sim.island[0].coordinate == (1, 1)
        assert self.sim.island[12].coordinate == (3, 3)

    def test_negihboring_cells(self):
        """
        Test to see if the neighboring cells to a specific cell are the correct ones
        """
        neighbors = self.sim.island[7].neighbors
        assert self.sim.island[6] in neighbors
        assert self.sim.island[8] in neighbors
        assert self.sim.island[12] in neighbors
        assert self.sim.island[2] in neighbors

    def test_migration(self):
        """
        Testing to see if animals will move between its neighbors.
        Not a bullet proof way of testing, but it works.
        """

        self.sim.set_animal_parameters('Herbivore',
                                       {'mu': 1, 'omega': 0, 'gamma': 0,
                                        'a_half': 1000})

        self.sim.island[7].execute_migration()
        self.sim.island[7].neighbors[0].merge_migration()
        self.sim.island[7].neighbors[1].merge_migration()
        self.sim.island[7].neighbors[2].merge_migration()
        self.sim.island[7].neighbors[3].merge_migration()

        count = 0
        for cell in self.sim.island[7].neighbors:
            count += cell.get_pop_herb()
        count += self.sim.island[7].get_pop_herb()

        assert self.sim.island[7].get_pop_herb() != 100
        assert count == 100


class TestParameterChange:

    @pytest.fixture(autouse=True)
    def create_island_map(self):
        """
        Creating the map and population so we don't have to in every test
        """
        self.geogr = """\
                WWWWW
                WHLHW
                WDHDW
                WWWWW"""
        self.geogr = textwrap.dedent(self.geogr)
        self.ini_herbs = [{'loc': (2, 3),
                           'pop': [{'species': 'Herbivore',
                                    'age': 5,
                                    'weight': 20}
                                   for _ in range(5)]}]
        self.sim = BioSim(island_map=self.geogr, ini_pop=self.ini_herbs)

    @pytest.fixture
    def reset_params(self):
        yield
        self.sim.set_animal_parameters('Herbivore')
        self.sim.set_landscape_parameters('L')

    def test_no_species(self):
        """
        Test to see in an error is raised if species is not specified in method
        """
        with pytest.raises(TypeError):
            assert self.sim.set_animal_parameters(params={'zeta': 3.2, 'xi': 1.8})

    def test_wrong_species(self):
        """
        Test to see in an error is raised if wrong species is implemented in method
        """
        with pytest.raises(NameError):
            assert self.sim.set_animal_parameters(species='Fish', params={'zeta': 3.2, 'xi': 1.8})

    def test_ani_parmameter_change(self):
        """
        Test to see if the parameters really change if the method is called
        """
        test_zeta = self.sim.island[7].cell_herb_pop[0]._ani_params['zeta']
        test_xi = self.sim.island[7].cell_herb_pop[0]._ani_params['xi']
        self.sim.set_animal_parameters(species='Herbivore', params={'zeta': 3.6, 'xi': 1.9})
        zeta = self.sim.island[7].cell_herb_pop[0]._ani_params['zeta']
        xi = self.sim.island[7].cell_herb_pop[0]._ani_params['xi']

        assert zeta != test_zeta
        assert xi != test_xi
        assert zeta == 3.6
        assert xi == 1.9

    def test_no_land(self):
        """
        Test to see if an error is raised if no land is specified
        """
        with pytest.raises(TypeError):
            assert self.sim.set_landscape_parameters(params={'f_max': 700})

    def test_wrong_land(self):
        """
        Test to see if an error is raised if wrong land is specified
        """
        with pytest.raises(NameError):
            assert self.sim.set_landscape_parameters(land='W', params={'f_max': 700})

    def test_land_parameter_change(self):
        """
        Test to see if the changes we implement really happen with right parameters implemented
        """
        test_f_max = self.sim.island[7].location.environment_parameter['f_max']
        self.sim.set_landscape_parameters('L', {'f_max': 900})
        f_max = self.sim.island[7].location.environment_parameter['f_max']
        assert f_max != test_f_max
        assert f_max == 900
