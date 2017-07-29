import numpy as np

def create_map(args):
    return np.random.uniform(low = 0.0, 
                            high = 1.0, 
                            size = [args['N'], 2 ] )
