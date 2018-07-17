'''
Application 1
'''

from collections import Counter
import urllib2
import matplotlib.pyplot as plt
import random

GRAPH_URL = 'http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt'

def load_graph(url):
    '''
    Loads a graph given the URL for a text representation of the graph.
    Returns a dictionary that models a graph.
    '''
    ans = {}
    lines = urllib2.urlopen(url).readlines()
    for line in lines:
        node_list = map(int, line.split(' ')[:-1])
        ans[node_list[0]] = set(node_list[1:])
    return ans

def compute_in_degrees(digraph):
    '''
    Return in-degrees of each node of a directed graph as a dictionary mapping
    each node to its in-degree.
    '''
    ans = {}
    for node in digraph:
        ans[node] = 0
    for nbrs in digraph.values():
        for nbr in nbrs:
            ans[nbr] += 1
    return ans

def in_degree_distribution(digraph):
    '''
    Return unnormalized in_digree distribution of a directed graph.
    '''
    ans = Counter()
    for in_digree in compute_in_degrees(digraph).values():
        ans[in_digree] += 1
    return ans

def normalized_distribution(digraph):
    '''
    Take a in-degree distribution and normalize it.
    Return a new dictionary.
    '''
    ans = {}
    distribution = in_degree_distribution(digraph)
    freq_sum = sum(distribution.values())
    for degree, freq in distribution.items():
        ans[degree] = float(freq) / freq_sum
    return ans

def plot_distribution(digraph, is_log):
    '''
    Take a in-degree distribution as a dictionary and whether
    log transform in-degree and frequency.
    Plot a scatterplot.
    '''
    distribution = normalized_distribution(digraph)
    x_degree = []
    y_freq = []
    for degree in distribution:
        x_degree.append(degree)
        y_freq.append(distribution[degree])
    plt.plot(x_degree, y_freq, 'ro')
    if is_log:
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('log(in-degree)')
        plt.ylabel('log(frequency)')
    else:
        plt.xlabel('in-degree')
        plt.ylabel('frequency')

def generate_directed_graph(node_num, edge_prob):
    '''
    Take the number of nodes and the probability that an edge exisis from one
    node to another.
    Return a directed graph as a dictionary.
    '''
    ans = {}
    nodes = [node for node in range(node_num)]
    for node in nodes:
        ans[node] = set()
        for nbr in nodes:
            if node != nbr:
                rand = random.random()
                if rand < edge_prob:
                    ans[node].add(nbr)
    return ans

def make_complete_graph(num_nodes):
    '''
    Return a complete directed graph of num_nodes edges.
    '''
    ans = {}
    for node in range(num_nodes):
        ans[node] = set([nbr for nbr in range(num_nodes) if nbr != node])
    return ans

class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

def DPA_graph(node_num, edge_num):
    '''
    Takes the final number of nodes and number of nodes each node is
    connected to.
    Returns a directed graph as a dictionary.
    '''
    ans = make_complete_graph(edge_num)
    trial = DPATrial(edge_num)
    for node in range(edge_num, node_num):
        nbrs = trial.run_trial(edge_num)
        ans[node] = nbrs
    return ans

# Question 1

GRAPH = load_graph(GRAPH_URL)

# plt.figure(1)
# plt.title('log-log in-degree distribution of the citation graph')
# plot_distribution(GRAPH, True)

# plt.figure(2)
# plt.title('in-degree distribution of the citation graph')
# plot_distribution(GRAPH, False)

# Question 2

# ER_GRAPH = generate_directed_graph(2000, 0.5)

# plt.figure(3)
# plt.title('in-degree distribution of ER graph with 2000 nodes and probability 0.5')
# plot_distribution(ER_GRAPH, False)

# Question 3

# DPA_NODE_NUM = len(GRAPH.keys())
# DPA_EDGE_NUM = sum(compute_in_degrees(GRAPH).values()) / DPA_NODE_NUM
# print DPA_NODE_NUM, DPA_EDGE_NUM

# Question 4

# DPA_GRAPH = DPA_graph(DPA_NODE_NUM, DPA_EDGE_NUM)
# plt.figure(4)
# plt.title('log-log in-degree distribution of the DPA graph')
# plot_distribution(DPA_GRAPH, True)

# Question 5

# Answers

# The plot of the in-degree distribution of the DPA graph is indeed similar to
# that of the citation graph. They agree on all of the items listed in item c
# for Question 1. In particular, the points in both plots are accuratelyapproximated
# by a line with falling (negative) slope. In both cases, the points tend to scatter
# more as the fraction of points (papers) decreases.

# The correct phenomenon is "The rich gets richer". In Algorithm DPA, a node with a
# higher degree (rich) has a higher probability of getting a new edge (richer).
# This process modeled by Algorithm DPA mimics the behavior of "The rich gets richer"
# model in which the wealthy have the means to more easily acquire new wealth.

# The "Rich get richer" phenomenon provides an explanation for the structure of the
# citation graph. Papers (nodes) that have lots of citations (incoming edges) are
# more visible and, therefore, more likely to draw new citations (incoming edges)
# due to their visibility.

# Show plots
plt.show()

