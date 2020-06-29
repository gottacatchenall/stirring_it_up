import numpy as np

def get_community_ids(num_indivs, community_size):
    num_communities = int(np.floor(num_indivs/community_size))
    community_ids = []
    for i in range(num_communities):
        community_ids += [i for x in range(community_size)]
    return community_ids

def initialize_sbm_probability_matrix(parameters):
    num_indivs = parameters['num_indivs']
    community_size = parameters['community_size']
    edge_density = parameters['edge_density']
    modularity = parameters["community_modularity"]
    num_communities = int(np.floor(num_indivs/community_size))

    probability_matrix = np.zeros((num_indivs, num_indivs))

    community_ids = get_community_ids(num_indivs, community_size)

    p_between_communities = (edge_density * num_indivs * num_communities) / (modularity * community_size**2)
    p_within_community = (edge_density * num_indivs * num_communities) / (community_size**2)

    print(p_between_communities)
    print(p_within_community)

    for i in range(num_indivs):
        for j in range(num_indivs):
            if (i == j):
                probability_matrix[i,j] = 0.0
            elif (community_ids[i] == community_ids[j]):
                probability_matrix[i,j] = min(1.0, p_within_community)
            else:
                probability_matrix[i,j] = p_between_communities

    return probability_matrix

def draw_from_sbm(probability_matrix):
    num_indivs= len(probability_matrix)
    adjacency_matrix = np.zeros((num_indivs, num_indivs))

    for i in range(num_indivs):
        for j in range(num_indivs):
            adjacency_matrix[i,j] = np.random.binomial(1, probability_matrix[i,j])
    return adjacency_matrix
