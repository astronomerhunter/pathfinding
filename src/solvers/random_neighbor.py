# -------------------------------------------------------------------------------------- #  
# Randomly travels to cities.  Does not return to the origin city at end.
# -------------------------------------------------------------------------------------- #
import numpy as np
import itertools
import time
import sys
from functions import complex as cmplx
import random

# -------------------------------------------------------------------------------------- #
# Functions go here


# -------------------------------------------------------------------------------------- #
def solve(args, node_locations, node_metadata):
    # This function finds the fastest route through the node_locations.
    #
    start_time = time.strftime("%H:%M:%S")
    print ' INFO: Begining solve().'
    print '\t- start time:', start_time
    print '\t- method:', __file__
    n_nodes = node_metadata['number_of_nodes']
    print '\t- n_nodes:', n_nodes

    solution = {}

    # see if an origin city has been defined
    if "origin_city" not in args or args['origin_city'] == '':
        origin_node = np.random.randint(0, n_nodes)
        print '\t- origin city randomly selected'
    else:
        origin_node = int(args['origin_city'])
        print '\t- origin in config file as',origin_node
    
    # populate distance matrix
    print '\t- populating distance matrix'
    vertex_weights = cmplx.create_distance_matrix(node_locations, n_nodes)
    print '\t\t- done'

    # randomly order the nodes
    visited_nodes = range(0,n_nodes)
    random.shuffle(path_indexs)
    path_indexs.remove(origin_node)
    path_indexs.insert(0,origin_node)

    # travel the randomly chosen path, tracking distance
    distance = 0.0
    for index in range(0, len(path_indexs)-1):
        distance = distance + vertex_weights[path_indexs[index],path_indexs[index+1]]
    
    # wrap up
    end_time = time.strftime("%H:%M:%S")
    print '\t- end time:', end_time

    # save values in solution
    solution['start_time'] = start_time
    solution['end_time'] = end_time
    solution['vertex_weights'] = vertex_weights
    solution['distance'] = distance
    solution['end_time'] = end_time
    solution['path_indexs'] = path_indexs
    solution['alg'] = 'random_neighbor'
    
    return solution
