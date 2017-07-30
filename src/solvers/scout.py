import numpy as np
import itertools
import copy
import time
import sys
from functions import complex as cmplx
from random_neighbor import chose_random_node_to_visit
from nearest_neighbor import chose_nearest_node_to_visit



def chose_mcmc_node_to_visit(args, current_node_index, vertex_weights):

    # initalize the walkers
    n_steps_to_scout_this_loop = np.min([n_nodes - dummy_index - 1, args['N_STEPS']])
    walker_costs = np.zeros([args['N_WALKERS']])
    walker_paths = np.zeros([args['N_WALKERS'], n_steps_to_scout_this_loop + 1])
    walker_paths[:, 0] = copy.deepcopy(current_node_index)

    #  for each ...
    for walker_index in range(0, args['N_WALKERS']):

        # ... define a unqiue vertex weight matrix and its current location
        vertex_weights_for_walker = copy.deepcopy(vertex_weights)
        current_node_index_for_walker = copy.deepcopy(current_node_index)
    
        for dummy_walker_step_index in range(0, n_steps_to_scout_this_loop):

            next_node_index_for_walker = chose_random_node_to_visit(args, current_node_index_for_walker, vertex_weights_for_walker)
            walker_costs[walker_index] =+ vertex_weights_for_walker[current_node_index_for_walker, next_node_index_for_walker]

            vertex_weights_for_walker[current_node_index_for_walker, :] = np.inf
            vertex_weights_for_walker[:, current_node_index_for_walker] = np.inf

            walker_paths[walker_index, dummy_walker_step_index] = next_node_index_for_walker
            current_node_index_for_walker = next_node_index_for_walker

    # evaluate scouting results
    walker_index_of_min_cost = np.where(walker_costs == np.min(walker_costs))[0]
    if len(walker_index_of_min_cost) is not 1:
        randomly_chosen_index = np.random.randint(0, len(walker_index_of_min_cost))
        walker_index_of_min_cost = int(walker_index_of_min_cost[randomly_chosen_index])
    else:
        walker_index_of_min_cost = int(walker_index_of_min_cost)

    for i in range(0, n_walkers):
        print walker_paths[i], walker_costs[i]

    return walker_paths[walker_index_of_min_cost][1]



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
        
        if args['N_STEPS'] > n_nodes - dummy_index - 1:
            next_node_index = chose_mcmc_node_to_visit(args, current_node_index, vertex_weights)
        else:
            next_node_index = chose_nearest_node_to_visit(args, current_node_index, vertex_weights)

        cost_of_path_so_far =+ vertex_weights[current_node_index, next_node_index]

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
    solution['SOLVER'] = 'nearest_neighbor'

    if args['--verbose']:
        print '- path, cost:'
        print '\t'+str(solution['path'])+', '+str(solution['cost_of_path'])

    return solution
