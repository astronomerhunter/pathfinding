""" 
This technique isn't perfected yet.  Some nodes can be out of bounds.
"""
import sys
import numpy as np


def create_graph(args):

    args['GROUPS'] = int(args['GROUPS'])

    args['OFFSET_STD_DEV'] = float(args['OFFSET_STD_DEV'])

    if args['GROUPS'] > args['N']:
        raise ValueError('Invalid inputs, GROUPS > N!')

    group_centers = np.random.uniform(low = 0.0,
                            high = 1.0,
                            size = [ args['GROUPS'], 2 ] )

    which_group = np.random.randint(low=0, 
                                   high=args['GROUPS'], 
                                   size=[args['N']-args['GROUPS']])

    other_city_locations = np.zeros([len(which_group), 2])
    for index in range(0, len(which_group)):
        
        group_index = which_group[index]

        x_coord_of_group_center = group_centers[group_index, 0]
        y_coord_of_group_center = group_centers[group_index, 1]

        angle = np.random.randint(low=0, high=180) # degrees
        distance = np.random.normal(loc=0.0, scale=args['OFFSET_STD_DEV'])

        x_offset = np.cos(angle*np.pi/180.0)*distance
        y_offset = np.sin(angle*np.pi/180.0)*distance

        # TODO: make sure all cities end up wthin [0,1] in both axis

        other_city_locations[index, 0] = x_coord_of_group_center + x_offset
        other_city_locations[index, 1] = y_coord_of_group_center + y_offset

    return np.vstack((group_centers, other_city_locations))