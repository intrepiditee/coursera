'''
Algorithmic Thinking Appication 3
'''

import random
import time
import alg_cluster
import alg_project3_solution
import matplotlib.pyplot as plt
import alg_project3_viz

def gen_random_clusters(num_clusters):
    '''
    Takes the number of clusters desired.
    Returns a list of clusters that corresponds to randomly generated points
    between (-1, -1) and (1, 1).
    '''
    return [alg_cluster.Cluster(set(), random.uniform(-1, 1), random.uniform(-1, 1), 0.0, 0.0)
            for dummy in range(num_clusters)]


def plot_running_time(sizes):
    '''
    Plots running time vs size of list of clusters.
    '''
    x_values = list(range(sizes[0], sizes[1] + 1))
    y_slow_values = []
    y_fast_values = []

    cluster_lists = [gen_random_clusters(size) for size in range(sizes[0], sizes[1] + 1)]

    for cluster_list in cluster_lists:

        start = time.clock()
        Project3.slow_closest_pair(cluster_list)
        y_slow_values.append(time.clock() - start)

        start = time.clock()
        Project3.fast_closest_pair(cluster_list)
        y_fast_values.append(time.clock() - start)

    plt.title('Running time vs size of list of clusters with slow and fast closest pair')
    plt.xlabel('Number of initial clusters')
    plt.ylabel('Running time in seconds')
    plt.plot(x_values, y_slow_values, label = 'slow_closest_pair')
    plt.plot(x_values, y_fast_values, label = 'fast_closest_pair')
    plt.legend(loc = 'upper right')
    plt.show()

def compute_distortion(cluster_list, data_table, clustering_method, num_clusters, num_iterations = 5):
    '''
    Takes a list of Clusters, the original data table, the clustering method,
    the number of output clusters, and potentially the number of iterations for
    K-means clustering.
    Returns the distortion of the input list of Clusters.
    '''
    if clustering_method == 'hierarchical':
        cluster_result = alg_project3_solution.hierarchical_clustering(cluster_list, num_clusters)
    elif clustering_method == 'k-means':
        cluster_result = alg_project3_solution.kmeans_clustering(cluster_list, num_clusters, num_iterations)
    else:
        print 'Invalid clustering method.'
        return

    ans = 0
    for cluster in cluster_result:
        ans += cluster.cluster_error(data_table)
    return ans

def gen_cluster_list(data_table_url):
    '''
    Takes url of data table.
    Returns a list of Clusters containing a single county and the data table.
    '''
    data_table = alg_project3_viz.load_data_table(data_table_url)

    cluster_list = []
    for county in data_table:
        cluster_list.append(alg_cluster.Cluster({county[0]}, county[1], county[2], county[3], county[4]))

    return (cluster_list, data_table)

def plot_distortions(data_table_url, num_clusters_range, num_iterations = 5):
    '''
    Question 10!!!!!!!!!!!!
    '''
    cluster_list, data_table = gen_cluster_list(data_table_url)

    if data_table_url == alg_project3_viz.DATA_111_URL:
        plt.title('Distortion curves for 111 county data set')
    elif data_table_url == alg_project3_viz.DATA_290_URL:
        plt.title('Distortion curves for 290 county data set')
    elif data_table_url == alg_project3_viz.DATA_896_URL:
        plt.title('Distortion curves for 896 county data set')
    else:
        print 'Invalid URL.'
        return

    plt.xlabel('Number of output clusters')
    plt.ylabel('Distortion')

    x_values = list(range(num_clusters_range[0], num_clusters_range[1] + 1))
    y_hierarchical = []
    y_k_means = []

    cluster_list_hierarchical = [cluster.copy() for cluster in cluster_list]

    for num_clusters in x_values:
        
        num_clusters_hierarchical = num_clusters_range[0] + num_clusters_range[1] - num_clusters
        y_hierarchical.append(compute_distortion(cluster_list_hierarchical, data_table,
                                                 'hierarchical', num_clusters_hierarchical,
                                                 num_iterations))

        y_k_means.append(compute_distortion(cluster_list, data_table, 'k-means', num_clusters,
                                            num_iterations))

    y_hierarchical.reverse()

    plt.plot(x_values, y_hierarchical, label = 'hierarchical')
    plt.plot(x_values, y_k_means, label = 'K-means')
    plt.legend(loc = 'upper right')
    plt.show()



# Question 1
# plot_running_time((2, 200))

# Question 2
#alg_project3_viz.plot_clusters(alg_project3_viz.DATA_3108_URL, 'hierarchical', 15)

# Question 3
#alg_project3_viz.plot_clusters(alg_project3_viz.DATA_3108_URL, 'k-means', 15, 5)

# Question 4
# K-means clustering is faster. Running time of hierarchical clustering is O((n^2)((logn)^2)),
# and running time of k-means clustering is O(n) if number of output clusters is fixed
# or O(n^2) if number of output of clusters is a fraction of number of input clusters. K-means
# clustering is more efficient, thus faster than hierarchical clustering.

# Question 5
# alg_project3_viz.plot_clusters(alg_project3_viz.DATA_111_URL, 'hierarchical', 9)

# Question 6
# alg_project3_viz.plot_clusters(alg_project3_viz.DATA_111_URL, 'k-means', 9, 5)

# Question 7

# CLUSTER_LIST_111, DATA_TABLE_111 = gen_cluster_list(alg_project3_viz.DATA_111_URL)
# print compute_distortion(CLUSTER_LIST_111, DATA_TABLE_111, 'hierarchical', 9)

# CLUSTER_LIST_111, DATA_TABLE_111 = gen_cluster_list(alg_project3_viz.DATA_111_URL)
# print compute_distortion(CLUSTER_LIST_111, DATA_TABLE_111, 'k-means', 9, 5)

# Hierarchical = 1.7516 * (10 ^ 11)
# K-means = 2.7125 * (10 ^ 11)

# Question 8

# While both clustering methods generated three clusters, the three clusters generated by
# hierarchical clustering consisted of counties closer to each other. Generated by K-means
# clustering, the cluster at the top consisted of counties from the entire three states
# that made up west coast.

# K-means clustering has higher distortion, because the inital clustering generated by K-means
# was according to total popolation in each county. Counties with smaller population far away
# were thus more likely to be included in other clusters instead of forming a cluster of their
# own.

# Question 9
# Hierarchical clustering

# Question 10

#CLUSTER_LIST_111, DATA_TABLE_111 = gen_cluster_list(alg_project3_viz.DATA_111_URL)
#CLUSTER_LIST_290, DATA_TABLE_290 = gen_cluster_list(alg_project3_viz.DATA_290_URL)
#CLUSTER_LIST_896, DATA_TABLE_896 = gen_cluster_list(alg_project3_viz.DATA_896_URL)

# plot_distortions(alg_project3_viz.DATA_111_URL, (6, 20), 5)
# plot_distortions(alg_project3_viz.DATA_290_URL, (6, 20), 5)
# plot_distortions(alg_project3_viz.DATA_896_URL, (6, 20), 5)

# Question 11
# For 111 data set, hierarchical clustering method consistently produces
# lower distortion clusterings. For 290 and 896 data sets, neither of the two
# methods consistently produces lower distortion clusterings.

# Question 12
# On these data sets, neither method dominates in all three areas: efficiency, automation,
# and quality. In terms of efficiency, k-means clustering is preferable to hierarchical
# clustering as long as the desired number of output clusters is known beforehand.
# However, in terms of automation, k-means clustering suffers from the drawback that
# a reliable method for determining the initial cluster centers needs to be available.
# Finally, in terms of quality, neither method produces clusterings with consistently
# lower distortion on larger data sets.


