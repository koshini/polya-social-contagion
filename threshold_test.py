import networkx as nx
from graph_generator import get_graph
from simulation import simulate
import time
import os


def main():


################################################################################################
    print('----------------facebook')
    topology = 'facebook'
    dir = topology + '/'
    if not os.path.exists(dir):
        os.mkdir(dir)
        print("Directory ", dir, " Created ")
    else:
        print("Directory ", dir, " already exists")


    red_mult = 1
    black_mult = 1
    graph_file = dir + str(red_mult) + '_' + str(black_mult) + '.json'
    G = get_graph(graph_file, topology)

    iterations = 500
    runs = 50

    node_count = nx.number_of_nodes(G)
    red_budget = node_count * 10
    black_budget = node_count * 10

    log_file = dir + 'log.txt'
    with open(log_file, 'a') as f:
        f.write('red budget: ' + str(red_budget) + '\n')
        f.write('black budget: ' +str(black_budget) + '\n')
        f.write('\n')

    strat_dict_list = []

    # threshold = 0.4
    # portion = 0.05
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'centrality_threshold',
    #     'threshold': threshold,
    #     'portion': portion
    # })
    #
    #
    # threshold = 0.4
    # portion = 0.1
    # strat_dict_list.append({
    #     'red_budget': red_budget,
    #     'black_budget': black_budget,
    #     'red_strat': 'bot',
    #     'black_strat': 'centrality_threshold',
    #     'threshold': threshold,
    #     'portion': portion
    # })


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
        prefix = str(strat['threshold']) + '_' + str(strat['portion'])
        simulate(graph_file, prefix, topology, strat, iterations, runs)
        elapsed_time = time.time() - start
        print(elapsed_time)
        print()

        log_file = dir + 'log.txt'
        with open(log_file, 'a') as f:
            f.write(str(strat) + '\n')
            f.write(str(elapsed_time) + '\n')
            f.write('\n')


################################################################################################
    print('----------------twitter')
    topology = 'twitter'
    dir = topology + '/'
    if not os.path.exists(dir):
        os.mkdir(dir)
        print("Directory ", dir, " Created ")
    else:
        print("Directory ", dir, " already exists")


    red_mult = 1
    black_mult = 1
    graph_file = dir + str(red_mult) + '_' + str(black_mult) + '.json'
    G = get_graph(graph_file, topology)

    iterations = 100
    runs = 50

    node_count = nx.number_of_nodes(G)
    red_budget = node_count * 10
    black_budget = node_count * 10

    log_file = dir + 'log.txt'
    with open(log_file, 'a') as f:
        f.write('red budget: ' + str(red_budget) + '\n')
        f.write('black budget: ' +str(black_budget) + '\n')
        f.write('\n')

    strat_dict_list = []


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
        prefix = str(strat['threshold']) + '_' + str(strat['portion'])
        simulate(graph_file, prefix, topology, strat, iterations, runs)
        elapsed_time = time.time() - start
        print(elapsed_time)
        print()

        log_file = dir + 'log.txt'
        with open(log_file, 'a') as f:
            f.write(str(strat) + '\n')
            f.write(str(elapsed_time) + '\n')
            f.write('\n')


################################################################################################
    print('----------------meetup')
    topology = 'meetup'
    dir = topology + '/'
    if not os.path.exists(dir):
        os.mkdir(dir)
        print("Directory ", dir, " Created ")
    else:
        print("Directory ", dir, " already exists")


    red_mult = 1
    black_mult = 1
    graph_file = dir + str(red_mult) + '_' + str(black_mult) + '.json'
    G = get_graph(graph_file, topology)

    iterations = 500
    runs = 50

    node_count = nx.number_of_nodes(G)
    red_budget = node_count * 10
    black_budget = node_count * 10

    log_file = dir + 'log.txt'
    with open(log_file, 'a') as f:
        f.write('red budget: ' + str(red_budget) + '\n')
        f.write('black budget: ' +str(black_budget) + '\n')
        f.write('\n')

    strat_dict_list = []


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
        prefix = str(strat['threshold']) + '_' + str(strat['portion'])
        simulate(graph_file, prefix, topology, strat, iterations, runs)
        elapsed_time = time.time() - start
        print(elapsed_time)
        print()

        log_file = dir + 'log.txt'
        with open(log_file, 'a') as f:
            f.write(str(strat) + '\n')
            f.write(str(elapsed_time) + '\n')
            f.write('\n')

if __name__ == "__main__":
    main()