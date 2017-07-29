# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------- #
import numpy as np

# -------------------------------------------------------------------------------------- #
def create_map(args):

    try:
        args['X_PEAKS'] = int(args['X_PEAKS'])
        args['Y_PEAKS'] = int(args['Y_PEAKS'])
    except ValueError:
        print 'X_PEAKS and Y_PEAKS must be a integers.'
        sys.exit(1)
        # TODO: make these raise ValueError


    node_locations = np.zeros([args['N'],2])

    x_function_input = np.linspace(0,
                                 np.pi*args['X_PEAKS'], 
                                 args['N'])
    node_locations[:,0] = np.random.choice(x_function_input,
                                size=args['N'],
                                p=np.sin(x_function_input)**2/np.sum(np.sin(x_function_input)**2))

    y_function_input = np.linspace(0,
                                 np.pi*args['Y_PEAKS'],
                                 args['N'])
    node_locations[:,1] = np.random.choice(y_function_input,
                                size=args['N'],
                                p=np.sin(y_function_input)**2/np.sum(np.sin(y_function_input)**2))
    
    # normalize
    node_locations[:,0] = node_locations[:,0]/np.max(node_locations[:,0])
    node_locations[:,1] = node_locations[:,1]/np.max(node_locations[:,1])

    return node_locations



# -------------------------------------------------------------------------------------- #