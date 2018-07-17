'''
Coursera Algorithmic Thinking Project 2.
1) bfs_visited;
2) cc_visited;
3) largest_cc_size;
4) compute_resilience.
'''

from collections import deque

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
    ugraph.pop(target)

    for nbrs in ugraph.values():
        if target in nbrs:
            nbrs.remove(target)

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