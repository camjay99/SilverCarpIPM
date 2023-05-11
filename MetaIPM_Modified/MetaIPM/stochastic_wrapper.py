import pandas as pd
import numpy as np
from MetaIPM import summarize_outputs as so


class stochastic_model():
    """
    A wrapper class around populated networks.
    """
    def __init__(self, network_creator):
        self.network_creator = network_creator
        self.population = pd.DataFrame()
        self.counting_index_base = 0

    def run_stochastic(self, n_iter):
        for i in range(n_iter):
            print("Running stochastic iteration ",
                  str(self.counting_index_base))
            # Draw new stochastic parameters
            self.network_creator.new_stochastic_parameters()

            # Project model, extract outputs
            self.network_creator.network.project_network()

            out = so.extract_all_populations(self.network_creator.network)
            index_df = pd.DataFrame(
                {'stoch_index': np.repeat(self.counting_index_base,
                                          out.shape[0])}
            )
            out_with_index = pd.concat(
                [index_df.reset_index(drop=True),
                 out.reset_index(drop=True)], axis=1, sort=False)

            # Save population and update look index
            self.population = self.population.append(out_with_index)
            self.counting_index_base += 1

    def return_population(self):
        return self.population
