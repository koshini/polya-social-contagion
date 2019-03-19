import networkx as nx
from graph_generator import get_graph
from simulation import simulate
import time


def main():
    folder = 'results/'
    print('----------------twitter')
    topology = 'twitter'
    G = get_graph(topology)

    iterations = 100
    runs = 100

    node_count = nx.number_of_nodes(G)
    red_budget = node_count * 10
    black_budget = node_count * 10
    strat_dict_list = []

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'pure_centrality_entropy',
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'centrality_entropy',
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
        'black_strat': 'uniform',
    })


    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot',
        'black_strat': 'follow_bot',
    })

    for strat in strat_dict_list:
        print(str(strat))
        start = time.time()
        simulate(folder, topology,strat, iterations, runs)
        elapsed_time = time.time() - start
        print(elapsed_time)
        print()

        log_file = folder + 'log.txt'
        with open(log_file, 'a') as f:
            f.write(str(strat) + '\n')
            f.write(str(elapsed_time) + '\n')
            f.write('\n')

##########################################################################################
    print('----------------meetup')
    topology = 'meetup'
    G = get_graph(topology)

    iterations = 500
    runs = 100

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


    for strat in strat_dict_list:
        print(str(strat))
        start = time.time()
        simulate(folder, topology,strat, iterations, runs)
        elapsed_time = time.time() - start
        print(elapsed_time)
        print()

        log_file = folder + 'log.txt'
        with open(log_file, 'a') as f:
            f.write(str(strat) + '\n')
            f.write(str(elapsed_time) + '\n')
            f.write('\n')


##########################################################################################
    print('----------------facebook')
    topology = 'facebook'
    G = get_graph(topology)

    iterations = 500
    runs = 100

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


    for strat in strat_dict_list:
        print(str(strat))
        start = time.time()
        simulate(folder, topology,strat, iterations, runs)
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