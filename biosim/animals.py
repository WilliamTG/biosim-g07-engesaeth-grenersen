"""
A file with the animal class. The file also contains subclasses Herbivore and Carnivore.
"""

import math
import numpy as np
from numba import jit, float64
import random

__author__ = 'William, Lars'
__email__ = 'william.tobias.grenersen@nmbu.no, laen@nmbu.no'


class Animals:
    """
    The main class for animals. This class contains all the methods that are shared for all species
    of animals. Each animal has access to _ani_params_ to use for performing basic tasks.
    """
    _ani_params = {'w_birth': None, 'sigma_birth': None, 'beta': None,
                   'eta': None, 'a_half': None, 'phi_age': None,
                   'w_half': None, 'phi_weight': None, 'mu': None, 'gamma': None,
                   'zeta': None, 'xi': None, 'omega': None, 'F': None, 'DeltaPhiMax': None}

    def __init__(self, age=0, weight=None):
        """
        This constructor initializes the parameters of each new animal. These parameters are
        updated later in each subclass. If the age and weight arent specified, a new animal
        is created with age 0 and a randomly chosen weight from normal distribution.
        :params age: the start-age of the animal.
        :type age: int
        :params weight: the start-weight of the animal.
        :type weight: float
        """

        if weight is None:
            self.weight = np.random.normal(self._ani_params['w_birth'],
                                           self._ani_params['sigma_birth'])
        else:
            self.weight = weight
        self.age = age
        self.fitness = None
        self.species = None

    def change_weight(self, weight_change=None, birth=False):
        """
        A versatile class method to change the weight of an animal.
        If it is called without parameters, it decreases the weight of an animal by the yearly
        weight loss.
        If it is called with a weight_change =! 0 it increases the weight of that animal by the
        amount it eats.
        If it is called as a result of giving birth, it reduces the weight of the animal by
        the child's weight.

        :param weight_change: Weight of food eaten.
        :type weight_change: float
        :param birth: True if it gives birth.
        :type birth: boolean
        """
        if weight_change is None:
            self.weight -= (self._ani_params['eta'] * self.weight)
        elif birth:
            self.weight -= (weight_change * self._ani_params['xi'])
        else:
            self.weight += (self._ani_params['beta'] * weight_change)

    @staticmethod
    @jit(float64(float64, float64, float64, float64, float64, float64))
    def _jit_fitness(phi_age, age, a_half, phi_weight, weight, w_half):
        return (1 / (1 + math.exp(phi_age * (age - a_half)))) * (
                1 / (1 + math.exp(-phi_weight * (weight - w_half))))

    def calculate_fitness(self):
        """
        Calculates the fitness of an animal and returns that value.
        :return: The animal's fitness.
        """
        if self.weight <= 0:
            return 0
        else:
            return self._jit_fitness(self._ani_params['phi_age'], self.age,
                                     self._ani_params['a_half'], self._ani_params['phi_weight'],
                                     self.weight, self._ani_params['w_half'])

    def aging(self):
        """
        Ages an animal's age by 1 each year.
        """
        self.age += 1

    def birth(self, cell, number_animals=None):
        """
        Calculates if an animal gives birth.
        :params number_animals: number of the relevant species in that cell.
        :type number_animals: int
        :params cell: the relevant cell.
        :type cell: object

        :return: True if it gives birth.
        """

        if number_animals is None \
                or number_animals <= 1 \
                or ((self.species == 'Herbivore') and (self in cell.graveyard)) \
                or self.weight < self._ani_params['zeta'] * (self._ani_params['w_birth'] +
                                                             self._ani_params['sigma_birth']) \
                or self.weight < np.random.normal(self._ani_params['w_birth'],
                                                  self._ani_params['sigma_birth']):
            return False
        else:
            return random.random() < min(1, self._ani_params['gamma'] *
                                         self.calculate_fitness() * number_animals - 1)

    def death(self):
        """
        Calculates the probability that an animals dies based on its fitness and weight.
        :return: True if the animals dies.
        """
        if self.weight <= 0:
            return True
        else:
            return random.random() < self._ani_params['omega'] * (1 - self.calculate_fitness())


class Herbivore(Animals):
    """
    This is a subclass of Animals.
    It replaces parameters defined in the main class, and gives the Herbivore its basic parameters.
    It inherits the methods of Animals.

    params: species, age, weight and fitness.
    """

    _ani_params = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                   'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.6,
                   'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25, 'gamma': 0.2,
                   'zeta': 3.2, 'xi': 1.8, 'omega': 0.4, 'F': 10.0, 'DeltaPhiMax': 10}

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)
        self.species = 'Herbivore'

    @classmethod
    def set_herb_params(cls, new_params=None):
        """
        Sets or changes the parameters for the species.

        :param new_params: the new parameters
        :type new_params: dict
        """

        if new_params is None:
            cls._ani_params = cls._ani_params
        elif type(new_params) != dict:
            raise TypeError('Input parameters must come in a dictionary')
        else:
            for key in new_params:
                if key not in cls._ani_params:
                    raise KeyError('Input parameters must already exist in the old parameters')
                elif not isinstance(new_params[key], (int, float)):
                    raise TypeError('Input parameters must consist of numbers')
                elif new_params[key] < 0:
                    raise ValueError('Input parameters must be positive')
                elif 'omega' in new_params and new_params['omega'] > 1:
                    raise ValueError('omega must be between 0 and 1')
                elif 'eta' in new_params and new_params['eta'] > 1:
                    raise ValueError('eta must be between 0 and 1')
                elif key != 'DeltaPhiMax':
                    cls._ani_params[key] = new_params[key]


class Carnivore(Animals):
    """
    This is a subclass of Animals.
    It replaces parameters defined in the main class, and gives the Carnivore its basic parameters:
    species, age, weight and fitness.
    This class also has a method for hunting herbivores. It inherits other methods from Animals.
    """

    _ani_params = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75,
                   'eta': 0.125, 'a_half': 70.0, 'phi_age': 0.5,
                   'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4, 'gamma': 0.8,
                   'zeta': 3.5, 'xi': 1.1, 'omega': 0.3, 'F': 65.0, 'DeltaPhiMax': 9}

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)
        self.species = 'Carnivore'

    @classmethod
    def set_carn_params(cls, new_params=None):
        """
        Sets or changes the parameters for the given animal

        :param new_params: the new parameters
        :type new_params: dict
        """

        if new_params is None:
            cls._ani_params = cls._ani_params
        elif type(new_params) != dict:
            raise TypeError('Input parameters must come in a dictionary')
        else:
            for key in new_params:
                if key not in cls._ani_params:
                    raise KeyError('Input parameters must already exist in the old parameters')
                elif not isinstance(new_params[key], (int, float)):
                    raise TypeError('Input parameters must consist of numbers')
                elif new_params[key] < 0:
                    raise ValueError('Input parameters must be positive')
                elif 'omega' in new_params and new_params['omega'] > 1:
                    raise ValueError('omega must be between 0 and 1')
                elif 'eta' in new_params and new_params['eta'] > 1:
                    raise ValueError('eta must be between 0 and 1')
                elif 'DeltaPhiMax' in new_params and new_params['DeltaPhiMax'] == 0:
                    raise ValueError('DeltaPhiMax cannot be equal to zero')
                else:
                    cls._ani_params[key] = new_params[key]

    def hunt_herbivores(self, herbivore_fitness, carnivore_fitness):
        """
        This method decides if a carnivore is able to capture and eat a herbivore.
        It returns true if that happens.

        :param herbivore_fitness: The fitness of the hunted herbivore.
        :type herbivore_fitness: float
        :param carnivore_fitness: The fitness of the hunting carnivore.
        :type carnivore_fitness: float
        :return: True if the carnivore catches the herbivore.
        """

        if 0 < carnivore_fitness - herbivore_fitness < 10:
            return random.random() < ((carnivore_fitness - herbivore_fitness) /
                                      self._ani_params['DeltaPhiMax'])
        elif carnivore_fitness > self._ani_params['DeltaPhiMax']:
            return True
