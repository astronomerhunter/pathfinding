from execute import apply_solver as module
from create_map import make_map as module


if __name__ == '__main__':
    # make a map to solve on
    assert 0 == module({'--help': False,
                        '--save': True,
                        '--version': False,
                        'GROUPS': None,
                        'N': 10,
                        'OFFSET_STD_DEV': None,
                        'TECHNIQUE': 'random_uniform',
                        'X_PEAKS': None,
                        'Y_PEAKS': None,
                        'ball': False,
                        'donut': False,
                        'fixed_number_of_groups': False,
                        'random_uniform': True,
                        'sinusoidal': False})
    


    pretty_string = 'All test cases passed.'
    print '!' * (len(pretty_string) + 4)
    print '! '+pretty_string+' !'
    print '!' * (len(pretty_string) + 4)
