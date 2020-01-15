# -*- coding: utf-8 -*-

__author__ = "Anders Huse, Bishnu Poudel"
__email__ = "anhuse@nmbu.no; bipo@nmbu.no"

from biosim.Herbivore_simulation import HSimulation
from biosim.Geography import Geo
from simulation import BioSim
import seaborn as sns
import numpy as np

import matplotlib.pyplot as plt

map = ("""\
    OOOOO
    OJSDO
    OJSMO
    OJSDO
    OOOOO""")
ini_herbs = [{'loc': (1, 1), 'pop': [{'species': 'Herbivore', 'age': 5,
                                      'weight': 100} for _ in range(6)] + [
                                        {'species': 'Carnivore', 'age': 10,
                                         'weight': 500} for _ in range(2)
                                    ]}]
g = Geo(map)  # no particular use here
s = BioSim(map, ini_herbs, seed =1)
# print(s.object_matrix)
# print(g.geo_shape)

row_num = g.geo_shape[0]
column_num = g.geo_shape[1]
total_cells = row_num * column_num

# print(row_num, column_num, total_cells)


# plt.subplots_adjust(wspace=0, hspace=0)

#Herbivore heatmap
h_matrix = np.zeros((row_num, column_num))
c_matrix = np.zeros((row_num, column_num))

for row, list_of_obj in enumerate(s.object_matrix):
    for col, cell in enumerate(list_of_obj):
        for animal in cell.animal_object_list:
            if type(animal).__name__ == "Herbivore":
                h_matrix[row][col] += 1
            else:
                c_matrix[row][col] += 1

# print(h_matrix )
# print(c_matrix)

fig = plt.figure()
ax = fig.add_subplot(223)
ax = sns.heatmap(h_matrix, linewidth=0.5, cmap = "Greens")
ax = fig.add_subplot(224)
ax = sns.heatmap(h_matrix, linewidth=0.5, cmap = "OrRd")


# For the map of the island
color_dict ={"Ocean":2, "Desert":11, "Savannah": 8,
             "Jungle":6, "Mountain":16}

island_matrix = np.zeros((row_num, column_num))

for row, list_of_obj in enumerate(s.object_matrix):
    for col, cell in enumerate(list_of_obj):
        island_matrix[row][col] = color_dict[type(cell).__name__]
# print(island_matrix)

ax = fig.add_subplot(221)
ax = plt.imshow(island_matrix, cmap='terrain', vmax = 20, vmin=1)

# For line plot
h_count = 0
c_count = 0
h_count_list = []
c_count_list = []

for row, list_of_obj in enumerate(s.object_matrix):
    for col, cell in enumerate(list_of_obj):
        for animal in cell.animal_object_list:
            if type(animal).__name__ == "Herbivore":
                h_count += 1
            else:
                c_count += 1

h_count_list.append(h_count)
c_count_list.append(c_count)
print(h_count_list, c_count_list)

ax = fig.add_subplot(222)
ax = plt.plot(h_count_list)
ax = plt.plot(c_count_list)

plt.show()

