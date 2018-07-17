'''
1) bfs_visited;
2) cc_visited;
3) largest_cc_size;
4) compute_resilience.
'''

from collections import deque

import urllib2
import random
import time
import math

# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
import matplotlib.pyplot as plt

def bfs_visited(ugraph, start_node):
    '''
    Takes an undirected graph and a starting node.
    Returns a connected component including the starting node.
    '''
    queue = deque([start_node])
    visited = {start_node}

    while queue != deque():
        current = queue.popleft()

        for nbr in ugraph[current]:
            if nbr not in visited:
                visited.add(nbr)
                queue.append(nbr)

    return visited

def cc_visited(ugraph):
    '''
    Takes an undirected graph.
    Returns a list of connected components.
    '''
    remaining_nodes = set(ugraph.keys())
    cc_list = []

    while remaining_nodes != set():
        current = remaining_nodes.pop()
        cc_set = bfs_visited(ugraph, current)
        cc_list.append(cc_set)
        remaining_nodes = remaining_nodes - cc_set

    return cc_list

def largest_cc_size(ugraph):
    '''
    Takes an undirected graph.
    Returns the size of the largest connected component.
    '''
    cc_list = cc_visited(ugraph)
    sizes = map(len, cc_list)

    if sizes == []:
        return 0

    return max(sizes)

def remove_node(ugraph, target):
    '''
    Takes an undirected graph and a node.
    Modifies the graph: removes the node and its edges.
    '''
    if target in ugraph:
        nbrs = ugraph[target]
        ugraph.pop(target)

        for nbr in nbrs:
            ugraph[nbr].remove(target)

def compute_resilience(ugraph, attack_order):
    '''
    Takes an undirected graph and a list of nodes.
    Returns a list of largest sizes of connected components as nodes get
    removed one by one.
    '''
    cc_sizes = [largest_cc_size(ugraph)]

    for target in attack_order:
        remove_node(ugraph, target)
        cc_sizes.append(largest_cc_size(ugraph))

    return cc_sizes

"""
Provided code for Application portion of Module 2
"""

############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    

##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[:-1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph
    
def add_edge(ugraph, node1, node2):
    '''
    Takes an undirected graph and two nodes.
    Modifies the graph by making an edge between
    the two nodes.
    '''
    if node1 not in ugraph:
        ugraph[node1] = set()
    if node2 not in ugraph:
        ugraph[node2] = set()

    if node2 not in ugraph[node1]:
        ugraph[node1].add(node2)
    if node1 not in ugraph[node2]:
        ugraph[node2].add(node1)

def ER_graph(num_nodes, edge_prob):
    '''
    Returns a random undirected graph of num_nodes nodes.
    '''
    graph = {node: set() for node in range(num_nodes)}

    for node1 in range(num_nodes):
        for node2 in range(node1 + 1, num_nodes):
            rand = random.random()
            if rand < edge_prob:
                add_edge(graph, node1, node2)

    return graph
    
"""
Provided code for application portion of module 2

Helper class for implementing efficient version
of UPA algorithm
"""

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

def make_complete_graph(num_nodes):
    '''
    Return a complete undirected graph of num_nodes edges.
    '''
    graph = {}
    for node in range(num_nodes):
        graph[node] = set([nbr for nbr in range(num_nodes) if nbr != node])
    return graph


def UPA_graph(node_num, edge_num):
    '''
    Takes the final number of nodes and number of nodes each node is
    connected to.
    Returns an undirected graph as a dictionary.
    '''
    graph = make_complete_graph(edge_num)
    trial = UPATrial(edge_num)

    for node in range(edge_num, node_num):
        nbrs = trial.run_trial(edge_num)
        graph[node] = nbrs

        for nbr in nbrs:
            add_edge(graph, nbr, node)

    return graph

def count_edge(ugraph):
    '''
    Takes an undirected graph.
    Returns the number of edges.
    '''
    edge_num = 0
    for nbrs in ugraph.values():
        edge_num += len(nbrs)
    return edge_num / 2
    
def random_order(graph):
    '''
    Takes a graph.
    Returns a list of all nodes in random order.
    '''
    nodes = graph.keys()
    random.shuffle(nodes)
    return nodes

def fast_targeted_order(ugraph):
    '''
    Takes an undirected graph.
    Returns an ordered list of nodes in drecreasing order of their
    degrees after previous nodes are removed.
    '''
    graph = copy_graph(ugraph)

    # Initialize degree sets
    degree_sets = [set() for dummy_degree in range(len(graph))]
    for node in graph:
        degree_sets[len(graph[node])].add(node)

    targeted_order = []

    for degree in range(len(graph) - 1, -1, -1):
        while degree_sets[degree] != set():
            # Arbitrary target
            target = degree_sets[degree].pop()

            for nbr in graph[target]:
                degree_sets[len(graph[nbr])].remove(nbr)
                degree_sets[len(graph[nbr]) - 1].add(nbr)

            targeted_order.append(target)
            remove_node(graph, target)

    return targeted_order

def random_resilience(network_graph, ER_graph, UPA_graph):
    '''
    Plots resilience of the three graphs after certain number
    of nodes are randomly removed.
    '''
    network_x = [node for node in range(len(network_graph) + 1)]
    network_y = compute_resilience(network_graph, random_order(network_graph))

    ER_x = [node for node in range(len(ER_graph) + 1)]
    ER_y = compute_resilience(ER_graph, random_order(ER_graph))

    UPA_x = [node for node in range(len(UPA_graph) + 1)]
    UPA_y = compute_resilience(UPA_graph, random_order(UPA_graph))

    plt.title('Resilience and number of nodes removed with random order')
    plt.xlabel('Number of nodes removed')
    plt.ylabel('Size of the largest connected component')
    plt.plot(network_x, network_y, label = 'Network graph')
    plt.plot(ER_x, ER_y, label = 'ER graph with p = 0.00397')
    plt.plot(UPA_x, UPA_y, label = 'UPA graph with m = 2')
    plt.legend(loc = 'upper right')
    plt.show()


def UPA_order_timing(node_range, edge_num):
    '''
    Plots the running time of targeted_order and fast_targeted_order.
    '''
    targeted_X = list(range(node_range[0], node_range[1], node_range[2]))
    targeted_Y = []
    fast_targeted_X = targeted_X
    fast_targeted_Y = []

    for node_num in range(node_range[0], node_range[1], node_range[2]):
        graph = UPA_graph(node_num, edge_num)

        start = time.clock()
        targeted_order(graph)
        targeted_Y.append(time.clock() - start)

        start = time.clock()
        fast_targeted_order(graph)
        fast_targeted_Y.append(time.clock() - start)

    plt.title('Running time of TO and FTO on desktop Python')
    plt.xlabel('Number of nodes of UPA graph with m = 5')
    plt.ylabel('Running time')
    plt.plot(targeted_X, targeted_Y, label = 'targeted_order')
    plt.plot(fast_targeted_X, fast_targeted_Y, label = 'fast_targeted_order')
    plt.legend(loc = 'upper right')
    plt.show()

def targeted_resilience(network_graph, ER_graph, UPA_graph, order_func):
    '''
    Plots resilience of the three graphs after certain number
    of nodes are removed in order of decreasing degree.
    '''
    network_x = [node for node in range(len(network_graph) + 1)]
    network_y = compute_resilience(network_graph, order_func(network_graph))

    ER_x = [node for node in range(len(ER_graph) + 1)]
    ER_y = compute_resilience(ER_graph, order_func(ER_graph))

    UPA_x = [node for node in range(len(UPA_graph) + 1)]
    UPA_y = compute_resilience(UPA_graph, order_func(UPA_graph))

    plt.title('Resilience and number of nodes removed with targeted order')
    plt.xlabel('Number of nodes removed')
    plt.ylabel('Size of the largest connected component')
    plt.plot(network_x, network_y, label = 'Network graph')
    plt.plot(ER_x, ER_y, label = 'ER graph with p = 0.00397')
    plt.plot(UPA_x, UPA_y, label = 'UPA graph with m = 2')
    plt.legend(loc = 'upper right')
    plt.show()

NETWORK_GRAPH= load_graph(NETWORK_URL)
# Question 1

# print count_edge(NETWORK_GRAPH)
ER_GRAPH = ER_graph(1239, 0.00397)
# print len(ER_GRAPH)
# print count_edge(ER_GRAPH)
# edge_prob = 0.00397

UPA_GRAPH = UPA_graph(1239, 2)
# print count_edge(UPA_GRAPH)
# edge_num = 2

# random_resilience(NETWORK_GRAPH, ER_GRAPH, UPA_GRAPH)

# Question 2
# All three are resilient.

# Question 3

# targeted_order = O(n^2)
# fast_targeted_order = O(n)

# UPA_order_timing((10, 1000, 10), 5)

# Question 4
# targeted_resilience(NETWORK_GRAPH, ER_GRAPH, UPA_GRAPH, fast_targeted_order)

# Question 5
# ER

