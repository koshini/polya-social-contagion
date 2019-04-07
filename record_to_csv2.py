import networkx as nx
from graph_generator import get_graph
from simulation import simulate
import time


def main():
    # folder = 'pre-infected-more-red/'
    print('----------------barabasi')
    topology = 'barabasi'
    folder = topology

    # node_count = nx.number_of_nodes(G)
    node_count = 100
    red_budget = node_count * 10
    black_budget = node_count * 10

    initial_condition = {
        'node_count': node_count,
        'red': node_count * 100,
        'black': node_count * 100,
        'parameter': 2,
        'dist': 'random'
    }

    strat_dict_list = []

    iterations = 300
    runs = 200

    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'pure_centrality',
    # })
    #
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'pure_degree',
    # })
    #
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'pure_closeness',
    # })
    #
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'pure_exposure',
    # })

    # threshold = 0.4
    # portion = 0
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'centrality_threshold',
    #     'threshold': threshold,
    #     'portion': portion
    # })

    threshold = 0.4
    portion = 0
    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': threshold,
        'portion': portion
    })


    threshold = 0.4
    portion = 0.01
    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': threshold,
        'portion': portion
    })


    threshold = 0.4
    portion = 0.02
    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': threshold,
        'portion': portion
    })


    threshold = 0.4
    portion = 0.05
    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': threshold,
        'portion': portion
    })

    threshold = 0.4
    portion = 0.1
    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': threshold,
        'portion': portion
    })


    threshold = 0.4
    portion = 0.5
    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_threshold',
        'threshold': threshold,
        'portion': portion
    })

    for strat in strat_dict_list:
        print(str(strat))
        start = time.time()
        if strat.get('threshold'):
            prefix = str(strat['threshold']) + '_' + str(strat['portion'])
        else:
            prefix = ''
        simulate(folder, topology, strat, iterations, runs, initial_condition=initial_condition, prefix=prefix)
        elapsed_time = time.time() - start
        print(elapsed_time)
        print()

        log_file = folder + 'log.txt'
        with open(log_file, 'a') as f:
            f.write(str(strat) + '\n')
            f.write(str(elapsed_time) + '\n')
            f.write('\n')

################################################################################################
    # print('----------------facebook')
    # topology = 'facebook'
    # folder = topology
    # G = get_graph(topology)
    #
    # iterations = 500
    # runs = 50
    #
    # node_count = nx.number_of_nodes(G)
    # red_budget = node_count * 10
    # black_budget = node_count * 10
    # strat_dict_list = []

    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'pure_centrality_entropy',
    # })
    #
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'centrality_entropy',
    # })
    #
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'pure_centrality',
    # })
    #
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'uniform',
    # })
    #
    #
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'follow_bot',
    # })

    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'pure_closeness',
    # })
    #
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'pure_degree',
    # })
    #
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'pure_exposure',
    # })
    #
    # for strat in strat_dict_list:
    #     print(str(strat))
    #     start = time.time()
    #     simulate(folder, topology,strat, iterations, runs)
    #     elapsed_time = time.time() - start
    #     print(elapsed_time)
    #     print()
    #
    #     log_file = folder + 'log.txt'
    #     with open(log_file, 'a') as f:
    #         f.write(str(strat) + '\n')
    #         f.write(str(elapsed_time) + '\n')
    #         f.write('\n')

############################################################################################
    # print('----------------meetup')
    # topology = 'meetup'
    # folder = topology
    # G = get_graph(topology)
    #
    # iterations = 500
    # runs = 50
    #
    # node_count = nx.number_of_nodes(G)
    # red_budget = node_count * 10
    # black_budget = node_count * 10
    # strat_dict_list = []

    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'pure_centrality_entropy',
    # })
    #
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'centrality_entropy',
    # })
    #
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'pure_centrality',
    # })
    #
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'uniform',
    # })
    #
    #
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'follow_bot',
    # })

    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'pure_closeness',
    # })
    #
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'pure_degree',
    # })
    #
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'pure_exposure',
    # })
    #
    # for strat in strat_dict_list:
    #     print(str(strat))
    #     start = time.time()
    #     simulate(folder, topology,strat, iterations, runs)
    #     elapsed_time = time.time() - start
    #     print(elapsed_time)
    #     print()
    #
    #     log_file = folder + 'log.txt'
    #     with open(log_file, 'a') as f:
    #         f.write(str(strat) + '\n')
    #         f.write(str(elapsed_time) + '\n')
    #         f.write('\n')

if __name__ == "__main__":
    main()