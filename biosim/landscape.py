"""
This is the landscape module. The file contains a Environment-class, and subclasses of Environment.
"""

__author__ = "Lars Engesæth / William Grenersen"
__email__ = 'laen@nmbu.no, wigrener@nmbu.no'


class Environments:
    """
    This is the main class for the different Environments on the island.
    The currently implemented environments are the following:
    -   Lowlands;
    -   Highlands;
    -   Desert;
    -   Water.
    This class assumes that the environments are habitable. If this is not the case, it will be
    updated in the subclass.
    """
    habitable = True
    environment_parameter = None

    def __init__(self):
        """Each subclass may have food available."""
        self.food = None

    def reset_food(self):
        """Resets the food for the environment when called."""
        self.food = self.environment_parameter['f_max']


class Lowlands(Environments):
    """
    This is the subclass "Lowlands", which is a subclass of Environments.
    Animals may live and feed here. The default food amount for each year is 800.
    """

    environment_parameter = {'f_max': 800}

    def __init__(self):
        """ The class inherits reset_food from Environments, and defines parameters."""
        super().__init__()
        self.food = self.environment_parameter['f_max']
        self.environment = 'L'

    @classmethod
    def set_lowlands_params(cls, new_params=None):
        """ Method that allows the user to change the default parameter in lowland. """

        if new_params is None:
            cls.environment_parameter = cls.environment_parameter

        elif type(new_params) != dict:
            raise TypeError('Parameter set input must be a dictionary')
        elif 'f_max' not in new_params:
            raise KeyError('All the parameters must already exist in the parameter list')
        elif new_params['f_max'] < 0:
            raise ValueError('All the parameters must be greater than or equal to zero')
        else:
            cls.environment_parameter['f_max'] = new_params['f_max']


class Highlands(Environments):
    """
    This is the subclass "Highlands", which is a subclass of Environments.
    Animals may live and feed here. The default food amount for each year is 300.
    """
    environment_parameter = {'f_max': 300}

    def __init__(self):
        """ The class inherits reset_food from Environments, and defines parameters."""
        super().__init__()
        self.food = self.environment_parameter['f_max']
        self.environment = 'H'

    @classmethod
    def set_highland_params(cls, new_params=None):
        """ Method that allows the user to change the default parameter in highland."""

        if new_params is None:
            cls.environment_parameter = cls.environment_parameter
        elif type(new_params) != dict:
            raise TypeError('Parameter set input must be a dictionary')
        elif 'f_max' not in new_params:
            raise KeyError('All the parameters must already exist in the parameter list')
        elif new_params['f_max'] < 0:
            raise ValueError('All the parameters must be greater than or equal to zero')
        else:
            cls.environment_parameter['f_max'] = new_params['f_max']


class Desert(Environments):
    """
    This is the subclass "Desert", which is a subclass of Environments.
    Animals may live here.
    """
    environment_parameter = {'f_max': 0}

    def __init__(self):
        """The class inherits reset_food from Environments, and defines parameters."""
        super().__init__()
        self.food = self.environment_parameter['f_max']
        self.environment = 'D'


class Water(Environments):
    """
    This is the subclass "Water", which is a subclass of Environments.
    Animals cannot live here.
    """
    habitable = False
    environment_parameter = {'f_max': 0}

    def __init__(self):
        """ This is a subclass of Environments."""
        super().__init__()
        self.environment = 'W'
