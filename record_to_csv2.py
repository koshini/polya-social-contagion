import networkx as nx
from graph_generator import get_graph
from simulation import simulate, set_top_central_nodes
import time


def main():
    topology = 'facebook'
    G = get_graph()
    iterations = 600
    runs = 100

    node_count = 10
    red_budget = node_count * 10
    black_budget = node_count * 10

    initial_condition = {
        'node_count': 10,
        'parameter': 2,
        'red': 500,
        'black': 500,
        'dist': 'random'
    }

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

    for strat in strat_dict_list:
        print(str(strat))
        start = time.time()
        simulate(folder, topology, strat, iterations, runs, initial_condition=initial_condition)
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