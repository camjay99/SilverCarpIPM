import numpy as np
import scipy.stats as stats
from MetaIPM import recruitment


class group:
    '''Groups contain distributions of individuals.'''
    def __init__(self, group_name):
        self.group_name = group_name

    def show_group_name(self):
        '''Print name of group.'''
        return self.group_name

    def set_start_pop(self, start_pop,
                      initial_mu,
                      initial_sd,
                      n_years,
                      n_months,
                      n_points,
                      omega):
        '''
        Set starting population.
        Parameters
        ----------
        start_pop : real
            Total number of individuals at start
        initial_mu : real
            Initial population log-normal mean.
        initial_sd : real
            Initial population log-normal standard deviation.
        n_years : int
            Number of years for simulation.
        n_months : int
            Number of months (or annual sub-division) for simulation.
        n_points : int
            Number of points in mesh (or annual sub-division) for simulation.
        omega :
            Network's mesh.
        '''
        self.age_0 = np.zeros((n_years + 1))
        self.population = np.zeros([n_points, ((n_years * n_months) + 1)])

        pop_dist_raw = stats.lognorm.pdf(omega,
                                         loc=0,
                                         scale=initial_mu,
                                         s=initial_sd)

        pop_dist_scaled = pop_dist_raw / pop_dist_raw.sum() * start_pop

        self.population[:, 0] = pop_dist_scaled

    def show_group_pop_dist(self, year):
        '''Show population distriubtion of group for a year.'''
        return self.population[:, year]

    def show_group_pop_total(self, year):
        '''Show total population of group for a year.'''
        return self.population[:, year].sum()

    def set_reproduction(self,
                         ratio_at_birth=0.5,
                         sigma_j=0.10,
                         recruit=recruitment.Logistic_recruitment(
                             alpha=1_000,
                             beta=10,
                             min_recruit=0,
                             max_recruit=10_000),
                         produce_eggs=True):
        '''Set reproduction for a group.'''
        self.ratio_at_birth = ratio_at_birth
        self.sigma_j = sigma_j
        self.recruit = recruit
        self.produce_eggs = produce_eggs

    def group_spawn(self,
                    year,
                    length_weight,
                    maturity_prob,
                    omega
                    ):
        '''Have spawning occur in a group.'''
        if self.produce_eggs:
            #biomass_in = (
            #    length_weight(omega) *
            #    maturity_prob(omega) *
            #    self.show_group_pop_dist(year)).sum()
            return (self.recruit(length_weight(omega))*self.show_group_pop_dist(year)).sum()
        else:
            return 0.0


class group_populated(group):
    '''Group with population distribution.'''
    def add_group_parameters(self, node, index, node_group_data, network):
        '''Add group parameters.'''
        self.set_start_pop(
                node_group_data["StartPop"][index],
                node_group_data["initialMu"][index],
                node_group_data["initialSD"][index],
                network.n_years,
                network.n_months,
                network.n_points,
                network.omega)

        self.set_reproduction(
            ratio_at_birth=node_group_data["RatioAtBirth"][index],
            sigma_j=node_group_data["sigmaJ"][index],
            recruit=recruitment.Logistic_recruitment(
                alpha=node.egg_alpha,
                beta=node.egg_beta,
                min_recruit=node.min_recruit,
                max_recruit=node.max_recruit),
            produce_eggs=node_group_data["produce_eggs"][index])
