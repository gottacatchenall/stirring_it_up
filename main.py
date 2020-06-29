#! /usr/bin/env python3

import figures
import stir

parameters = {
                'number_of_days': 200,

                # disease parameters
                    'infectivity': 0.01,
                    'recovery_time' :  14,
                    'transmissable_time' : 14,

                # social distancing
                    'social_distancing_strength': 0.5,
                    'social_distancing_days': 70,

                # network structure
                    'num_indivs': 400,
                    'edge_density': 0.1,            # makes sense between 0.01 and 0.1
                    'community_size': 20,
                    'community_modularity': 5.0,     #only makes sense between 1 and ~10
             }



result = stir.run_stir_model(parameters)

figures.plot_single_simulation(result)
#figures.plot_network(result)
