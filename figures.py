import matplotlib.pyplot as plt
#from webweb import Web

def plot_single_simulation(results):
    fig, (ax1, ax2, ax3) = plt.subplots(1,3)

    I = results['I']
    T = results['T']
    social_distancing = results['social_distancing']
    total_infections = results['total']
    t = range(len(I))

    ax1.plot(t, I, 'b')
    ax1.plot(t, T, 'r--')
    ax1.set_title('New Infections over time')
    ax1.legend(['infected', 'transmisable but not symptomatic'])
    ax1.set_ylabel('per capita infections')
    ax1.set_xlabel('day')

    ax2.plot(t, total_infections, 'g')
    ax2.set_title('cumalative infections per capita')
    ax2.set_xlabel('day')
    ax2.set_ylabel('total infections')

    ax3.plot(t,social_distancing, 'r')
    ax3.set_xlabel('day')
    ax3.set_ylabel('social connectivity')
    ax3.set_title('social distancing over time')

    plt.show()


def plot_network(results):
    adjacency_matrix = results['adjacency_matrix']
    web = Web(adjacency_matrix, adjacency_type='matrix')
    web.show()
