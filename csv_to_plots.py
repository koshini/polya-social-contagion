import matplotlib.pyplot as plt
import numpy as np

strat_list = []
topology = 'meetup'
folder = 'Tegan/'

# strat_list.append({
#     'red_strat': 'uniform',
#     'black_strat': 'entropy',
# })

strat_list.append({
    'red_strat': 'uniform',
    'black_strat': 'gradient',
})

strat_list.append({
    'red_strat': 'bot',
    'black_strat': 'gradient',
})

# strat_list.append({
#     'red_strat': 'bot',
#     'black_strat': 'centrality_entropy',
# })
#
# strat_list.append({
#     'red_strat': 'bot',
#     'black_strat': 'follow_bot',
# })

# strat_list.append({
#     'red_strat': 'uniform',
#     'black_strat': 'gradient',
# })

waste_label = []
infection_label = []
for strat_dict in strat_list:
    infection_csv = folder + 'empirical-infection' + topology + strat_dict['red_strat'] + strat_dict[
        'black_strat'] + 'infection.csv'
    waste_csv = folder + topology + strat_dict['red_strat'] + strat_dict['black_strat'] + 'waste.csv'
    waste_array = np.loadtxt(waste_csv, delimiter=',', unpack=True)
    # avg_waste = waste_array # if there is only one row
    avg_waste = np.mean(waste_array, axis=1)
    plt.figure(1)
    plt.plot(list(range(avg_waste.size)), avg_waste, label = 'red: ' + strat_dict['red_strat'] + ', black: ' + strat_dict['black_strat'])

    plt.figure(2)
    infection_array = np.loadtxt(infection_csv, delimiter=',', unpack=True)
    avg_infection = np.mean(infection_array, axis=1)
    # avg_infection = infection_array # if there is only one row
    plt.plot(list(range(avg_infection.size)), avg_infection, label = 'red: ' + strat_dict['red_strat'] + ', black: ' + strat_dict['black_strat'])


plt.figure(1)
plt.legend(loc='best', prop={'size': 5})
plt.axis([0,500, 0, 10])
title = topology + ' Average Wasted Budget per Node'

plt.figure(2)
plt.legend(loc='best', prop={'size': 5})
plt.axis([0,500, 0.1, 0.9])
title = topology + ' Network Empirical Infection'

plt.show()

print()

