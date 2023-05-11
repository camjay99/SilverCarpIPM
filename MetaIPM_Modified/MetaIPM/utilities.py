import pandas as pd
import numpy as np

def project_migration(transition_key_data, transition_data,
                      n_periods = 12):
    '''
    Takes transition data and projects what cumulative transition
    probabilities will be n_periods in the future assuming a
    Markov Model.
    
    Parameters:
    transition_key_data (DataFrame): The relationship between route names
                                     and start and end nodes
    transition_data (DataFrame):     The probability of an individual
                                     taking each route
    n_periods (int):                 Number of periods to project for

    Returns:
    new_keys:  The new relationship between route names and start/end nodes
    new_probs: The new probability of an individual taking each route after
               n_periods.
    '''
    transition_data_transposed = transition_data.transpose()
    transition_data_transposed.index.name = 'column'
    transition_data_transposed.reset_index(
            inplace=True)

    transition_data_use = pd.merge(
        transition_key_data,
        transition_data_transposed,
        on="column")
    
    # Set up reference for indices associated with names in transition matrix
    reference = list(set(transition_data_use['start'].unique()) | 
                     set(transition_data_use['end'].unique()))
    
    # Initialize the transition matrix
    transition = np.zeros((len(reference), len(reference)))
    
    # Add entries to transtion matrix:
    for index, row in transition_data_use.iterrows():
        start = reference.index(row['start'])
        end = reference.index(row['end'])
        transition[start, end] = row[0]
        
    # Fill in probabilities for not moving
    for row in range(len(transition)):
        transition[row, row] = 1 - transition[row].sum()
    
    n_transition = np.linalg.matrix_power(transition, n_periods)
        
    result = pd.DataFrame()
    for m in range(len(n_transition)):
        for n in range(len(n_transition)):
            if m == n:
                continue
            if n_transition[m, n] == 0:
                continue
            new_row = pd.Series(data={'start':reference[m], 'end':reference[n], 'prob':n_transition[m, n]})
            result = result.append(new_row, ignore_index=True)

    new_routes = [row['start'] + '-' + row['end'] for index, row in result.iterrows()]
    result = result.assign(routes=new_routes)

    new_keys = result[['routes', 'start', 'end']]
    new_probs = pd.DataFrame(data = [list(result['prob'])], columns = result['routes'])
    
    return new_keys, new_probs