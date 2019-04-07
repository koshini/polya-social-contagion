import matplotlib.pyplot as plt
import numpy as np

strat_list = []
topology = 'facebook'
folder = 'pre-cured-equal/'

strat_list.append({
    'red_strat': 'bot',
    'black_strat': 'uniform',
})

strat_list.append({
    'red_strat': 'bot',
    'black_strat': 'pure_centrality_threshold',
})

strat_list.append({
    'red_strat': 'bot',
    'black_strat': 'centrality_threshold',
})

strat_list.append({
    'red_strat': 'bot',
    'black_strat': 'pure_centrality',
})

strat_list.append({
    'red_strat': 'bot',
    'black_strat': 'follow_bot',
})

# strat_list.append({
#     'red_strat': 'bot',
#     'black_strat': 'gradient',
# })



waste_label = []
infection_label = []
for strat_dict in strat_list:
    red_strat = strat_dict['red_strat'].replace('_', ' ')
    black_strat = strat_dict['black_strat'].replace('_', ' ')
    if black_strat == 'pure centrality entropy':
        black_strat = 'centrality threshold'
    infection_csv = folder + 'empirical-infection' + topology + strat_dict['red_strat'] + strat_dict['black_strat'] + 'infection.csv'
    # waste_csv = folder + topology + strat_dict['red_strat'] + strat_dict['black_strat'] + 'waste.csv'
    # waste_array = np.loadtxt(waste_csv, delimiter=',', unpack=True)
    # avg_waste = waste_array # if there is only one row
    # avg_waste = np.mean(waste_array[0:50], axis=1)
    # plt.figure(1)
    # plt.xlabel('Time step')
    # plt.ylabel('Average budget wasted per node')
    # plt.plot(list(range(avg_waste.size)), avg_waste, label = black_strat)

    plt.figure(2)
    infection_array = np.loadtxt(infection_csv, delimiter=',', unpack=True)
    avg_infection = np.mean(infection_array, axis=1)
    plt.xlabel('Time step')
    plt.ylabel('Average infection rate')
    # avg_infection = infection_array # if there is only one row
    plt.plot(list(range(avg_infection.size)), avg_infection, label = black_strat)


plt.figure(1)
plt.legend(loc='best', prop={'size': 9})
plt.axis([0, 60, 0, 12])
filename = folder + topology + ' waste.png'
plt.savefig(filename)

plt.figure(2)
# plt.legend(loc='best', prop={'size': 9})
plt.axis([0, 300, 0, 1])
filename = folder + topology + ' infection.png'
plt.savefig(filename)

print()

