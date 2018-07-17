"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster



######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """

    ans = (float('inf'), -1, -1)

    for index1 in range(len(cluster_list)):
        for index2 in range(len(cluster_list)):

            if index1 != index2:
                distance = cluster_list[index1].distance(cluster_list[index2])
                if distance < ans[0]:
                    if index1 < index2:
                        ans = (distance, index1, index2)
                    else:
                        ans = (distance, index1, index2)
                    
    return ans



def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    
    num_clusters = len(cluster_list)

    if num_clusters <= 3:
        ans = slow_closest_pair(cluster_list)
    else:
        mid_index = num_clusters / 2
        left_clusters = cluster_list[:mid_index]
        right_clusters = cluster_list[mid_index:]

        left_ans = fast_closest_pair(left_clusters)
        right_ans = fast_closest_pair(right_clusters)

        if left_ans[0] < right_ans[0]:
            ans = left_ans
        else:
            ans = (right_ans[0], right_ans[1] + mid_index, right_ans[2] + mid_index)

        mid = (cluster_list[mid_index - 1].horiz_center() +
                        cluster_list[mid_index].horiz_center()) / 2

        strip_ans = closest_pair_strip(cluster_list, mid, ans[0])
        if strip_ans[0] < ans[0]:
            ans = strip_ans

    return ans


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """

    strip_clusters = [cluster for cluster in cluster_list
                      if abs(cluster.horiz_center() - horiz_center) < half_width]

    strip_clusters.sort(key = lambda cluster: cluster.vert_center())
    num_clusters = len(strip_clusters)

    ans = (float('inf'), -1, -1)
    for index1 in range(0, num_clusters - 1):
        for index2 in range(index1 + 1, min(index1 + 3, num_clusters - 1) + 1):
            distance = strip_clusters[index1].distance(strip_clusters[index2])
            if distance < ans[0]:
                ans = (distance, index1, index2)

    if ans[0] == float('inf'):
        return ans

    index1 = cluster_list.index(strip_clusters[ans[1]])
    index2 = cluster_list.index(strip_clusters[ans[2]])

    if index1 < index2:
        return (ans[0], index1, index2)
    else:
        return (ans[0], index2, index1)
            

######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    
    while len(cluster_list) > num_clusters:
        cluster_list.sort(key = lambda cluster: cluster.horiz_center())

        dist_indexes = fast_closest_pair(cluster_list)
        index1, index2= dist_indexes[1], dist_indexes[2]
        cluster1, cluster2 = cluster_list[index1], cluster_list[index2]

        cluster1.merge_clusters(cluster2)
        cluster_list.remove(cluster2)

    return cluster_list
######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
    
    len_clusters = len(cluster_list)    
    center_clusters = list(cluster_list)
    center_clusters.sort(key = lambda cluster: cluster.total_population(), reverse = True)
    center_clusters = center_clusters[:num_clusters]

    for dummy in range(num_iterations):
        empty_clusters = [alg_cluster.Cluster(set(), 0.0, 0.0, 0.0, 0.0) for dummy in range(num_clusters)]

        for index in range(len_clusters):
            current_cluster = cluster_list[index]
            distance = current_cluster.distance(center_clusters[0])
            min_dist_index = 0

            for center_index in range(num_clusters):
                center = center_clusters[center_index]
                dist_center = current_cluster.distance(center)
                if dist_center < distance:
                    distance = dist_center
                    min_dist_index = center_index

            empty_clusters[min_dist_index].merge_clusters(current_cluster)

        center_clusters = empty_clusters

    return empty_clusters


