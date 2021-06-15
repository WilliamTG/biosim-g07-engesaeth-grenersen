from biosim.simulation import BioSim
import textwrap
from biosim.animals import Herbivore
import matplotlib.pyplot as plt

geogr = """\
WWWWWWWWWWWWWWWWWWWWW
WWWWWWWWHWWWWLLLLLLLW
WHHHHHLLLLWWLLLLLLLWW
WHHHHHHHHHWWLLLLLLWWW
WHHHHHLLLLLLLLLLLLWWW
WHHHHHLLLDDLLLHLLLWWW
WHHLLLLLDDDLLLHHHHWWW
WWHHHHLLLDDLLLHWWWWWW
WHHHLLLLLDDLLLLLLLWWW
WHHHHLLLLDDLLLLWWWWWW
WWHHHHLLLLLLLLWWWWWWW
WWWHHHHLLLLLLLWWWWWWW
WWWWWWWWWWWWWWWWWWWWW"""
geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (10, 10),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(150)]}]

ini_carns = [{'loc': (10, 10),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(40)]}]

sim = BioSim(island_map=geogr, ini_pop=ini_herbs, seed=100, img_dir='..\data')
sim.set_animal_parameters('Herbivore', {'zeta': 3.2, 'xi': 1.8})
sim.set_animal_parameters('Carnivore', {'a_half': 70, 'phi_age': 0.5,
                                            'omega': 0.3, 'F': 65,
                                            'DeltaPhiMax': 9.})
sim.set_landscape_parameters('L', {'f_max': 700})

sim.simulate(num_years=100, vis_years=2, img_years=None)
# sim.make_movie('mp4')
sim.add_population(ini_carns)
sim.simulate(num_years=300, vis_years=2)

plt.show()
