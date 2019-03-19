import matplotlib.pyplot as plt
import numpy as np

strat_list = []
topology = 'facebook'
folder = 'results/'


# strat_list.append({
#     'red_strat': 'bot',
#     'black_strat': 'gradient',
# })

strat_list.append({
    'red_strat': 'uniform',
    'black_strat': 'entropy',
})

strat_list.append({
    'red_strat': 'uniform',
    'black_strat': 'uniform',
})



waste_label = []
infection_label = []
for strat_dict in strat_list:
    red_strat = strat_dict['red_strat'].replace('_', ' ')
    black_strat = strat_dict['black_strat'].replace('_', ' ')
    if black_strat == 'centrality entropy':
        black_strat = 'centrality adjusted threshold'
    elif black_strat == 'pure centrality entropy':
        black_strat = 'centrality threshold'
    infection_csv = folder + 'empirical-infection' + topology + strat_dict['red_strat'] + strat_dict['black_strat'] + 'infection.csv'
    waste_csv = folder + topology + strat_dict['red_strat'] + strat_dict['black_strat'] + 'waste.csv'
    waste_array = np.loadtxt(waste_csv, delimiter=',', unpack=True)
    # avg_waste = waste_array # if there is only one row
    avg_waste = np.mean(waste_array, axis=1)
    plt.figure(1)
    plt.plot(list(range(avg_waste.size)), avg_waste, label = 'red: ' + red_strat + ', black: ' + black_strat)

    plt.figure(2)
    infection_array = np.loadtxt(infection_csv, delimiter=',', unpack=True)
    avg_infection = np.mean(infection_array, axis=1)
    # avg_infection = infection_array # if there is only one row
    plt.plot(list(range(avg_infection.size)), avg_infection, label = 'red: ' + red_strat + ', black: ' + black_strat)


plt.figure(1)
plt.legend(loc='best', prop={'size': 9})
plt.axis([0, 500, 0, 12])
title = topology + ' Average Wasted Budget per Node'

plt.figure(2)
plt.legend(loc='best', prop={'size': 9})
plt.axis([0, 500, 0, 1])
title = topology + ' Network Empirical Infection'

plt.show()

print()

