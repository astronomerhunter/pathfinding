from create_map import make_map as module

if __name__ == '__main__':
    """
    create_map.py -h
    create_map.py --help
    create_map.py random_uniform N [--save-map]
    create_map.py ball N [--save-map]
    create_map.py donut N [--save-map]
    create_map.py fixed_number_of_groups N GROUPS OFFSET_STD_DEV [--save-map] 
    create_map.py sinusoidal N X_PEAKS Y_PEAKS [--save-map]
    create_map.py --version

    {'--help': False,
    '--save-map': False,
    '--version': False,
    'GROUPS': None,
    'N': 15,
    'OFFSET_STD_DEV': None,
    'TECHNIQUE': 'ball',
    'X_PEAKS': None,
    'Y_PEAKS': None,
    'ball': True,
    'donut': False,
    'fixed_number_of_groups': False,
    'random_uniform': False,
    'sinusoidal': False}
    
    """
    print 'TESTING:  python create_map.py random_uniform 15'
    assert 0 == module({'--help': False,
                        '--save-map': False,
                        '--version': False,
                        'GROUPS': None,
                        'N': 15,
                        'OFFSET_STD_DEV': None,
                        'TECHNIQUE': 'random_uniform',
                        'X_PEAKS': None,
                        'Y_PEAKS': None,
                        'ball': False,
                        'donut': False,
                        'fixed_number_of_groups': False,
                        'random_uniform': True,
                        'sinusoidal': False})
    print 'TESTING:  python create_map.py random_uniform 15 --save-map'
    assert 0 == module({'--help': False,
                        '--save-map': True,
                        '--version': False,
                        'GROUPS': None,
                        'N': 15,
                        'OFFSET_STD_DEV': None,
                        'TECHNIQUE': 'random_uniform',
                        'X_PEAKS': None,
                        'Y_PEAKS': None,
                        'ball': False,
                        'donut': False,
                        'fixed_number_of_groups': False,
                        'random_uniform': True,
                        'sinusoidal': False})
    
    print 'TESTING:  python create_map.py ball 15'
    assert 0 == module({'--help': False,
                        '--save-map': False,
                        '--version': False,
                        'GROUPS': None,
                        'N': 15,
                        'OFFSET_STD_DEV': None,
                        'TECHNIQUE': 'ball',
                        'X_PEAKS': None,
                        'Y_PEAKS': None,
                        'ball': True,
                        'donut': False,
                        'fixed_number_of_groups': False,
                        'random_uniform': False,
                        'sinusoidal': False})
    print 'TESTING:  python create_map.py ball 15 --save-map'
    assert 0 == module({'--help': False,
                        '--save-map': True,
                        '--version': False,
                        'GROUPS': None,
                        'N': 15,
                        'OFFSET_STD_DEV': None,
                        'TECHNIQUE': 'ball',
                        'X_PEAKS': None,
                        'Y_PEAKS': None,
                        'ball': True,
                        'donut': False,
                        'fixed_number_of_groups': False,
                        'random_uniform': False,
                        'sinusoidal': False})

    print 'TESTING:  python create_map.py donut 15'
    assert 0 == module({'--help': False,
                        '--save-map': False,
                        '--version': False,
                        'GROUPS': None,
                        'N': 15,
                        'OFFSET_STD_DEV': None,
                        'TECHNIQUE': 'donut',
                        'X_PEAKS': None,
                        'Y_PEAKS': None,
                        'ball': False,
                        'donut': True,
                        'fixed_number_of_groups': False,
                        'random_uniform': False,
                        'sinusoidal': False})
    print 'TESTING:  python create_map.py donut 15 --save-map'
    assert 0 == module({'--help': False,
                        '--save-map': True,
                        '--version': False,
                        'GROUPS': None,
                        'N': 15,
                        'OFFSET_STD_DEV': None,
                        'TECHNIQUE': 'donut',
                        'X_PEAKS': None,
                        'Y_PEAKS': None,
                        'ball': False,
                        'donut': True,
                        'fixed_number_of_groups': False,
                        'random_uniform': False,
                        'sinusoidal': False})

    print 'TESTING:  python create_map.py fixed_number_of_groups 15 5 0.10'
    assert 0 == module({'--help': False,
                        '--save-map': False,
                        '--version': False,
                        'GROUPS': '5',
                        'N': 15,
                        'OFFSET_STD_DEV': '0.10',
                        'TECHNIQUE': 'fixed_number_of_groups',
                        'X_PEAKS': None,
                        'Y_PEAKS': None,
                        'ball': False,
                        'donut': False,
                        'fixed_number_of_groups': True,
                        'random_uniform': False,
                        'sinusoidal': False})
    print 'TESTING:  python create_map.py fixed_number_of_groups 15 5 0.10 --save-map'
    assert 0 == module({'--help': False,
                        '--save-map': True,
                        '--version': False,
                        'GROUPS': '5',
                        'N': 15,
                        'OFFSET_STD_DEV': '0.10',
                        'TECHNIQUE': 'fixed_number_of_groups',
                        'X_PEAKS': None,
                        'Y_PEAKS': None,
                        'ball': False,
                        'donut': False,
                        'fixed_number_of_groups': True,
                        'random_uniform': False,
                        'sinusoidal': False})



    print 'TESTING:  python create_map.py sinusoidal 15 3 3'
    assert 0 == module({'--help': False,
                        '--save-map': False,
                        '--version': False,
                        'GROUPS': None,
                        'N': 15,
                        'OFFSET_STD_DEV': None,
                        'TECHNIQUE': 'sinusoidal',
                        'X_PEAKS': '3',
                        'Y_PEAKS': '3',
                        'ball': False,
                        'donut': False,
                        'fixed_number_of_groups': False,
                        'random_uniform': False,
                        'sinusoidal': True})
    print 'TESTING:  python create_map.py sinusoidal 15 3 3 --save-map'
    assert 0 == module({'--help': False,
                        '--save-map': True,
                        '--version': False,
                        'GROUPS': None,
                        'N': 15,
                        'OFFSET_STD_DEV': None,
                        'TECHNIQUE': 'sinusoidal',
                        'X_PEAKS': '3',
                        'Y_PEAKS': '3',
                        'ball': False,
                        'donut': False,
                        'fixed_number_of_groups': False,
                        'random_uniform': False,
                        'sinusoidal': True})

    pretty_string = 'All test cases passed.'
    print '!' * (len(pretty_string) + 4)
    print '! '+pretty_string+' !'
    print '!' * (len(pretty_string) + 4)
