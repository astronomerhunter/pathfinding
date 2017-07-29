"""
description goes here
"""
import sys
import numpy as np


def create_map(args):
    '''
    necesary_keys = ['number_of_groups','number_of_nodes','std_dev_of_offset']
    if args['--map_args'].keys()
    included_keys = args.keys()
    for key in necesary_keys:
        if key not in included_keys:
            print "Missing necesary key ("+key+") in arguments for create_map()."
            sys.exit(0)
    '''
    try:
        args['GROUPS'] = int(args['GROUPS'])
    except ValueError:
        print 'GROUPS must be a integer.'
        sys.exit(1)
        # TODO: make these raise ValueError

    try:
        args['OFFSET_STD_DEV'] = float(args['OFFSET_STD_DEV'])
    except ValueError:
        print 'OFFSET_STD_DEV must be a float.'
        sys.exit(1)

    if args['GROUPS'] > args['N']:
        print "Invalid inputs, GROUPS > N!"
        sys.exit(1)

    group_centers = np.random.uniform(low = 0.0,
                            high = 1.0,
                            size = [ args['GROUPS'], 2 ] )

    which_group = np.random.randint(low=0, 
                                   high=args['GROUPS'], 
                                   size=[args['N']-args['GROUPS']])

    # assign X and Y coordinates to those remaining cities
    other_city_locations = np.zeros([len(which_group), 2])
    for index in range(0, len(which_group)):
        
        group_index = which_group[index]

        x_coord_of_group_center = group_centers[group_index, 0]
        y_coord_of_group_center = group_centers[group_index, 1]

        # get polar coordinates of this cities location ofset from group HQ
        angle = np.random.randint(low=0, high=180) # degrees
        distance = np.random.normal(loc=0.0, scale=args['OFFSET_STD_DEV'])

        # convert polar offset to cartesian (=X,Y) offset
        x_offset = np.cos(angle*np.pi/180.0)*distance
        y_offset = np.sin(angle*np.pi/180.0)*distance

        # TODO: make sure all cities end up wthin [0,1] in both axis

        other_city_locations[index, 0] = x_coord_of_group_center + x_offset
        other_city_locations[index, 1] = y_coord_of_group_center + y_offset

    return np.vstack((group_centers, other_city_locations))