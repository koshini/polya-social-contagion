import networkx as nx
from graph_generator import get_graph, generate_graph
from simulation import simulate
import time


def main():
    topologies = ['facebook', 'meetup']
    iterations = 300
    runs = 50

##################################################################################################
    # folder = 'neutral-equal/'
    # red_mult = 1
    # black_mult = 1
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
    #         'black_strat': 'centrality_threshold',
    #         'threshold': 0.4,
    #         'portion': 0.05
    #     })
    #
    #     run_strats(folder, topology, red_mult, black_mult, strat_dict_list, iterations, runs)

##################################################################################################
#     folder = 'neutral-more-red/'
#     red_mult = 1
#     black_mult = 1
#
#     print('-------------' + folder)
#     for topology in topologies:
#         print(topology)
#         if topology == 'twitter':
#             iterations = 100
#         else:
#             iterations = 300
#
#         G = generate_graph(folder, topology, red_mult, black_mult)
#         node_count = nx.number_of_nodes(G)
#         red_budget = node_count * 10
#         black_budget = node_count * 7
#         strat_dict_list = []
#
#         strat_dict_list.append({
#             'red_budget': red_budget,
#             'black_budget': black_budget,
#             'red_strat': 'bot',
#             'black_strat': 'centrality_threshold',
#             'threshold': 0.4,
#             'portion': 0.05
#         })
#
#         run_strats(folder, topology, red_mult, black_mult, strat_dict_list, iterations, runs)
#
# ##################################################################################################
#     folder = 'pre-infected-equal/'
#     red_mult = 2
#     black_mult = 1
#
#     print('-------------' + folder)
#     for topology in topologies:
#         print(topology)
#         if topology == 'twitter':
#             iterations = 100
#         else:
#             iterations = 300
#
#         G = generate_graph(folder, topology, red_mult, black_mult)
#         node_count = nx.number_of_nodes(G)
#         red_budget = node_count * 10
#         black_budget = node_count * 10
#         strat_dict_list = []
#
#         strat_dict_list.append({
#             'red_budget': red_budget,
#             'black_budget': black_budget,
#             'red_strat': 'bot',
#             'black_strat': 'centrality_threshold',
#             'threshold': 0.4,
#             'portion': 0.05
#         })
#
#         run_strats(folder, topology, red_mult, black_mult, strat_dict_list, iterations, runs)

##################################################################################################
    folder = 'pre-cured-more-red/'
    red_mult = 1
    black_mult = 2

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
            'black_strat': 'centrality_threshold',
            'threshold': 0.4,
            'portion': 0.05
        })

        run_strats(folder, topology, red_mult, black_mult, strat_dict_list, iterations, runs)

##################################################################################################
    folder = 'pre-cured-equal/'
    red_mult = 1
    black_mult = 2

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
            'threshold': 0.4,
            'portion': 0.05
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

        run_strats(folder, topology, red_mult, black_mult, strat_dict_list, iterations, runs)


def run_strats(folder, topology, red_mult, black_mult, strat_list, iterations, runs):
    for strat in strat_list:
        print(str(strat))
        start = time.time()
        simulate(folder, topology, red_mult, black_mult, strat, iterations, runs)
        elapsed_time = time.time() - start
        print(elapsed_time)
        print()

        log_file = folder + 'log.txt'
        with open(log_file, 'a') as f:
            f.write(str(strat) + '\n')
            f.write(str(elapsed_time) + '\n')
            f.write('\n')




if __name__ == "__main__":
    main()