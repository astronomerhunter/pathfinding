# -------------------------------------------------------------------------------------- #
# This solver script finds all the possible paths.  There are (N-1)! many where N is the 
# number of cities. It can take an extreamly long time when there are more than 10 cities.
# This solver prints a progress bar in 10% increments.
# -------------------------------------------------------------------------------------- #
import numpy as np
import itertools
import time
import sys
from functions import complex as cmplx


NUMBER_NODES_TO_WARN_USER = 9


def get_perms(N):
    """
    # returns N!, or the number of permutations. Ex: if N=3, function returns 6. This
    # function exists only because I may someday want to create a get_all_possible_routes()
    # by hand.  I would use this function in that.
    #
    """
    result = 1
    for i in range(1, N+1):
        result = result*i
    return result


def get_all_possible_routes(N, origin_node):
    """
    # Returns all possible routes, using Python indicies (first = 0) to as references
    # for cities.
    # 
    #    INPUTS:
    #        - N: integer, number of cities to calculate possible route for
    #        - origin_node: index of the origin city
    #    OUTPUTS:
    #        - possible_routes: [(N-1)!/2,N] sized array where each row is a unique route path. 
    #
    """
    # make a list of cities. be sure not to visit the origin city
    list_of_nodes = range(0,N-1)
    for index in range(0, len(list_of_nodes)):
        if list_of_nodes[index] > origin_node or list_of_nodes[index] == origin_node:
            list_of_nodes[index] = list_of_nodes[index] + 1
        else:
            pass
    # the fancy method to get the possible routes
    possible_routes = list( itertools.permutations(list_of_nodes) )
    # arrays are cool
    possible_routes = np.asarray(possible_routes)
    # tac on origin city as first node
    origin_adjusted_possible_routes = np.zeros([np.shape(possible_routes)[0],
                                                np.shape(possible_routes)[1]+1])
    origin_adjusted_possible_routes[:,0] = origin_node
    # fill the meat of the paths array with the old routes
    origin_adjusted_possible_routes[:,1:] = possible_routes
    return origin_adjusted_possible_routes
    
    
def solve(args, node_locations, node_metadata):
    """
    some description
    """
    start_time = time.strftime("%H:%M:%S")
    n_nodes = node_metadata['number_of_nodes']

    if args['--verbose']:
        print ' INFO: Begining solve().'
        print '\t- start time:', start_time
        print '\t- method:', __file__
        print '\t- n_nodes:', n_nodes

    if args['--force'] is False and n_nodes > NUMBER_NODES_TO_WARN_USER:
        print '\nWARNING: There are more than '+str(NUMBER_NODES_TO_WARN_USER)+' cities in this map, brute forcing may take a while.'
        if raw_input('\tWould you like to proceed? ["y" to continue]  ') != 'y':
            print 'INFO: user input cancelled solve().'
            sys.exit(1)

    solution = {}

    # TODO: make this variable!
    origin_node_index = 0

    if args['--verbose']:
        print '- getting all possible paths'

    paths = get_all_possible_routes(n_nodes, origin_node_index)

    if args['--verbose']:
        print '- aquired '+str(len(paths))+' of them'
        print '- populating vertex weight matrix'

    vertex_weights = cmplx.create_vertex_weights_matrix(node_locations, n_nodes)

    if args['--verbose']:
        print '- done'
        print '- begining calculation of each path length'

    progress_bar = [0]*10
    weights = np.zeros(np.shape(paths)[0])
    for i in range(0, len(weights)):
        this_path = paths[i,:]
        this_weight = 0
        for j in range(0, len(this_path)-1):
            origin_node_idx = int(this_path[j])
            destination_node_idx = int(this_path[j+1])
            this_weight = this_weight + vertex_weights[origin_node_idx, destination_node_idx]
        weights[i] = this_weight
        progress_bar = cmplx.print_progress_bar(progress_bar, i, len(weights))

    shortest_path_index = np.where(weights == min(weights))[0]

    end_time = time.strftime("%H:%M:%S")
    if args['--verbose']:
        print '- end time:', end_time

    solution['start_time'] = start_time
    solution['end_time'] = end_time
    solution['paths'] = paths
    solution['path'] = [int(i) for i in paths[shortest_path_index, :][0]]
    solution['vertex_weights'] = vertex_weights
    solution['cost_of_path'] = float(weights[shortest_path_index])
    solution['weights'] = weights
    solution['end_time'] = end_time
    solution['shortest_path_index'] = shortest_path_index
    solution['SOLVER'] = 'brute'

    if args['--verbose']:
        print '- index, path, weight:'
        for i in range(0, len(solution['weights'])):
            line_to_print = '\t'+str(i)+', '+str(solution['paths'][i,:])+', '+str(solution['weights'][i])
            if i in solution['shortest_path_index']:
                line_to_print = line_to_print + ' *'
            print line_to_print

    return solution
