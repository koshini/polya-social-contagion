import networkx as nx
from graph_generator import generate_graph
from simulation import simulate
import time
import matplotlib.pyplot as plt
import numpy as np

runs = 100
node_count = 100
iterations = 300
initial_balls = node_count * 100
topology = 'barabasi'

def main():
    folder = 'neutral-equal/'
    red_mult = 1
    black_mult = 1
    red_budget = node_count * 10
    black_budget = node_count * 10
    run_scenario(folder, red_mult, black_mult, red_budget, black_budget)

    folder = 'neutral-more-red/'
    red_mult = 1
    black_mult = 1
    red_budget = node_count * 10
    black_budget = node_count * 7
    run_scenario(folder, red_mult, black_mult, red_budget, black_budget)

    folder = 'pre-infected-equal/'
    red_mult = 2
    black_mult = 1
    red_budget = node_count * 10
    black_budget = node_count * 10
    run_scenario(folder, red_mult, black_mult, red_budget, black_budget)

    folder = 'pre-cured-equal/'
    red_mult = 1
    black_mult = 2
    red_budget = node_count * 10
    black_budget = node_count * 10
    run_scenario(folder, red_mult, black_mult, red_budget, black_budget)

    folder = 'pre-cured-more-red/'
    red_mult = 1
    black_mult = 2
    red_budget = node_count * 10
    black_budget = node_count * 7
    run_scenario(folder, red_mult, black_mult, red_budget, black_budget)




def run_scenario(folder, red_mult, black_mult, red_budget, black_budget):
    initial_condition = {
        'node_count': node_count,
        'parameter': 2,
        'red': initial_balls * red_mult,
        'black': initial_balls * black_mult,
        'dist': 'random'
    }

    print('-------------' + folder)
    strat_dict_list = []

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': 0,
        'portion': 0.01
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': 0,
        'portion': 0.05
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': 0,
        'portion': 0.1
    })

    # run_strats(folder, topology, red_mult, black_mult, strat_dict_list, iterations, runs, initial_condition)
    make_plots(folder, topology, strat_dict_list, '0vary-portion')



    ###############################
    strat_dict_list = []

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': 0.2,
        'portion': 0.01
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': 0.2,
        'portion': 0.05
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': 0.2,
        'portion': 0.1
    })

    # run_strats(folder, topology, red_mult, black_mult, strat_dict_list, iterations, runs, initial_condition)
    make_plots(folder, topology, strat_dict_list, '0.2vary-portion')

    ###############################

    ###############################
    strat_dict_list = []

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': 0.4,
        'portion': 0.01
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': 0.4,
        'portion': 0.05
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': 0.4,
        'portion': 0.1
    })

    # run_strats(folder, topology, red_mult, black_mult, strat_dict_list, iterations, runs, initial_condition)
    make_plots(folder, topology, strat_dict_list, '0.4vary-portion')

    ###############################

    strat_dict_list = []

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': 0.6,
        'portion': 0.01
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': 0.6,
        'portion': 0.05
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': 0.6,
        'portion': 0.1
    })

    # run_strats(folder, topology, red_mult, black_mult, strat_dict_list, iterations, runs, initial_condition)
    # make_plots(folder, topology, strat_dict_list, '0.6vary-portion')

    ###############################
    strat_dict_list = []

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'pure_centrality',
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'pure_degree',
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'pure_closeness',
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'pure_exposure',
    })

    # run_strats(folder, topology, red_mult, black_mult, strat_dict_list, iterations, runs, initial_condition)

    #### Plot exposure-degree-closeness
    strat_dict_list = []

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'pure_exposure',
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'pure_degree',
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'pure_closeness',
    })
    # make_plots(folder, topology, strat_dict_list, 'exposure-degree-closeness')

    #### Plot centrality-degree-closeness
    strat_dict_list = []

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'pure_centrality',
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'pure_degree',
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'pure_closeness',
    })
    # make_plots(folder, topology, strat_dict_list, 'centrality-degree-closeness')


    ############################### gradient nash equilibrium
    strat_dict_list = []

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'uniform',
        'black_strat': 'gradient',
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'gradient',
        'black_strat': 'gradient',
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'gradient',
        'black_strat': 'uniform',
    })
    #
    # run_strats(folder, topology, red_mult, black_mult, strat_dict_list, iterations, runs, initial_condition)
    # make_plots(folder, topology, strat_dict_list, 'gradient-nash-equil')


def run_strats(folder, topology, red_mult, black_mult, strat_list, iterations, runs, initial_condition):
    for strat in strat_list:
        print(str(strat))
        start = time.time()
        prefix = ''
        if strat.get('threshold') is not None:
            prefix = str(strat['threshold']) + '_' + str(strat['portion'])
        infection_csv = folder + topology + prefix + strat['red_strat'] + strat[
                'black_strat'] + 'infection.csv'
        simulate(folder, topology, red_mult, black_mult, strat, iterations, runs, prefix=prefix, initial_condition=initial_condition)
        elapsed_time = time.time() - start
        print(elapsed_time)
        print()

        log_file = folder + 'log.txt'
        with open(log_file, 'a') as f:
            f.write(str(strat) + '\n')
            f.write(str(elapsed_time) + '\n')
            f.write('\n')

def make_plots(folder, topology, strat_dict_list, plot_name):
    plt.figure()
    for strat_dict in strat_dict_list:
        if topology == 'twitter':
            iterations = 60
        else:
            iterations = 300
        prefix = ''
        red_strat = strat_dict['red_strat'].replace('_', ' ')
        black_strat = strat_dict['black_strat'].replace('_', ' ')
        infection_csv = folder + '/empirical-infection' + topology + strat_dict['red_strat'] + strat_dict[
            'black_strat'] + 'infection.csv'
        if strat_dict.get('threshold') is not None:
            prefix = str(strat_dict['threshold']) + '_' + str(strat_dict['portion'])
        if prefix:
            infection_csv = folder + topology + prefix + strat_dict['red_strat'] + strat_dict[
                'black_strat'] + 'infection.csv'

        infection_array = np.loadtxt(infection_csv, delimiter=',', unpack=True)
        # infection_array = np.insert(infection_array, 0, 0.2, axis=1)
        avg_infection = np.mean(infection_array, axis=1)
        plt.xlabel('Time step')
        plt.ylabel('Average infection rate')
        # avg_infection = infection_array # if there is only one row
        plt.plot(list(range(avg_infection.size)), avg_infection, label=prefix + black_strat)

    plt.legend(loc='best', prop={'size': 10})
    plt.axis([0, iterations, 0.2, 0.8])
    filename = folder + topology + plot_name + '.png'
    plt.savefig(filename)
    # plt.show()
    plt.close()



if __name__ == "__main__":
    main()