"""
doc string
"""
import copy
import time
import sys
import numpy as np
from . import nearest_neighbor
from . import random_neighbor
from functions import complex as cmplx


def solve(args, node_locations, node_metadata):
    """
    description
    """

    try:
        args['N_WALKERS'] = int(args['N_WALKERS'])
        args['N_STEPS'] = int(args['N_STEPS'])
    except ValueError:
        print 'N_WALKERS and N_STEPS must be a integers.'
        sys.exit(1)
        # TODO: make these raise ValueError


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

    # from any given node, one must travel to a new node, thus the diagnal should be infinite cost
    for i in range(0, n_nodes):
        vertex_weights[i, i] = np.inf

    # define variables to track journey
    cost_of_path_so_far = 0.0
    path_so_far = [current_node_index]
    unvisited_nodes = range(1, n_nodes)

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
        
        if len(unvisited_nodes) > args['N_STEPS']:

            walker_costs = np.zeros(args['N_WALKERS'])
            walker_first_index = np.zeros(args['N_WALKERS'])

            for walker_index in range(0, args['N_WALKERS']):

                walker_unvisisted_nodes = copy.deepcopy(unvisited_nodes)

                # randomly create a path
                walker_path = np.random.choice(walker_unvisisted_nodes, args['N_STEPS'], replace=False)
                walker_first_index[walker_index] = walker_path[0]

                # sum the cost associated with traveling it
                for step_index in range(1, args['N_STEPS']):
                    walker_costs[walker_index] =+ vertex_weights[walker_path[step_index-1], walker_path[step_index]]

                if args['--verbose']:
                    print walker_path, walker_costs[walker_index]


            # pick the next node index
            probabilities = walker_costs/np.sum(walker_costs)
            next_node_index = int(np.random.choice(walker_first_index, size=1, replace=True, p=probabilities))


        # if there are less steps remaining than a walker would walk, grab the closest one
        else:
            next_node_index = nearest_neighbor.chose_nearest_node_to_visit(args, current_node_index, vertex_weights)


        cost_of_path_so_far =+ vertex_weights[current_node_index, next_node_index]

        # make sure we dont revisit this node, do this by setting cost to it as infinite
        vertex_weights[current_node_index, :] = np.inf
        vertex_weights[:, current_node_index] = np.inf

        path_so_far.append(next_node_index)
        unvisited_nodes.remove(next_node_index)
        current_node_index = next_node_index
    

    end_time = time.strftime("%H:%M:%S")
    if args['--verbose']:
        print '- end time:', end_time

    solution['start_time'] = start_time
    solution['end_time'] = end_time
    solution['cost_of_path'] = cost_of_path_so_far
    solution['path'] = path_so_far
    solution['SOLVER'] = 'nearest_neighbor'

    if args['--verbose']:
        print '- path, cost:'
        print '\t'+str(solution['path'])+', '+str(solution['cost_of_path'])

    return solution
