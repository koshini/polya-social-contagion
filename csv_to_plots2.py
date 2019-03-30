import matplotlib.pyplot as plt
import numpy as np

strat_list = []
topology = 'meetup'

# threshold = 0.4
# portion = 0
# strat_list.append({
#     'red_strat': 'bot',
#     'black_strat': 'centrality_threshold',
#     'threshold': threshold,
#     'portion': portion
# })
#
# threshold = 0.6
# portion = 0
# strat_list.append({
#     'red_strat': 'bot',
#     'black_strat': 'centrality_threshold',
#     'threshold': threshold,
#     'portion': portion
# })

threshold = 0.4
portion = 0.02
strat_list.append({
    'red_strat': 'bot',
    'black_strat': 'centrality_threshold',
    'threshold': threshold,
    'portion': portion
})


threshold = 0.4
portion = 0.05
strat_list.append({
    'red_strat': 'bot',
    'black_strat': 'centrality_threshold',
    'threshold': threshold,
    'portion': portion
})


threshold = 0.4
portion = 0.1
strat_list.append({
    'red_strat': 'bot',
    'black_strat': 'centrality_threshold',
    'threshold': threshold,
    'portion': portion
})

threshold = 0.4
portion = 0.5
strat_list.append({
    'red_strat': 'bot',
    'black_strat': 'centrality_threshold',
    'threshold': threshold,
    'portion': portion
})





waste_label = []
infection_label = []
for strat_dict in strat_list:
    red_strat = strat_dict['red_strat'].replace('_', ' ')
    black_strat = strat_dict['black_strat'].replace('_', ' ')
    prefix = str(strat_dict['threshold']) + '_' + str(strat_dict['portion'])
    if black_strat == 'centrality entropy':
        black_strat = 'adjusted centrality threshold'
    elif black_strat == 'pure centrality entropy':
        black_strat = 'centrality threshold'
    infection_csv = topology + '/' + prefix + 'empirical-infection' + strat_dict['red_strat'] + strat_dict['black_strat'] + 'infection.csv'
    waste_csv = topology + '/' + prefix + strat_dict['red_strat'] + strat_dict['black_strat'] + 'waste.csv'
    waste_array = np.loadtxt(waste_csv, delimiter=',', unpack=True)
    # avg_waste = waste_array # if there is only one row
    avg_waste = np.mean(waste_array, axis=1)
    plt.figure(1)
    plt.xlabel('Time step')
    plt.ylabel('Average budget wasted per node')
    plt.plot(list(range(avg_waste.size)), avg_waste, label = prefix)

    plt.figure(2)
    infection_array = np.loadtxt(infection_csv, delimiter=',', unpack=True)
    # infection_array = np.insert(infection_array, 0, 0.2, axis=1)
    avg_infection = np.mean(infection_array, axis=1)
    plt.xlabel('Time step')
    plt.ylabel('Average infection rate')
    # avg_infection = infection_array # if there is only one row
    plt.plot(list(range(avg_infection.size)), avg_infection, label = prefix)


plt.figure(1)
# plt.legend(loc='best', prop={'size': 9})
# plt.axis([0, 60, 0, 8]) # for twitter
plt.axis([0, 300, 0, 8])
filename = topology + '/vary-portion' + ' waste.png'
plt.savefig(filename)

plt.figure(2)
plt.legend(loc='best', prop={'size': 12})
# plt.axis([0, 60, 0, 1]) # for twitter
plt.axis([0, 300, 0, 1])
filename = topology + '/vary-portion' + ' infection.png'
plt.savefig(filename)
# plt.show()
print()

