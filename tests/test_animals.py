# -*- encoding: utf-8 -*-

"""
Test suite for animals.py
"""

__author__ = "Lars Engesæth / NMBU"
__email__ = 'laen@nmbu.no'

from biosim.animals import Herbivore, Carnivore
import random
import math
import scipy.stats as stats
import pytest


def test_blank_constructor():
    """Do animals have access to weight and age with blank inputs?"""
    h = Herbivore()
    assert h.weight is not None and h.weight > 0
    assert h.age == 0


def test_constructor():
    """Are input variables properly assigned?"""
    h = Herbivore(age=4, weight=10)
    assert len(h._ani_params) > 0
    assert h.age == 4
    assert h.weight == 10


def test_gaussian_weight():
    """Statistical test to see if the birth-weight is within the expected interval.
    Expect this test to fail 10%(?) of times."""
    h = Herbivore()
    ALPHA = 0.01
    random.seed(100)
    probability = h._ani_params['w_birth']

    animals = 100
    n = sum(h.weight for _ in range(animals))

    mean = animals * probability

    var = animals * probability * (1 - probability)
    z = (n - mean) / math.sqrt(abs(var))
    phi = 2 * stats.norm.cdf(-abs(z))
    assert phi > ALPHA


def test_natural_weight_loss():
    """Does animals lose weight each year as expected?"""
    h = Herbivore()
    weight_h = h.weight
    h.change_weight()
    assert weight_h - (h._ani_params['eta'] * weight_h) == h.weight

    c = Carnivore()
    weight_c = c.weight
    c.change_weight()
    assert weight_c - (c._ani_params['eta'] * weight_c) == c.weight


def test_birth_weight_loss():
    """Does birthing an animal reduce the animals weight to a non-negative number?"""
    h1 = Herbivore(weight=20)
    h2 = Herbivore()
    h1.change_weight(h2.weight, True)
    assert h1.weight < 20
    assert h1.weight > 0


def test_herbivore_eating_weight_change():
    """Does herbivores gain weight correctly?"""
    h1 = Herbivore()
    weight = h1.weight + 10 * h1._ani_params['beta']
    h1.change_weight(10)
    assert weight == h1.weight


def test_calculate_fitness_negative_weight():
    """Does negative weight give fitness: 0?"""
    h1 = Herbivore(weight=-1)
    assert h1.calculate_fitness() == 0


def test_calculate_fitness_range():
    """Fitness should always be in this interval: (0,1)"""
    for number in range(1, 100):
        h1 = Herbivore(age=number, weight=number)
        assert 0 < h1.calculate_fitness() < 1


def test_negative_weight_equals_death():
    """Does animals with negative weight die?"""
    h1 = Herbivore(weight=-5)
    assert h1.death()

#def test_hunt_herb(mocker):
 #   mocker.patch('random.random', return_value=1)
  #  c = Carnivore()
   # h = Herbivore()
    #c_fitness = c.calculate_fitness()
    ##h_fitness = h.calculate_fitness()
    #assert c.hunt_herbivores(h_fitness,c_fitness) == True

class TestSetAniParams:

    def test_set_Herb_parmas_non_dict(self):
        """
        Test to see if an error is raised if a non dictionary is inserted as a parameter
        replacement
        """
        with pytest.raises(TypeError):
            assert Herbivore().set_herb_params(new_params=['zeta', 0.4])

    def test_set_Herb_params_wrong_key(self):
        """
        Test to see if an error is raised if non-existing key is inserted as a parameter
        replacement
        """
        with pytest.raises(KeyError):
            assert Herbivore().set_herb_params(new_params={'z':16})

    def test_set_Herb_params_non_int_float(self):
        """
        Test to see if an error is raised if a non int or float is inserted as a parameter
         replacement
        """
        with pytest.raises(TypeError):
            assert Herbivore().set_herb_params(new_params={'zeta':'four'})

    def test_set_Herb_params_negative_number(self):
        """
        Test to see if an error is raised if a negative number is inserted as a parameter
        replacement
        """
        with pytest.raises(ValueError):
            assert Herbivore().set_herb_params(new_params={'zeta': -5})

    def test_set_Herb_params_wrong_omega(self):
        """
        Test to see if an error is raised when parameter Omega is replaced with a number
        that is not between 0 and 1
        """
        with pytest.raises(ValueError):
            assert Herbivore().set_herb_params(new_params={'omega': 1.5})

    def test_set_Herb_params_wrong_eta(self):
        """
        Test to see if an error is raised when parameter Omega is replaced with a number
        that is not between 0 and 1
        """
        with pytest.raises(ValueError):
            assert Herbivore().set_herb_params(new_params={'eta': 1.5})

    def test_set_Carn_parmas_non_dict(self):
        """
        Test to see if an error is raised if a non dictionary is inserted as a parameter
        replacement
        """
        with pytest.raises(TypeError):
            assert Carnivore().set_carn_params(new_params=['zeta', 0.4])

    def test_set_Carn_params_wrong_key(self):
        """
        Test to see if an error is raised if non-existing key is inserted as a parameter
        replacement
        """
        with pytest.raises(KeyError):
            assert Carnivore().set_carn_params(new_params={'z':16})

    def test_set_Carn_params_non_int_float(self):
        """
        Test to see if an error is raised if a non int or float is inserted as a parameter
         replacement
        """
        with pytest.raises(TypeError):
            assert Carnivore().set_carn_params(new_params={'zeta':'four'})

    def test_set_Carn_params_negative_number(self):
        """
        Test to see if an error is raised if a negative number is inserted as a parameter
        replacement
        """
        with pytest.raises(ValueError):
            assert Carnivore().set_carn_params(new_params={'zeta': -5})

    def test_set_Carn_params_wrong_omega(self):
        """
        Test to see if an error is raised when parameter Omega is replaced with a number
        that is not between 0 and 1
        """
        with pytest.raises(ValueError):
            assert Carnivore().set_carn_params(new_params={'omega': 1.5})

    def test_set_Carn_params_wrong_eta(self):
        """
        Test to see if an error is raised when parameter Omega is replaced with a number
        that is not between 0 and 1
        """
        with pytest.raises(ValueError):
            assert Carnivore().set_carn_params(new_params={'eta': 1.5})
