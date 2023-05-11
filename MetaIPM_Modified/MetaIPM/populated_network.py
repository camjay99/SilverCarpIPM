from MetaIPM import network, node


class populate_network_from_csv():
    """
    Create network from CSV files.

    The class also contains functions needed
    to run the stochastic version of the model.

    This includes re-setting conditions between stochastic runs.
    """
    def __init__(self,
                 network_data,
                 transition_data,
                 transition_key_data,
                 node_data,
                 group_data,
                 lw_data, vonB_data, vonB_sigma_data,
                 maturity_data,
                 stochastic_spawn=True,
                 stochastic_pars=True):

        # Save inputs for future use
        self.network_data = network_data
        self.transition_data = transition_data
        self.transition_key_data = transition_key_data
        self.lw_data = lw_data
        self.maturity_data = maturity_data
        self.vonB_data = vonB_data
        self.vonB_sigma_data = vonB_sigma_data
        self.group_data = group_data
        self.stochastic_spawn = stochastic_spawn
        self.stochastic_pars = stochastic_pars

        # Create network
        self.network = network.network_populated_paths(
            network_data["network_name"][0])
        self.network.add_network_parameters(
            network_data,
            stochastic_spawn=self.stochastic_spawn)

        # Create network's paths using transition data
        self.network.create_paths(
            stochastic_pars=self.stochastic_pars,
            transition_data=transition_data,
            transition_key_data=transition_key_data)

        # Create list of nodes for network
        start_nodes = transition_key_data['start'].unique()
        start_nodes.sort()
        stop_nodes = transition_key_data['end'].unique()
        stop_nodes.sort()

        if len(start_nodes) != len(stop_nodes):
            if (start_nodes != stop_nodes).all():
                print("Warning, not all nodes are connected",
                      "Check your transition files")

        # Fill nodes and groups
        nodes_in = []
        for node_name in start_nodes:
            if(node_name in node_data['Pool'].unique()):
                node_temp = node.node_populated(node_name)
                node_temp.add_node_parameters(node_data)
                node_temp.add_group_parameters(
                    self.group_data, self.network)
                node_temp.add_stochastic_parameters(
                    lw_data, maturity_data,
                    vonB_data, vonB_sigma_data,
                    self.network, self.stochastic_pars)
                nodes_in.append(node_temp)
            else:
                print("Warning " +
                      node_name +
                      " is not in the node_data. Node not created.")

        self.network.add_nodes(nodes_in)
        self.network.initialize_nodes_in_network()

    def new_stochastic_parameters(self):
        """
        Resets population and updates stochastic
        parameters in nodes for the groups.
        """

        self.network.clear_nodes()
        # update spawning probs
        if self.stochastic_spawn:
            """
            Only run if needed.
            Not running gives a very small improvement in model run time.
            """

            self.network.create_new_spawn_prob(
                self.network_data,
                stochastic_spawn=self.stochastic_spawn)

        if self.stochastic_pars:
            """
            Only run if needed.
            Not running gives a very small improvement in model run time.
            """
            self.network.clear_populated_paths()
            self.network.create_paths(
                stochastic_pars=self.stochastic_pars,
                transition_data=self.transition_data,
                transition_key_data=self.transition_key_data)

        for node_idx in self.network.nodes:
            node_idx.update_group_parameters(self.network)

    def show_network(self):
        return self.network
