'''
Algorithmic Thinking Project 1
1) make_complete_graph
2) compute_in_degrees
3) in_degree_distribution
'''

from collections import Counter

# Example graphs

EX_GRAPH0 = {0: set([1, 2]), 1: set(), 2: set()}

EX_GRAPH1 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3]), 3: set([0]),
             4: set([1]), 5: set([2]), 6: set()}

EX_GRAPH2 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3, 7]), 3: set([7]),
             4: set([1]), 5: set([2]), 6: set(), 7: set([3]), 8: set([1, 2]),
             9: set([0, 3, 4, 5, 6, 7])}

def make_complete_graph(num_nodes):
    '''
    Return a complete directed graph of num_nodes edges.
    '''
    ans = {}
    for node in range(num_nodes):
        ans[node] = set([nbr for nbr in range(num_nodes) if nbr != node])
    return ans

def compute_in_degrees(digraph):
    '''
    Return in-degrees of each node of a directed graph as a dictionary.
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
