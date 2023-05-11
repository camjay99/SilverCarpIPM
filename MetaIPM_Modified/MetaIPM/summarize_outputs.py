import pandas as pd
import numpy as np
import seaborn as sns

sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
pal = sns.cubehelix_palette(12, rot=-.25, light=.7)


def extract_all_populations(network_in):
    '''
    Extract out group-level data and summarize at network-level.
    '''
    data_out = pd.DataFrame()

    year_month = pd.DataFrame(
        {"Year": np.repeat(range(network_in.n_years + 1),
                           network_in.n_months),
         "Month": np.tile(range(network_in.n_months),
                          network_in.n_years + 1)}
    )

    for node in network_in.nodes:
        for group in node.groups:
            pop_raw = pd.DataFrame(group.population.transpose())
            pop_raw.columns = network_in.omega
            node_group = pd.DataFrame(
                {"Node": np.repeat(node.show_node_name(),
                                   (network_in.n_years + 1) *
                                   network_in.n_months),
                 "Group": np.repeat(group.show_group_name(),
                                    (network_in.n_years + 1) *
                                    network_in.n_months)}
            )
            pop_year_mo = pd.concat(
                [pop_raw, year_month, node_group],
                axis=1).melt(id_vars=['Year', 'Month', 'Node', 'Group'],
                             var_name="Length",
                             value_name="Population")
            data_out = data_out.append(pop_year_mo)
    return data_out
