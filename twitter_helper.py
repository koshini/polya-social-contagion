import tweepy, json, collections, functools, operator
import networkx as nx
from main import set_positions
import pylab
import matplotlib.pyplot as plt
import pandas as pd

oauth = json.loads(open('oauth.json', 'r').read())

# Create a twitter API connection w/ OAuth.
auth = tweepy.OAuthHandler(oauth['consumer_key'], oauth['consumer_secret'])
auth.set_access_token(oauth['access_token'], oauth['access_token_secret'])
api = tweepy.API(auth)
# the user that we want to scrape
screen_name = 'name_alreadytak'

def main():
    # get_first_friends()
    # get_second_friends()
    graph = create_graph_from_matrix('data/fb-adjacency-matrix.csv')
    # pylab.show()
    # pylab.ion()
    draw_graph(graph)
    # pylab.ioff()


    # fill_out_graph()
    print()


def get_first_friends():
    friends = []
    friend_cursors = tweepy.Cursor(api.friends, id = screen_name)
    for friend_cursor in friend_cursors.items():
        friend = {}
        friend['screen_name'] = friend_cursor.screen_name
        friend['friends_count'] = friend_cursor.friends_count
        friend['followers_count'] = friend_cursor.followers_count
        friend['name'] = friend_cursor.name
        friend['profile_image_url'] = friend_cursor.profile_image_url
        friend['id'] = friend_cursor.id
        friend['following'] = friend_cursor.following
        friends.append(friend)

    f = open('data/myfriends.json', 'w')
    f.seek(0)
    friends_json = json.dumps(friends, sort_keys=True, indent=4)
    f.write(friends_json)
    f.truncate()
    f.close()

    # totals = functools.reduce(operator.add, map(collections.Counter, friends))
    # print("%s is follwing: %s" % (screen_name, len(friends)))
    # print ("They follow a total of: %s" % totals['friends_count'])
    # print ("And have a following of: %s" % totals['followers_count'])

def get_second_friends():
    nodes = []
    f = open('data/myfriends.json','r').read()
    friends = json.loads(f)
    friend_ids = [f['id'] for f in friends]
    for friend_id in friend_ids:
        print("Getting followers for %s" % friend_id)
        id_list = api.friends_ids(user_id=friend_id)
        node = {}
        node['id'] = friend_id
        nodes.append(node)
        for second_id in id_list:
            second_node = {}
            second_node['id'] = second_id
            write_edgelist(friend_id, second_id)
            nodes.append(second_node)

    f = open('data/nodes.json', 'w')
    f.seek(0)
    nodes_json = json.dumps(nodes, sort_keys=True, indent=4)
    f.write(nodes_json)
    f.truncate()
    f.close()

def write_edgelist(follower, followed):
    f = open('data/twitter.edgelist', 'a')
    f.write("%s %s\n" % (follower, followed))
    f.close()

def create_graph_from_edgelist(filename):
    # Edgelist looks like:
    # node1 node2
    # node3 node1
    # node1 node3
    # ...
    G = nx.read_edgelist(filename, create_using=nx.Graph())
    print("Read in edgelist file ", filename)
    print(nx.info(G))
    return G

# takes an adjacency matrix in csv format
def create_graph_from_matrix(filename):
    input_data = pd.read_csv(filename, header=None)
    G = nx.Graph(input_data.values)
    print(nx.info(G))
    return G


def fill_out_graph():
    # mygraph = json.loads(open('data/nodes.json', 'r').read())
    mygraph = json.loads(open('data/graph.json', 'r').read())
    last_filled = mygraph["pointer"]
    node_list = mygraph["nodes"]
    for node in mygraph["nodes"][last_filled:]:
        try:
            full_user = api.get_user(id=node['id'])
            node['screen_name'] = full_user.screen_name
            node['friends_count'] = full_user.friends_count
            node['followers_count'] = full_user.followers_count
            node['name'] = full_user.name
            node['following'] = full_user.following
            last_filled = mygraph.index(node)
            print(last_filled)
        except Exception as e:
            print(e)
            break

    f = open('data/graph.json', 'w')
    f.seek(0)
    graph = {}

    graph["pointer"] = last_filled
    graph["nodes"] = mygraph
    graph_json = json.dumps(graph, sort_keys=True, indent=4)
    f.write(graph_json)
    f.truncate()
    f.close()


def draw_graph(G):
    # pylab.clf()
    set_positions(G)
    color_map = set_color(G)
    nx.draw(G, nx.get_node_attributes(G, 'pos'), node_color=color_map, node_size=3)
    plt.show()


def set_color(G):
    color_map = ['red'] * len(G.node.items())
    return color_map


if __name__ == '__main__':
    main()