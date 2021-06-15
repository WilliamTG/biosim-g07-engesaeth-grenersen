How to use Biosim
=================

Welcome to the Bioim projects infopage on how to use and run biosim.
There is not a lot that needs to be in place for you to take your first swing at
our biosimulation.

First you will need to define a map of the island you want to simulate on.
The island is build up via a docstring, and consists of only the letters:
W,D,L,H. Use any other letter or symbol and an error will be raised.
For an example of how an island would look, check out the example file in the package.

.. note::
   Do NOT include any "space" symbols in the island string

Second you will need an initial population of both herbivores and carnivores.
The way you implement them is done in a very specific way, so do exactly as we describe it.
The population is a list, with a dictionary as its first object.
The dictionary consists of two keys: 'loc' and 'pop'.
'loc' shall have a tuple with the coordinate you want to place your animals.
If you would create an island consisting of 10 letters wide og 10 letters tall, then
the top left corner would be coordinate (1,1) while the down right corner would be (10,10).
Remember that you can't place animals in water, this will raise an error.
'pop' shall have a list consisting of dictionaries, where each dictionary is an animal.
The dictionaries shall have three keys: 'species', 'age, 'weight'.
'species' can only have two different values: 'Herbivore' or 'Carnivore'
'age' is an integer, and can't be negative
'weight' can be a float or an integer, but it can't equal zero or be a negative number.
To see an example on how this can be done, check out the example file we have provided in the package.
Create both an initial herbivore population and an initial carnivore population.
The normal way of simulating is to start with the herbivore population.
We will show you how to implement both.

.. note::
   If the structure is not exactly as described you will
   not be able to place the animals on the island.

You can also choose your own seed. The seed can be any integer number you want.
It will only make sure if you run the same simulation with the same seed that the outcome
of the simulation will be the same.

Now that the main parameters as set yuo would need to call the Biosim class.
Do as follows:

sim = Biosim(island_map = map, initial_population=ini_herbs, seed=123456)
This way you start with the herbivore population.

You are now ready to simulate. But if you would like, you can change som parameters to
change the outcome of the simulation.

You can change the animal parameters be calling the method sim.set_animal_parameters().
The method takes two arguments: species and params.
Species is a string and can only be either 'Herbivore' or 'Carnivore'.
params is a dictionary where the key is the parameter you want to change in the form of a string
while the value connected to the key is a float.
To see all the values you are able to change, see the documentation for the animal module.

.. note::
   You can only change parameters that already exists.

You can also change the food you would like to provide the herbivores in the landscapes Lowlands
and Highlands. This can be done by calling the method sim.set_landscape_parameters().
This method also takes two arguments: land and params.
land is a string and can only be either 'L' or 'H'.
parmas is a dictionary, and the only key that can be placed in it is 'f_max'.
The value of 'f_max' can be anything you want, as long as it is an integer value.
The standards as 800 for Lowlands and 300 for Highlands.

After you have set the parameters to your desire you are ready to simulate.
To start simulating you will need to run the simulate method.
This method takes two arguments: num_years and vis_years.
num_years is the number of years you want to simulate. 2- or 300 is the normal amount.
vis_year is just a number for how often you would like the graphics to update.
The standard here is 1.

run:

sim.simulate(num_years=100,vis_years=1)
sim.add_population(population=ini_carns)
sim.simulate(num_years=100,vis_years=1)


If you need a more hands on example, check out the example file provided in the package.
Or if you are wondering what methods are used in the simulation check out the rest of the documentation.

