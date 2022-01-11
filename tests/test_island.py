import pytest
from biosim.island import IslandCell
from biosim.landscape import Highlands
from biosim.animals import Herbivore, Carnivore


def test_animal_spawn():
    island_cell = IslandCell(None, None)
    island_cell.initialize_herbs(10, 4, 20)
    island_cell.initialize_carns(10, 5, 20)
    assert island_cell.get_pop_herb() == 10
    assert island_cell.get_pop_carn() == 10
    assert island_cell.cell_herb_pop[0].age == 4
    assert island_cell.cell_herb_pop[0].weight == 20
    assert island_cell.cell_carn_pop[0].age == 5
    assert island_cell.cell_carn_pop[0].weight == 20


def test_species():
    island_cell = IslandCell(None, None)
    for herb in island_cell.current_herb_infolist:
        assert herb['species'] == 'Herbivore'


def test_aging():
    """
    The test will see if the aging function works as intended
    The Herbovire object should go from age 0 to 1
    """
    island_cell = IslandCell()
    island_cell.initialize_herbs()
    assert island_cell.cell_herb_pop[0].age == 0
    island_cell.execute_aging()
    assert island_cell.cell_herb_pop[0].age == 1


def test_weight_loss():
    """
        The test will test for the yearly weight loss function
        If it does, the Herbivore objects weight should reduce with 5% of its current weight
    """
    island_cell = IslandCell()
    island_cell.initialize_herbs()
    test_weight = island_cell.cell_herb_pop[0].weight
    island_cell.execute_weightloss()
    assert island_cell.cell_herb_pop[0].weight == \
           test_weight - (test_weight * island_cell.cell_herb_pop[0]._ani_params['eta'])


@pytest.mark.parametrize('n_herbs,n_carns', [(10, 10), (20, 20)])
class TestFeedingAndHunting:

    @pytest.fixture(autouse=True)
    def create_island(self, n_herbs, n_carns):
        self.island = IslandCell(Highlands())
        self.island.initialize_herbs(n_herbs, 5, 10)
        self.island.initialize_carns(n_carns, 20, 50)

    def test_test_execute_feeding_random(self):
        """
        The function should shuffle the list before feeding starts
        I am testing to see if the list shuffles as intended.
        This will only happen to Herbivores
        This test might fail as there is a possibility that the same herb
        can get the same index
        """

        test_herb = self.island.cell_herb_pop[0]
        self.island.execute_feeding()
        assert test_herb != self.island.cell_herb_pop[0]

    def test_weight_gain_feeding(self):
        """
        The test will see if the feeding function works as intended.
        If it does, the Herbivore should eat and increase its weight
        Since the function shuffles the init_herb_list I have to
        find the index of the object I am testing.
        """

        test_weight = self.island.cell_herb_pop[0].weight
        first_herb = self.island.cell_herb_pop[0]
        self.island.execute_feeding()
        index = self.island.cell_herb_pop.index(first_herb)
        assert self.island.cell_herb_pop[index].weight > test_weight

    def test_not_enough_food(self):
        """
        To test if the Herbivores will eat every food, and check
        that not everybody gain weight
        """
        self.weight = []
        self.island.location.food = 90
        n_ani_eat = self.island.location.food / self.island.cell_herb_pop[0]._ani_params['F']
        self.island.execute_feeding()

        for herb in self.island.cell_herb_pop:
            self.weight.append(herb.weight)

        assert self.weight.count(10) == self.island.get_pop_herb() - int(n_ani_eat)

    @pytest.mark.xfail()
    def test_weight_gain_hunt(self, mocker):
        """
        The test will see if the carnivores will in fact eat Herbivores and
        gain weight from this.
        """
        # det kan være noe galt med fitness funksjonen da sannsynlgiheten for
        # å drepe en herb er ekstremt lav.
        mocker.patch('random.random', return_value=0)
        self.island.cell_carn_pop = [Carnivore(5, 50)]
        self.island.cell_herb_pop = [Herbivore()]
        self.island.location.food = 0
        test_weight = self.island.cell_carn_pop[0].weight
        self.island.execute_feeding()
        assert test_weight < self.island.cell_carn_pop[0].weight

    def test_hunt_herbivore_death(self, mocker):
        """
        Test to see if herbivores die when eaten be carnivores
        Since Herbivores are not removed from the population list in the feeding function
        we have to run the update_list function to see if they die.
        """
        mocker.patch('random.random', return_value=0)

        old_len = len(self.island.cell_herb_pop)
        self.island.execute_feeding()
        self.island.remove_dead()
        assert len(self.island.cell_herb_pop) < old_len

    def test_fittest_carn_eats_first(self, mocker):
        """
        Tests to see if the fittest of three carnivores is the
        one that gets to eat the Herbivore
        """
        mocker.patch('random.random', return_value=0)

        self.island.cell_carn_pop = [Carnivore(1, 20), Carnivore(1, 20), Carnivore(5, 30)]
        self.island.cell_herb_pop = [Herbivore()]
        self.island.location.food = 0
        self.island.execute_feeding()

        assert self.island.cell_carn_pop[2].weight > 30 \
               and self.island.cell_carn_pop[0].weight == 20


@pytest.mark.parametrize('n_herbs,n_carns', [(10, 10), (20, 20)])
class TestBirthDeath:

    @pytest.fixture(autouse=True)
    def create_island(self, n_herbs, n_carns):
        self.island = IslandCell()
        self.island.initialize_herbs(n_herbs, 5, 40)
        self.island.initialize_carns(n_carns, 5, 40)

    def test_birth(self):
        """
        Test to see if the birth function in fact will give birth to new
        Herbivores and Carnivores by running it 10 times.
        """
        test_herb = self.island.get_pop_herb()
        test_carn = self.island.get_pop_carn()
        old_num_herbs = self.island.get_pop_herb()
        old_num_carns = self.island.get_pop_carn()
        for _ in range(10):
            self.island.execute_birth()
            # See that the number of animals does not decrease
            num_herb = self.island.get_pop_herb()
            num_carn = self.island.get_pop_carn()
            assert num_herb >= old_num_herbs
            assert num_carn >= old_num_carns
            old_num_herbs, old_num_carns = num_herb, num_carn

        assert self.island.get_pop_herb() > test_herb
        assert self.island.get_pop_carn() > test_carn

    def test_death(self, mocker):
        """
        Test to see if the death function works
        In the test every animal should die since the probability of dying
        is sett to 100% by mocker.patch
        """

        mocker.patch('random.random', return_value=1)

        self.island.execute_death()

        assert self.island.get_pop_herb() == 0
        assert self.island.get_pop_carn() == 0

