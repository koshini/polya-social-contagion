import networkx as nx
from graph_generator import get_graph
from simulation import simulate, set_top_central_nodes
import timeit


def main():
    topology = 'facebook'
    G = get_graph(topology)
    targets = set_top_central_nodes(G)

    iterations = 500
    runs = 200
    node_count = nx.number_of_nodes(G)
    red_budget = node_count * 10
    black_budget = node_count * 10
    strat_dict_list = []

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'uniform',
        'black_strat': 'entropy',
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'uniform',
        'black_strat': 'pure_centrality',
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'uniform',
        'black_strat': 'centrality_ratio',
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'uniform',
        'black_strat': 'centrality_entropy',
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'uniform',
        'black_strat': 'pure_centrality_entropy',
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'uniform',
        'black_strat': 'entropy2',
    })

    strat_dict_list.append({
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'uniform',
        'black_strat': 'bot',
    })

    for strat in strat_dict_list:
        print(str(strat))
        wrapped = wrapper(simulate,topology, strat, iterations, runs, targets)
        time = timeit.timeit(wrapped, number=runs)
        print(time)
        print()

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped



if __name__ == "__main__":
    main()