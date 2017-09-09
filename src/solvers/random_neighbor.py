import numpy as np
import time
import sys
from . import nearest_neighbor

def chose_next_node_to_visit(args, current_node_index, vertex_weights):
    """
    This function randomly selects an unvisited node to travel to next.
    """
    available_node_indicies = np.where(vertex_weights[current_node_index] != np.inf)[0]
    if len(available_node_indicies) is not 1:
        randomly_chosen_index = np.random.randint(0, len(available_node_indicies))
        nearest_node_index = available_node_indicies[randomly_chosen_index]
    else:
        nearest_node_index = available_node_indicies
    return int(nearest_node_index)


def solve(args, node_locations, node_metadata):
    """
    Because this algorithm differs from nearest_neighbor only in how it selects the
    next node to travel to, we replace the hose_next_node_to_visit() function
    in nearest_neighbor.py and then reuse its solve() function.
    """
    # Rewrite external (nearest_neighbor.py) function with internal (random_neighbor.py) function
    nearest_neighbor.chose_next_node_to_visit = chose_next_node_to_visit
    solution = nearest_neighbor.solve(args, node_locations, node_metadata)
    solution['SOLVER'] = 'random_neighbor'
    return solution