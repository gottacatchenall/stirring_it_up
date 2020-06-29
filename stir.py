import stochastic_block_model as sbm
import numpy as np

S = 1
T = 2
I = 3
R = 4

def update_individual(i, adjacency_matrix, state, old_state, connectivity, parameters):
    num_indivs = len(state)
    this_individuals_state = state[i]

    infectivity = parameters['infectivity']
    transmissable_time = parameters['transmissable_time']
    recovery_time = parameters['recovery_time']

    if (this_individuals_state == R):
        return state

    if (this_individuals_state == S):
        for j in range(num_indivs):
            if (adjacency_matrix[j,i] == 1):
                if (old_state[j] == T):
                    if (np.random.random() < connectivity):
                        if (np.random.random() <  infectivity):
                            if (old_state[i] == S):
                                state[i] = T
                            if (old_state[j] == S):
                                state[j] = T

    if (state[i] == T):
        if (np.random.exponential(transmissable_time) < 1):
            state[i] = I
        else:
            state[i] = T

    if (state[i] == I):
        if (np.random.exponential(recovery_time) < 1):
            state[i] = R
        else:
            state[i] = I

    return state


def run_stir_timestep(old_state, parameters, adjacency_matrix, connectivity):
    num_indivs = len(old_state)

    infectivity = parameters['infectivity']
    recovery_time = parameters['recovery_time']
    transmissable_time = parameters['transmissable_time']

    state = [old_state[x] for x in range(num_indivs)]

    for i in range(num_indivs):
        state = update_individual(i, adjacency_matrix, state, old_state, connectivity, parameters)

    return state

def count_bins(state):
    S_now = state.count(S)
    T_now = state.count(T)
    I_now = state.count(I)
    R_now = state.count(R)
    return((S_now, T_now, I_now, R_now))

def get_connectivity_timeseries(parameters):
    num_timesteps = parameters['number_of_days']
    distancing_str = parameters['social_distancing_strength']
    connectivity_timeseries = [1 for x in range(num_timesteps)]
    social_distancing_interval = (5, parameters['social_distancing_days'] + 5)

    for t in range(num_timesteps):
        if (social_distancing_interval[0] < t and t < social_distancing_interval[1]):
            connectivity_timeseries[t] = 1.0-distancing_str
    return connectivity_timeseries

def run_stir_model(parameters):
    num_timesteps = parameters['number_of_days']

    probability_matrix = sbm.initialize_sbm_probability_matrix(parameters)
    connectivity_over_time = get_connectivity_timeseries(parameters)

    S_timeseries = [0 for x in range(num_timesteps)]
    T_timeseries = [0 for x in range(num_timesteps)]
    I_timeseries = [0 for x in range(num_timesteps)]
    R_timeseries = [0 for x in range(num_timesteps)]


    initial_condition = [T,T] + [S for i in range(len(probability_matrix)-2)]
    np.random.shuffle(initial_condition)
    state = initial_condition

    adj_mat= sbm.draw_from_sbm(probability_matrix)
    for t in range(num_timesteps):
        print('Simulating day %d..... ' % t, end='\r')
        state = run_stir_timestep(state, parameters, adj_mat, connectivity_over_time[t])
        (S_now, T_now, I_now, R_now) = count_bins(state)      # get number of s, t, i, and r, and update timeseries
        S_timeseries[t] = S_now
        T_timeseries[t] = T_now
        I_timeseries[t] = I_now
        R_timeseries[t] = R_now

    num_indivs = parameters['num_indivs']
    S_proportion_timeseries = [S_timeseries[t]/num_indivs for t in range(num_timesteps)]
    T_proportion_timeseries = [T_timeseries[t]/num_indivs for t in range(num_timesteps)]
    I_proportion_timeseries = [I_timeseries[t]/num_indivs for t in range(num_timesteps) ]
    cumalative_infections_timeseries = [(T_timeseries[i] + I_timeseries[i] + R_timeseries[i])/num_indivs for i in range(num_timesteps)]

    results = { 'adjacency_matrix': adj_mat, 'S': S_proportion_timeseries, 'T': T_proportion_timeseries, 'I': I_proportion_timeseries, 'total': cumalative_infections_timeseries, 'social_distancing': connectivity_over_time}
    print('')
    print('')
    return(results)
