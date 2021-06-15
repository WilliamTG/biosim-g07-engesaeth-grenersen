"""
The island module contain the main class for cells that compose the island.
"""

from biosim.animals import Herbivore, Carnivore
import random
import operator
from random import randint



class IslandCell:
    """
    This main class uses the features from the class Animals and the class Environments.
    The class defines all methods that each cell must perform. These methods are used by the
    simulation-file.

    This class will also maintain the population in each cell and stores this information in lists.
    """

    def __init__(self, location=None):
        """
        Each cell needs the following parameters to function.
        """
        self.location = location
        self.current_herb_infolist = []
        self.current_carn_infolist = []
        self.graveyard = []
        self.cell_herb_pop = []
        self.cell_carn_pop = []
        self.fitness_herb_list = []
        self.fitness_carn_list = []
        self.coordinate = (0, 0)
        self.newborn_herb = []
        self.newborn_carn = []
        self.emigrated_herb = []
        self.emigrated_carn = []
        self.neighbors = [None, None, None, None]
        self.herbs = []
        self.herbs_incoming = []
        self.carns = []
        self.carns_incoming = []

    def remove_dead(self):
        """
        This method updates the list of animals. It uses a list comprehension
        to remove items that are in the graveyard (i.e. dead animals).
        """
        self.cell_herb_pop = [herb for herb in self.cell_herb_pop
                              if herb not in self.graveyard]
        self.cell_carn_pop = [carn for carn in self.cell_carn_pop
                              if carn not in self.graveyard]
        self.graveyard = []

    def execute_aging(self):
        """
        This method performs the aging process on the two lists of animals in a cell.
        """
        for herb in self.cell_herb_pop:
            herb.aging()
        for carn in self.cell_carn_pop:
            carn.aging()

    def execute_weightloss(self):
        """
        This method makes all animals lose weight each year.
        """
        for herb in self.cell_herb_pop:
            herb.change_weight()
        for carn in self.cell_carn_pop:
            carn.change_weight()

    def execute_feeding(self):
        """
        This method feeds the animals. The first part of the method feeds herbivores in a random
        order until there is no more food in the cell or every herbivore has been fed. At the
        end of this feeding process, the food for the herbivores is reset.

        The second part of the method deals with the hunting of herbivores. To do this, the lists
        of animals must be sorted by their fitness. The carnivores are sorted in reverse.
        Herbivores that are eaten are removed before another carnivore tries to eat it.
        Carnivores hunt until they are fed or until they have tried to catch each living herbivore.
        """

        random.shuffle(self.cell_herb_pop)
        for herb in self.cell_herb_pop:
            if self.location.food >= herb._ani_params['F']:
                herb.change_weight(herb._ani_params['F'])
                self.location.food -= herb._ani_params['F']
            herb.fitness = herb.calculate_fitness()
        self.location.reset_food()

        for carn in self.cell_carn_pop:
            carn.fitness = carn.calculate_fitness()
        self.fitness_herb_list = sorted(self.cell_herb_pop, key=operator.attrgetter("fitness"))
        self.fitness_carn_list = sorted(self.cell_carn_pop, key=operator.attrgetter("fitness"),
                                        reverse=True)

        for carnivore in self.fitness_carn_list:
            consumed = 0
            total_consumed = 0
            remaining_appetite = carnivore._ani_params['F']
            for herbivore in self.fitness_herb_list:
                if carnivore.hunt_herbivores(herbivore.fitness, carnivore.fitness):
                    self.graveyard.append(herbivore)
                    consumed += herbivore.weight
                    total_consumed += herbivore.weight
                    remaining_appetite -= herbivore.weight
                    if total_consumed >= carnivore._ani_params['F']:
                        carnivore.change_weight(remaining_appetite)
                        break
                    carnivore.change_weight(consumed)
                    consumed = 0
                    carnivore.fitness = carnivore.calculate_fitness()
            self.fitness_herb_list = [herb for herb in self.fitness_herb_list
                                      if herb not in self.graveyard]

    def execute_birth(self):
        """
        This method makes the animals check if they procreate.
        New animals are given a random weight and age set to 0.
        Newborns are added after each animal has tried to give birth.
        """
        self.newborn_herb = []
        for herb in self.cell_herb_pop:
            if herb.birth(self, len(self.cell_herb_pop)):
                new_animal = Herbivore()
                self.newborn_herb.append(new_animal)
                herb.change_weight(weight_change=new_animal.weight, birth=True)
        self.cell_herb_pop.extend(self.newborn_herb)

        self.newborn_carn = []
        for carn in self.cell_carn_pop:
            if carn.birth(0, len(self.cell_carn_pop)):
                new_animal = Carnivore()
                self.newborn_carn.append(new_animal)
                carn.change_weight(weight_change=new_animal.weight, birth=True)
        self.cell_carn_pop.extend(self.newborn_carn)

    def execute_death(self):
        """
        This method adds animals that die by random probability to the graveyard. They are removed
        from the cell in the remove_dead()-method.
        """
        for herb in self.cell_herb_pop:
            if herb.death():
                self.graveyard.append(herb)
        for carn in self.cell_carn_pop:
            if carn.death():
                self.graveyard.append(carn)

    def migrate_herbivore(self, herb, neighbor):
        """
        This method migrates 1 herbivore into the selected neighbor's list for incoming herbivores.
        I also adds this herbivore to the emigrated_herb-list so that it can be removed later.
        :param herb: The herbivore that tries to migrate.
        :type herb: Animals-object.
        :param neighbor: The neighboring cell-object in which the animal tries to migrate to.
        :type neighbor: IslandCell-object.
        """

        if neighbor is not None and neighbor.location.environment != 'W':
            neighbor.herbs_incoming.append(herb)
            self.emigrated_herb.append(herb)

    def migrate_carnivore(self, carn, neighbor):
        """
        This methods migrates 1 carnivore into the selected neighbor's list for incoming carnivores.
        It also adds this carnivore to the emigrated_carn-list so that it can be removed later.
        :param carn: The carnivore that tries to migrate.
        :type carn: Animals-object.
        :param neighbor: The neighboring cell-object in which the animal tries to migrate to.
        :type neighbor: IslandCell-object.
        """

        if neighbor is not None and neighbor.location.environment != 'W':
            neighbor.carns_incoming.append(carn)
            self.emigrated_carn.append(carn)

    def merge_migration(self):
        """
        This method merges carnivore list and herbivore lists for the cell.
        The lists of incoming animals are emptied after they have transferred the animal objects.
        """
        self.cell_herb_pop.extend(self.herbs_incoming)
        self.herbs_incoming = []

        self.cell_carn_pop.extend(self.carns_incoming)
        self.carns_incoming = []

    def execute_migration(self):
        """
        This method tests each animal in a cell to evaluate if it migrates, and where it would
        migrate to.
        If the animal migrates, the direction it moves is also determined. The direction is
        randomly selected among the cell's neighbors.
        The method removes animals that migrate after all animals have been evaluated in the cell.
        """
        self.emigrated_herb = []
        for herbivore in self.cell_herb_pop:
            if herbivore._ani_params['mu'] * herbivore.calculate_fitness() >= random.random():
                direction = randint(0, 3)
                self.migrate_herbivore(herbivore, self.neighbors[direction])
        self.cell_herb_pop = [herb for herb in self.cell_herb_pop
                              if herb not in self.emigrated_herb]

        self.emigrated_carn = []
        for carnivore in list(self.cell_carn_pop):
            if carnivore._ani_params['mu'] * carnivore.calculate_fitness() >= random.random():
                direction = randint(0, 3)
                self.migrate_carnivore(carnivore, self.neighbors[direction])
        self.cell_carn_pop = [carn for carn in self.cell_carn_pop
                              if carn not in self.emigrated_carn]

    def initialize_herbs(self, num_ani=None, age=0, weight=10):
        """
        This method is used for testing purposes.
        It initializes a population og herbivores in a given cell

        :param num_ani: Number of herbivores yoo want to initialize
        :type num_ani: int
        :param age: The age you want to give to the animal(s)
        :type age: int
        :param weight: the weight you want to give the animal(s)
        :type weight: int ,float
        """
        if num_ani is None:
            num_ani = 10
        self.cell_herb_pop = [Herbivore(age, weight) for _ in range(num_ani)]

    def initialize_carns(self, num_ani=None, age=0, weight=10):
        """
        This method is used for testing purposes.
        It initializes a population of carnivores in a given cell

        :param num_ani: Number of carnivores yoo want to initialize
        :type num_ani: int
        :param age: The age you want to give to the animal(s)
        :type age: int
        :param weight: the weight you want to give the animal(s)
        :type weight: int ,float
        """
        if num_ani is None:
            num_ani = 10
        self.cell_carn_pop = [Carnivore(age, weight) for _ in range(num_ani)]

    def get_pop_herb(self):
        """
        This method is used for testing purposes.
        Counts number of herbivores in a cell on island.
        :return: number of Herbivores in IslandCell.
        """
        return len(self.cell_herb_pop)

    def get_pop_carn(self):
        """
        This method is used for testing purposes.
        Counts number of carnivores in a cell on island.
        :return: number of Carnivores in IslandCell.
        """
        return len(self.cell_carn_pop)
