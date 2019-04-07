import matplotlib.pyplot as plt
import numpy as np

strat_list = []
topology = 'barabasi'

threshold = 0.4
portion = 0
strat_list.append({
    'red_strat': 'bot',
    'black_strat': 'centrality_threshold',
    'threshold': threshold,
    'portion': portion
})

threshold = 0.4
portion = 0.01
strat_list.append({
    'red_strat': 'bot',
    'black_strat': 'centrality_threshold',
    'threshold': threshold,
    'portion': portion
})

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


for strat_dict in strat_list:
    prefix = ''
    red_strat = strat_dict['red_strat'].replace('_', ' ')
    black_strat = strat_dict['black_strat'].replace('_', ' ')
    infection_csv = topology + '/empirical-infection' + topology + strat_dict['red_strat'] + strat_dict[
        'black_strat'] + 'infection.csv'
    if strat_dict.get('threshold'):
        prefix = str(strat_dict['threshold']) + '_' + str(strat_dict['portion'])
    if prefix:
        infection_csv = topology + '/' + prefix + strat_dict['red_strat'] + strat_dict[
            'black_strat'] + 'infection.csv'


    plt.figure(1)
    infection_array = np.loadtxt(infection_csv, delimiter=',', unpack=True)
    # infection_array = np.insert(infection_array, 0, 0.2, axis=1)
    avg_infection = np.mean(infection_array, axis=1)
    plt.xlabel('Time step')
    plt.ylabel('Average infection rate')
    # avg_infection = infection_array # if there is only one row
    plt.plot(list(range(avg_infection.size)), avg_infection, label = prefix+strat_dict['black_strat'])

plt.figure(1)
plt.legend(loc='best', prop={'size': 10})
# plt.axis([0, 60, 0, 1]) # for twitter
plt.axis([0, 300, 0.2, 0.5])
filename = topology + '/' + 'vary-portion-infection.png'
plt.savefig(filename)
# plt.show()

