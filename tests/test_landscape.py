from biosim.landscape import Lowlands, Highlands, Desert, Water
import pytest

class TestParameterChange:

    def test_lowlands_list_as_params(self):
        """
        Test to see if an error is raised when inserting a list as environment params
        """
        with pytest.raises(TypeError):
            assert Lowlands().set_lowlands_params(['f_max', 70])

    def test_lowlands_wrong_param(self):
        """
        Test to see if an error is raised when inserting a parameter
        """
        with pytest.raises(KeyError):
            assert Lowlands().set_lowlands_params({'food':700})

    def test_lowlands_fmax_negative(self):
        """
        Test to see if an error is raised when giving f_max a negative number
        """
        with pytest.raises(ValueError):
            assert Lowlands().set_lowlands_params({'f_max':-800})

    def test_higlands_list_as_params(self):
        """
        Test to see if an error is raised when inserting a list as environment params
        """
        with pytest.raises(TypeError):
            assert Highlands().set_highland_params(['f_max', 70])

    def test_highlands_wrong_param(self):
        """
        Test to see if an error is raised when inserting a parameter
        """
        with pytest.raises(KeyError):
            assert Highlands().set_highland_params({'food':700})

    def test_highlands_fmax_negative(self):
        """
        Test to see if an error is raised when giving f_max a negative number
        """
        with pytest.raises(ValueError):
            assert Highlands().set_highland_params({'f_max':-800})




def test_food():
    e = Lowlands()
    assert e.food is not None

def test_rest_food():
    e = Lowlands()
    e.food = None
    e.reset_food()
    assert e.food is not None

def test_environment_parameter():
    e = Lowlands()
    assert e.environment is not None
    assert type(e.environment) == str

