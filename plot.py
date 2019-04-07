import networkx as nx
from graph_generator import generate_graph
from simulation import simulate
import time
import matplotlib.pyplot as plt
import numpy as np


def main():
    runs = 50

    ##################################################################################################
    folder = 'neutral-equal/'
    red_mult = 1
    black_mult = 1
    topologies = ['twitter']

    print('-------------' + folder)
    for topology in topologies:
        print(topology)
        if topology == 'twitter':
            iterations = 100
        else:
            iterations = 300

        G = generate_graph(folder, topology, red_mult, black_mult)
        node_count = nx.number_of_nodes(G)
        red_budget = node_count * 10
        black_budget = node_count * 10
        strat_dict_list = []

        strat_dict_list.append({
            'red_budget': red_budget,
            'black_budget': black_budget,
            'red_strat': 'bot',
            'black_strat': 'uniform',
        })

        strat_dict_list.append({
            'red_budget': red_budget,
            'black_budget': black_budget,
            'red_strat': 'bot',
            'black_strat': 'pure_centrality_threshold',
        })

        strat_dict_list.append({
            'red_budget': red_budget,
            'black_budget': black_budget,
            'red_strat': 'bot',
            'black_strat': 'centrality_threshold',
            'threshold': 0,
            'portion': 0.02
        })

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
            'black_strat': 'follow_bot',
        })

        # run_strats(folder, topology, red_mult, black_mult, strat_dict_list, iterations, runs)
        make_plots(folder, topology, strat_dict_list, 'infection')

#################################################################################################
    folder = 'neutral-more-red/'
    red_mult = 1
    black_mult = 1
    topologies = ['twitter']


    print('-------------' + folder)
    for topology in topologies:
        print(topology)
        if topology == 'twitter':
            iterations = 100
        else:
            iterations = 300

        G = generate_graph(folder, topology, red_mult, black_mult)
        node_count = nx.number_of_nodes(G)
        red_budget = node_count * 10
        black_budget = node_count * 7
        strat_dict_list = []

        strat_dict_list.append({
            'red_budget': red_budget,
            'black_budget': black_budget,
            'red_strat': 'bot',
            'black_strat': 'uniform',
        })

        strat_dict_list.append({
            'red_budget': red_budget,
            'black_budget': black_budget,
            'red_strat': 'bot',
            'black_strat': 'pure_centrality_threshold',
        })

        strat_dict_list.append({
            'red_budget': red_budget,
            'black_budget': black_budget,
            'red_strat': 'bot',
            'black_strat': 'centrality_threshold',
            'threshold': 0,
            'portion': 0.02
        })

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
            'black_strat': 'follow_bot',
        })
        # run_strats(folder, topology, red_mult, black_mult, strat_dict_list, iterations, runs)
        # make_plots(folder, topology, strat_dict_list, 'infection')

##################################################################################################
    folder = 'pre-infected-equal/'
    red_mult = 2
    black_mult = 1

    print('-------------' + folder)
    for topology in topologies:
        print(topology)
        if topology == 'twitter':
            iterations = 100
        else:
            iterations = 300

        G = generate_graph(folder, topology, red_mult, black_mult)
        node_count = nx.number_of_nodes(G)
        red_budget = node_count * 10
        black_budget = node_count * 10
        strat_dict_list = []

        strat_dict_list.append({
            'red_budget': red_budget,
            'black_budget': black_budget,
            'red_strat': 'bot',
            'black_strat': 'uniform',
        })

        strat_dict_list.append({
            'red_budget': red_budget,
            'black_budget': black_budget,
            'red_strat': 'bot',
            'black_strat': 'pure_centrality_threshold',
        })

        strat_dict_list.append({
            'red_budget': red_budget,
            'black_budget': black_budget,
            'red_strat': 'bot',
            'black_strat': 'centrality_threshold',
            'threshold': 0,
            'portion': 0.02
        })

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
            'black_strat': 'follow_bot',
        })

        # run_strats(folder, topology, red_mult, black_mult, strat_dict_list, iterations, runs)
        # make_plots(folder, topology, strat_dict_list, 'infection')
        print()

##################################################################################################
    folder = 'pre-cured-more-red/'
    red_mult = 1
    black_mult = 2
    # topologies = ['facebook', 'meetup', 'twitter']
    topologies = ['twitter']

    print('-------------' + folder)
    for topology in topologies:
        print(topology)
        if topology == 'twitter':
            iterations = 100
        else:
            iterations = 300

        G = generate_graph(folder, topology, red_mult, black_mult)
        node_count = nx.number_of_nodes(G)
        red_budget = node_count * 10
        black_budget = node_count * 7
        strat_dict_list = []

        strat_dict_list.append({
            'red_budget': red_budget,
            'black_budget': black_budget,
            'red_strat': 'bot',
            'black_strat': 'uniform',
        })

        strat_dict_list.append({
            'red_budget': red_budget,
            'black_budget': black_budget,
            'red_strat': 'bot',
            'black_strat': 'pure_centrality_threshold',
        })

        strat_dict_list.append({
            'red_budget': red_budget,
            'black_budget': black_budget,
            'red_strat': 'bot',
            'black_strat': 'centrality_threshold',
            'threshold': 0.2,
            'portion': 0.02
        })

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
            'black_strat': 'follow_bot',
        })

        # run_strats(folder, topology, red_mult, black_mult, strat_dict_list, iterations, runs)
        # make_plots(folder, topology, strat_dict_list, 'infection')
        print()


##################################################################################################
    # folder = 'pre-cured-equal/'
    # red_mult = 1
    # black_mult = 2
    #
    # print('-------------' + folder)
    # for topology in topologies:
    #     print(topology)
    #     if topology == 'twitter':
    #         iterations = 100
    #     else:
    #         iterations = 300
    #
    #     G = generate_graph(folder, topology, red_mult, black_mult)
    #     node_count = nx.number_of_nodes(G)
    #     red_budget = node_count * 10
    #     black_budget = node_count * 10
    #     strat_dict_list = []
    #
    #     strat_dict_list.append({
    #         'red_budget': red_budget,
    #         'black_budget': black_budget,
    #         'red_strat': 'bot',
    #         'black_strat': 'uniform',
    #     })
    #
    #     strat_dict_list.append({
    #         'red_budget': red_budget,
    #         'black_budget': black_budget,
    #         'red_strat': 'bot',
    #         'black_strat': 'pure_centrality_threshold',
    #     })
    #
    #     strat_dict_list.append({
    #         'red_budget': red_budget,
    #         'black_budget': black_budget,
    #         'red_strat': 'bot',
    #         'black_strat': 'centrality_threshold',
    #         'threshold': 0.4,
    #         'portion': 0.05
    #     })
    #
    #     strat_dict_list.append({
    #         'red_budget': red_budget,
    #         'black_budget': black_budget,
    #         'red_strat': 'bot',
    #         'black_strat': 'pure_centrality',
    #     })
    #
    #     strat_dict_list.append({
    #         'red_budget': red_budget,
    #         'black_budget': black_budget,
    #         'red_strat': 'bot',
    #         'black_strat': 'follow_bot',
    #     })
    #
    #     run_strats(folder, topology, red_mult, black_mult, strat_dict_list, iterations, runs)


def run_strats(folder, topology, red_mult, black_mult, strat_list, iterations, runs):
    for strat in strat_list:
        print(str(strat))
        start = time.time()
        # prefix = str(strat['threshold']) + '_' + str(strat['portion'])
        prefix = ''
        if strat.get('threshold') is not None:
            prefix = str(strat['threshold']) + '_' + str(strat['portion'])
        if prefix:
            infection_csv = folder + topology + prefix + strat['red_strat'] + strat[
                'black_strat'] + 'infection.csv'
        simulate(folder, topology, red_mult, black_mult, strat, iterations, runs, prefix=prefix)
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
        if black_strat == 'centrality threshold':
            black_strat = 'centrality exposure threshold'
        if black_strat == 'pure centrality threshold':
            black_strat = 'pure centrality exposure threshold'
        infection_csv = folder + 'empirical-infection' + topology + strat_dict['red_strat'] + strat_dict[
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
        plt.plot(list(range(avg_infection.size)), avg_infection, label=black_strat)

    # plt.legend(loc='best', prop={'size': 10})
    plt.axis([0, iterations, 0, 1])
    filename = folder + topology + plot_name + '.png'
    plt.savefig(filename)
    # plt.show()
    plt.close()




if __name__ == "__main__":
    main()