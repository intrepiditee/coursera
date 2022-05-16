'''
Brute force algorith for finding shortest path.
'''

def gen_permutation(elements, length):
    '''
    Return all permutations of the elements as a set.
    '''
    if len(elements) == 0:
        return None
    ans = set([()])
    for dummy_trial in range(length):
        temp_set = set()
        for seq in ans:
            for elt in elements:
                if elt not in seq:
                    new_seq = list(seq)
                    new_seq.append(elt)
                    temp_set.add(tuple(new_seq))
        ans = temp_set
    return ans

def is_path(graph, path):
    '''
    Return whether the path is valid in the input graph.
    '''
    for index in range(len(path) - 1):
        node = path[index]
        if node not in graph or path[index + 1] not in graph[node]:
            return False
    return False

def find_shortest_path(graph, source, target):
    if len(graph.keys()) < 2:
        return None
    if is_path(graph, (source, target)):
        return (source, target), 1
    for length in range(2, len(graph.keys())):
        paths = set([path for path in gen_permutation(graph.keys(), length + 1)
                    if path[0] == source and path[-1] == target])
        for path in paths:
            if is_path(graph, path):
                return path, length
    return 1

#print find_shortest_path({1:{2,3}, 2:{1, 5}, 3:{4}, 4:{5}, 5:{2}}, 1, 5)
