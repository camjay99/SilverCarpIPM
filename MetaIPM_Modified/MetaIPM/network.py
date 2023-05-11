import numpy as np
import pandas as pd
import scipy.stats as stats
from MetaIPM import path


class network:
    '''Networks contains paths, populated paths, and edges.'''
    def __init__(self, network_name):
        self.network_name = network_name
        self.nodes = []
        self.populated_paths = []

    def show_network_name(self):
        return self.network_name

    def add_nodes(self, nodes_in):
        [self.nodes.append(n) for n in nodes_in]

    def n_nodes(self):
        return len(self.nodes)

    def add_populated_paths(self, paths_in):
        [self.populated_paths.append(n) for n in paths_in]


class network_mesh(network):
    """Adds in network mesh for the population's length distribution."""
    def set_mesh(self, n_years, n_points, min_length, max_length, n_months):
        self.n_points = n_points
        self.min_length = min_length
        self.max_length = max_length
        self.n_years = n_years
        self.n_months = n_months

        self.omega = np.linspace(start=self.min_length,
                                 stop=self.max_length,
                                 num=self.n_points + 2)[1:-1]
        self.h_width = self.omega[1] - self.omega[0]


class network_spawn(network_mesh):
    '''Adds in spawning probability for the network.'''
    def set_spawn(self, spawn_months, spawn_a,
                  spawn_b, stochastic_spawn=True):
        self.spawn_months = spawn_months
        self.spawn_a = spawn_a
        self.spawn_b = spawn_b

        if stochastic_spawn:
            self.spawn_prob = stats.beta.rvs(spawn_a,
                                             spawn_b,
                                             size=self.n_years)
        else:
            self.spawn_prob = stats.beta.mean(spawn_a,
                                              spawn_b).repeat(self.n_years)


class network_spawn_pd(network_spawn):
    '''Sets spawning probability using pandas (pd) data.frame.'''
    def add_network_parameters(self, network_data, stochastic_spawn=True):
        self.set_mesh(network_data['n_years'].values[0],
                      network_data['n_points'].values[0],
                      network_data['min_length'].values[0],
                      network_data['max_length'].values[0],
                      network_data['no_months'].values[0])

        self.set_spawn(
            list(map(int, network_data['spawn_months'].values[0].split(";"))),
            network_data['spawn_a'].values[0],
            network_data['spawn_b'].values[0],
            stochastic_spawn=stochastic_spawn)
        
        self.egg_viability = network_data['egg_viability'].values[0]

    def create_new_spawn_prob(self, network_data, stochastic_spawn=True):
        '''update spawning probability using pandas (pd) data.frame'''
        self.set_spawn(
            list(map(int, network_data['spawn_months'].values[0].split(";"))),
            network_data['spawn_a'].values[0],
            network_data['spawn_b'].values[0],
            stochastic_spawn=stochastic_spawn)


class network_projection():
    """Includes population projection functions for network model."""
    def project_network(self):
        for year in range(self.n_years):
            for month in range(self.n_months):
                current_time_index = year * self.n_months + month

                # Project through time
                for node_idx in self.nodes:
                    node_idx.project_node(year, month, self)

                # Load paths
                for path_idx in self.populated_paths:
                    path_start = path_idx.show_start()
                    for start_node in self.nodes:
                        node_name = start_node.show_node_name()
                        if path_start == node_name:
                            path_idx.add_to_path(
                                node=start_node,
                                year=current_time_index,
                                network=self)

                # Move to new nodes
                for path_idx in self.populated_paths:
                    for end_node in self.nodes:
                        if path_idx.show_end() == end_node.show_node_name():
                            path_idx.add_to_node(
                                node=end_node,
                                year=current_time_index)

                # Remove from old nodes
                for path_idx in self.populated_paths:
                    path_start = path_idx.show_start()
                    for start_node in self.nodes:
                        node_name = start_node.show_node_name()
                        if path_start == node_name:
                            path_idx.subtract_from_node(
                                node=start_node,
                                year=current_time_index)

    def clear_nodes(self):
        for node_idx in self.nodes:
            node_idx.clear_nonstart_group()


class network_populated_paths(network_spawn_pd, network_projection):
    """Includes populated paths as part of the network."""
    def initialize_nodes_in_network(self):
        for nd in self.nodes:
            nd.initialize_node(self)

    def initialize_paths_in_network(self,
                                    transition_data):
        for index, row in transition_data.iterrows():
            path.temp = path.populated_path(
                start_node=transition_data["start"][index],
                end_node=transition_data["end"][index],
                probability=transition_data["prob"][index])
            self.add_populated_paths([path.temp])

    def clear_populated_paths(self):
        self.populated_paths = []

    def create_paths(self,
                     stochastic_pars,
                     transition_data,
                     transition_key_data):
        transition_data_transposed = transition_data.transpose()
        transition_data_transposed.index.name = 'column'
        transition_data_transposed.reset_index(
            inplace=True)

        transition_data_use = pd.merge(
            transition_key_data,
            transition_data_transposed,
            on="column")

        # Either select stochastic output,
        # or use mean of all estimates
        if stochastic_pars:
            column_to_use = np.random.choice(
                transition_data_use.columns[3:])
            transition_data_use['prob'] = transition_data_use.iloc[
                :,
                column_to_use]
        else:
            transition_data_use['prob'] = transition_data_use.iloc[
                :,
                3:].mean(1)

        self.initialize_paths_in_network(transition_data_use)

    def describe_network(self):
        '''
        Describe network's structure.
        '''
        print("\n")
        print(" ~~ ~~~ "*5)
        print("<=>< "*5)
        print("This network is named " + self.show_network_name() + ".")
        print("\n")
        print("The network has " + str(self.n_nodes()) + " nodes.")
        print("\n")
        print("The network has " +
              str(len(self.populated_paths)) +
              " populated paths.")
        print("\n")
        print("--" * 10)
        print("The numerical mesh has " +
              str(self.n_points) +
              " points ranging from " +
              str(self.min_length) +
              " to " +
              str(self.max_length) +
              ".")

        print("\n")
        print("The model is set to run  " + str(self.n_years) + " years.")
        print("\n")
        print("--" * 10)
        print("The following nodes are in the model:")

        for node_idx in self.nodes:
            print("\t" + node_idx.show_node_name())

        print("--" * 10)
        print("The following paths are in the model:")
        for path_idx in self.populated_paths:
            print("\t" +
                  path_idx.show_start() +
                  " to " +
                  path_idx.show_end() +
                  ", with probability " +
                  str(round(path_idx.probability, 3)))
        print("\n")
