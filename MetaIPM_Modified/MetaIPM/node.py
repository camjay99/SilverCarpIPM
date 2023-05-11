import numpy as np
from scipy.special import expit
import scipy.stats as stats
from MetaIPM import group


class logistic:
    """Defines a logistic function."""

    def __init__(self, inflection, slope, min, max):
        self.inflection = inflection
        self.slope = slope
        self.min = min
        self.max = max

    def __call__(self, z):
        out = (self.min + ((self.max - self.min) /
                           (1 + np.exp(- self.slope *
                                       (z - self.inflection)))))
        return out


class node:
    """Nodes contain groups and exist within the network"""
    def __init__(self, node_name):
        self.node_name = node_name
        self.groups = []

    def show_node_name(self):
        return self.node_name

    def add_groups(self, groups_in):
        [self.groups.append(n) for n in groups_in]

    def n_groups(self):
        return len(self.groups)


class node_populated(node):
    """
    Populated nodes contain groups with length distributions.

    This class also has function to set the group's parameters.
    """
    def add_node_parameters(self, node_data):
        pool_id = node_data['Pool'] == self.node_name
        self.Spawn = node_data[pool_id]['Spawn'].values[0]
        #self.S0 = node_data[pool_id]['S0'].values[0]
        #self.h = node_data[pool_id]['h'].values[0]
        #self.R0 = node_data[pool_id]['R0'].values[0]
        self.egg_alpha = node_data[pool_id]['egg_alpha'].values[0]
        self.egg_beta = node_data[pool_id]['egg_beta'].values[0]
        self.min_recruit = node_data[pool_id]['min_recruit'].values[0]
        self.max_recruit = node_data[pool_id]['max_recruit'].values[0]
        self.harvest_min = node_data[pool_id]['harvest_min'].values[0]
        self.harvest_max = node_data[pool_id]['harvest_max'].values[0]
        self.harvest_slope = node_data[pool_id]['harvest_slope'].values[0]
        inflection_use = node_data[pool_id]['harvest_inflection'].values[0]
        self.harvest_inflection = inflection_use
        self.harvest_start = node_data[pool_id]['harvest_start'].values[0]
        self.harvest_end = node_data[pool_id]['harvest_end'].values[0]
        month_use = list(map(int, node_data[pool_id]['harvest_month'].values[0].split(";")))
        self.harvest_months = month_use

        self.harvest_level = logistic(
            inflection=self.harvest_inflection,
            slope=self.harvest_slope,
            min=self.harvest_min,
            max=self.harvest_max)

    def set_maturity_parameters(self):
        # Add or update maturity parameters
        mat_columns = self.maturity_data.columns
        par_columns_use = ["V" in mat for mat in mat_columns]
        par_columns = mat_columns[par_columns_use]

        if self.stochastic_pars:
            mat_column_name = np.random.choice(par_columns)
            mat_prob = self.maturity_data[mat_column_name]
        else:
            mat_prob = self.maturity_data[par_columns].mean(1)
        self.maturity_data['prob'] = mat_prob

        mat_data_use = self.maturity_data[['parameter', 'prob']]

        mat_alpha_rows = mat_data_use['parameter'] == 'alpha'
        self.mat_alpha = mat_data_use[mat_alpha_rows]['prob'].values[0]

        mat_beta_rows = mat_data_use['parameter'] == 'beta'
        self.mat_beta = mat_data_use[mat_beta_rows]['prob'].values[0]

    def set_vonB_parameters(self, network):
        # Add vonB parameter sigma
        self.vonB_sigma_k = self.vonB_sigma_data['sd'].values[0]

        vonB_columns = self.vonB_data.columns
        vonB_par_columns_use = ["V" in vonB for vonB in vonB_columns]
        vonB_par_columns = vonB_columns[vonB_par_columns_use]

        if self.stochastic_pars:
            vonB_column_name = np.random.choice(vonB_par_columns)
            self.vonB_data['pars'] = self.vonB_data[vonB_column_name]
        else:
            self.vonB_data['pars'] = self.vonB_data[vonB_columns].mean(1)

        vonB_data_use = self.vonB_data[['parameter', 'pars']]

        vb_k_rows = vonB_data_use['parameter'] == 'K'
        self.vonB_K = (vonB_data_use[vb_k_rows]['pars'].values[0] /
                       network.n_months)

        vb_linf_rows = vonB_data_use['parameter'] == 'Linf'
        self.vonB_Linf = vonB_data_use[vb_linf_rows]['pars'].values[0]

        vb_m_rows = vonB_data_use['parameter'] == 'max'
        self.surv_max = (vonB_data_use[vb_m_rows]['pars'].values[0] /
                       network.n_months)
        
        vb_m_rows = vonB_data_use['parameter'] == 'alpha'
        self.surv_alpha = (vonB_data_use[vb_m_rows]['pars'].values[0] /
                       network.n_months)
        
        vb_m_rows = vonB_data_use['parameter'] == 'beta'
        self.surv_beta = (vonB_data_use[vb_m_rows]['pars'].values[0] /
                       network.n_months)
        
        vb_m_rows = vonB_data_use['parameter'] == 'min'
        self.surv_min = (vonB_data_use[vb_m_rows]['pars'].values[0] /
                       network.n_months)
        
        vb_m_rows = vonB_data_use['parameter'] == 'g_migration'
        self.g_migration = (vonB_data_use[vb_m_rows]['pars'].values[0] /
                       network.n_months)
        
        vb_m_rows = vonB_data_use['parameter'] == 'g_length'
        self.g_length = (vonB_data_use[vb_m_rows]['pars'].values[0] /
                       network.n_months)
        

    def set_lw_parameters(self):
        lw_columns = self.lw_data.columns
        lw_par_columns_use = ["V" in lw for lw in lw_columns]
        lw_par_columns = lw_columns[lw_par_columns_use]

        if self.stochastic_pars:
            lw_column_name = np.random.choice(lw_par_columns)
            self.lw_data['prob'] = self.lw_data[lw_column_name]
        else:
            self.lw_data['prob'] = self.lw_data[lw_par_columns].mean(1)

        lw_data_use = self.lw_data[['parameter', 'prob']]

        beta_1_condition = lw_data_use['parameter'] == 'beta_1'
        self.lw_beta1 = lw_data_use[beta_1_condition]['prob'].values[0]

        beta_2_condition = lw_data_use['parameter'] == 'beta_2'
        self.lw_beta2 = lw_data_use[beta_2_condition]['prob'].values[0]

    def add_stochastic_parameters(self, lw_data, maturity_data,
                                  vonB_data, vonB_sigma_data,
                                  network, stochastic_pars):
        '''
        add stochastic parameters and choose values for simulation
        '''
        self.stochastic_pars = stochastic_pars
        self.maturity_data = maturity_data

        if(vonB_data['site'].isin([self.show_node_name()]).any()):
            vb_condition = vonB_data['site'] == self.show_node_name()
            vb_dat = vonB_data[vb_condition].copy()
        else:
            vb_dat = vonB_data[vonB_data['site'] == 'hyper'].copy()
        self.vonB_data = vb_dat

        if(vonB_sigma_data['site'].isin([self.show_node_name()]).any()):
            site_condition = vonB_sigma_data['site'] == self.show_node_name()
            vb_in = vonB_sigma_data[site_condition].copy()
        else:
            vb_in = vonB_sigma_data[vonB_sigma_data['site'] == 'hyper'].copy()
        self.vonB_sigma_data = vb_in

        if (lw_data['site'].isin([self.show_node_name()]).any()):
            lw_in = lw_data[lw_data['site'] == self.show_node_name()].copy()
        else:
            lw_in = lw_data[lw_data['site'] == 'hyper'].copy()
        self.lw_data = lw_in

        self.set_maturity_parameters()
        self.set_vonB_parameters(network)
        self.set_lw_parameters()

    def add_group_parameters(self, group_data, network):
        if (self.node_name in group_data['Node'].unique()):
            node_grp_data = group_data[group_data["Node"] == self.node_name]
            for index, row in node_grp_data.iterrows():
                group_temp = \
                    group.group_populated(node_grp_data["Group"][index])
                group_temp.add_group_parameters(node=self,
                                                index=index,
                                                node_group_data=node_grp_data,
                                                network=network)
                self.add_groups([group_temp])

        else:
            print("Warning: " +
                  self.node_name +
                  " is not in the group_data. Group data not added.")

    def update_group_parameters(self, network):
        self.set_maturity_parameters()
        self.set_vonB_parameters(network)
        self.set_lw_parameters()

    def calculate_node_population(self, year):
        pop_temp = 0.0
        for grp in self.groups:
            pop_temp += grp.show_group_pop_total(year)

        return pop_temp
    
    def calculate_node_biomass(self, year, omega):
        biomass_temp = 0.0
        weights = self.length_weight(omega)
        for grp in self.groups:
            biomass_temp += (grp.show_group_pop_dist(year) * weights).sum()
        return biomass_temp

    def raw_node_population(self):
        pop_temp = 0.0
        for grp in self.groups:
            pop_temp += grp.population

        return pop_temp

    def clear_nonstart_group(self):
        ''' Reset initial conditions and zero out later years.'''
        for grps in self.groups:
            # Reset the initial population size
            grps.population[:, 1:] = np.transpose(
                np.tile(grps.population[:, 0],
                        (grps.population[:, 1:].shape[1], 1)))
            # Reset the non-initial population size to zeros
            grps.population[:, 1:] = np.zeros(grps.population[:, 1:].shape)

    def length_weight(self, length_in):
        '''
        Takes in length in m and returns weight in kg
        '''
        length_log10 = np.log10(length_in)
        weight_log10 = self.lw_beta1 + self.lw_beta2 * length_log10
        return 10.0 ** weight_log10

    def maturity_prob(self, length_in):
        return expit(self.mat_alpha + self.mat_beta * length_in)

    def growth(self, length_now, length_next, year, omega):
        z = np.atleast_1d(length_now)
        z_prime = np.atleast_1d(length_next)
        biomass = self.calculate_node_biomass(year, omega)
        
        project = np.zeros((len(z), len(z_prime)))
        for index in range(0, len(z)):
            location_parameter = (self.vonB_K * z[index] + \
                (1 - self.vonB_K) * (self.vonB_Linf)) * \
                np.exp(-1*self.g_length*biomass) # - self.g_length*biomass)
            prob_raw = stats.norm.pdf(x=z_prime,
                                      loc=location_parameter,
                                      scale=self.vonB_sigma_k)
            if prob_raw.sum() == 0:
                project[:, index] = 0
            else:
                project[:, index] = prob_raw / prob_raw.sum()
        return project
    
    def survival(self, length_in):
        return self.surv_min + (self.surv_max - self.surv_min) / \
            (1 + np.exp(self.surv_beta*(np.log(length_in) - np.log(self.surv_alpha))))

    def initialize_node(self, network, year=0):
        self.projection_matrix = self.growth(network.omega, network.omega, year, network.omega)

    def vonB_function(self, age_in):
        return self.vonB_Linf * (1.0 - np.exp(- self.vonB_K * age_in))

    def project_node(self,
                     current_year,
                     current_month,
                     network):

        current_time_index = current_year * network.n_months + current_month
        self.initialize_node(network, current_time_index)
            
        # Is it a node and spawning month?
        if self.Spawn and current_month in network.spawn_months:
            # Add new age_0 fish to next year
            for grp in self.groups:
                grp.age_0[current_year + 1] += (
                    grp.group_spawn(year=current_time_index,
                                    length_weight=self.length_weight,
                                    maturity_prob=self.maturity_prob,
                                    omega=network.omega) *
                    network.spawn_prob[current_year] *
                    network.egg_viability
                )

        # If it is the first month of the year, age_0 fish enter the population
        add_in_month = 0
        if current_month == add_in_month:
            new_at_node = 0.0
            # Add up new individuals in node
            for grp in self.groups:
                new_at_node += grp.age_0[current_year]
                grp.age_0[current_year] = 0.0
            for grp in self.groups:
                age_0_mean = self.vonB_function(1.0 / network.n_months)
                age_0_dist_raw = stats.lognorm.pdf(network.omega,
                                                   loc=0.0,
                                                   scale=age_0_mean,
                                                   s=grp.sigma_j)
                if age_0_dist_raw.sum() > 0.0:
                    age_0_dist = age_0_dist_raw/age_0_dist_raw.sum()
                else:
                    age_0_dist = np.zeros(len(age_0_dist_raw))

                grp.population[:, current_time_index] += (
                    new_at_node * grp.ratio_at_birth * age_0_dist
                    )

        # Harvest code
        if (current_year >= self.harvest_start and
                current_year <= self.harvest_end and
                current_month in self.harvest_months):
            harvest_level = self.harvest_level(network.omega)
        else:
            harvest_level = 0.0
        
        survival_level = self.survival(network.omega)
        
        # project growth
        for grp in self.groups:
            grp.population[:, current_time_index + 1] = np.dot(
                self.projection_matrix,
                grp.population[:, current_time_index]
            ) * survival_level * (1.0 - harvest_level)
