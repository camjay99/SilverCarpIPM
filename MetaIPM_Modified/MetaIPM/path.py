from MetaIPM import group
import numpy as np


class path():
    """
    Plain paths with only starts and ends.
    """
    def __init__(self, start_node, end_node, probability):
        self.start_node = start_node
        self.end_node = end_node
        self.probability = probability

    def show_start(self):
        return self.start_node

    def show_end(self):
        return self.end_node

    def show_probability(self):
        return self.probability


class populated_path(path):
    """
    Includes groups in paths and functions
    to transfer groups to-and-from nodes.
    """
    def add_to_path(self, node, year, network):
        self.hold_groups = []
        for grp in node.groups:
            biomass = node.calculate_node_biomass(year, network.omega)
            migration = self.probability * (2 - np.exp(-node.g_migration * biomass))
            grp_temp = group.group_populated(grp.show_group_name())
            grp_temp.population = (grp.show_group_pop_dist(year) *
                                   migration)
            self.hold_groups.append(grp_temp)

    def add_to_node(self, node, year):
        for path_grp in self.hold_groups:
            for node_grp in node.groups:
                if path_grp.show_group_name() == node_grp.show_group_name():
                    node_grp.population[:, year] += path_grp.population

    def subtract_from_node(self, node, year):
        for path_grp in self.hold_groups:
            for node_grp in node.groups:
                if path_grp.show_group_name() == node_grp.show_group_name():
                    # Next lines prevents negative (or zombie) fish
                    if (node_grp.population[:, year] -
                            path_grp.population).min() < 0:
                        node_grp.population[:, year] *= 0.0
                    else:
                        node_grp.population[:, year] -= path_grp.population
