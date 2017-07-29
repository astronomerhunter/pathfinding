# -------------------------------------------------------------------------------------- #
# This solver script estimates the shortest path through a node_locations.  It does that by
# choosing the nearest city to go to next.  It prints a progress bar in 10% increments.
# -------------------------------------------------------------------------------------- #
import numpy as np
import itertools
import copy
import time
import sys
from functions import complex as cmplx


def solve(args, node_locations, node_metadata):

    start_time = time.strftime("%H:%M:%S")
    n_nodes = node_metadata['number_of_nodes']
    solution = {}

    if args['--verbose']:
        print 'INFO: Begining solve().'
        print '- start time:', start_time
        print '- method:', __file__
        print '- n_nodes:', n_nodes
        print '- populating vertex weight matrix'

    vertex_weights = cmplx.create_vertex_weights_matrix(node_locations, n_nodes)
    solution['vertex_weights'] = vertex_weights.tolist()

    if args['--verbose']:
        print '- done'

    # visit origin node
    current_node_index = 0
    #vertex_weights[current_node_index, :] = np.inf
    #vertex_weights[:, current_node_index] = np.inf

    # from any given node, one must travel to a new node, thus the diagnal should be infinite cost
    # we also don't want repeats in this table make the matrix an upper triangle
    for i in range(0, n_nodes):
        vertex_weights[i, i] = np.inf

    # define variables to track journey
    cost_of_path_so_far = 0.0
    path_so_far = [current_node_index]

    # create progress bar for tracking
    progress_bar = [0]*10

    # loop through cities until all have been hit choosing to visit nearest neighbor
    if args['--verbose']:
        print '- begining nearest neighbor path'

    
    for dummy_index in range(0, n_nodes-1):

        if args['--verbose']:
            progress_bar = cmplx.print_progress_bar(progress_bar,
                                                    dummy_index,
                                                    n_nodes)

        nearest_node_index = np.where(vertex_weights[current_node_index] == np.min(vertex_weights[current_node_index]))[0]
        if len(nearest_node_index) is not 1:
            if args['--verbose']:
                print '- found more than 1 equidistance nearest neighbors, randomly selecting one'
            randomly_chosen_index = np.random.randint(0, len(nearest_node_index))
            nearest_node_index = nearest_node_index[randomly_chosen_index]
        nearest_node_index = int(nearest_node_index)

        cost_of_path_so_far = cost_of_path_so_far + vertex_weights[current_node_index, nearest_node_index]
        # make sure we dont revisit this node, do this by setting cost to it as infinite
        vertex_weights[current_node_index, :] = np.inf
        vertex_weights[:, current_node_index] = np.inf

        path_so_far.append(nearest_node_index)

        current_node_index = nearest_node_index

    end_time = time.strftime("%H:%M:%S")
    if args['--verbose']:
        print '- end time:', end_time

    solution['start_time'] = start_time
    solution['end_time'] = end_time
    solution['cost_of_path'] = cost_of_path_so_far
    solution['path'] = path_so_far
    solution['SOLVER'] = 'greedy'

    if args['--verbose']:
        print '- path, cost:'
        print '\t'+str(solution['path'])+', '+str(solution['cost_of_path'])

    return solution
