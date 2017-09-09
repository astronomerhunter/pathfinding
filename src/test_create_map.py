from create_map import make_map
import copy

if __name__ == '__main__':
    empty_cli_arguments = {'--help': False,
                            '--save': False,
                            '--version': False,
                            '--display': False,
                            'GROUPS': None,
                            'N': 15,
                            'OFFSET_STD_DEV': None,
                            'TECHNIQUE': '',
                            'X_PEAKS': None,
                            'Y_PEAKS': None,
                            'ball': False,
                            'donut': False,
                            'fixed_number_of_groups': False,
                            'random_uniform': False,
                            'sinusoidal': False}
        
    temp = copy.deepcopy(empty_cli_arguments)
    print 'TESTING:  python create_map.py random_uniform 15'
    temp['TECHNIQUE'] = 'random_uniform'
    temp['random_uniform'] = True
    assert make_map(temp)[0] == 0
    print 'TESTING:  python create_map.py random_uniform 15 --save'
    temp['--save'] = True
    assert make_map(temp)[0] == 0

    temp = copy.deepcopy(empty_cli_arguments)
    print 'TESTING:  python create_map.py ball 15'
    temp['TECHNIQUE'] = 'ball'
    temp['ball'] = True
    assert make_map(temp)[0] == 0
    print 'TESTING:  python create_map.py ball 15 --save'
    temp['--save'] = True
    assert make_map(temp)[0] == 0

    temp = copy.deepcopy(empty_cli_arguments)
    print 'TESTING:  python create_map.py donut 15'
    temp['TECHNIQUE'] = 'donut'
    temp['donut'] = True
    assert make_map(temp)[0] == 0
    print 'TESTING:  python create_map.py donut 15 --save'
    temp['--save'] = True
    assert make_map(temp)[0] == 0

    temp = copy.deepcopy(empty_cli_arguments)
    print 'TESTING:  python create_map.py fixed_number_of_groups 15 5 0.1'
    temp['TECHNIQUE'] = 'fixed_number_of_groups'
    temp['fixed_number_of_groups'] = True
    temp['GROUPS'] = '5'
    temp['OFFSET_STD_DEV'] = '0.1'
    assert make_map(temp)[0] == 0
    print 'TESTING:  python create_map.py fixed_number_of_groups 15 5 0.1 --save'
    temp['--save'] = True
    assert make_map(temp)[0] == 0

    temp = copy.deepcopy(empty_cli_arguments)
    print 'TESTING:  python create_map.py sinusoidal 15 3 3'
    temp['TECHNIQUE'] = 'sinusoidal'
    temp['sinusoidal'] = True
    temp['X_PEAKS'] = '3'
    temp['Y_PEAKS'] = '3'
    assert make_map(temp)[0] == 0
    print 'TESTING:  python create_map.py fixed_number_of_groups 15 3 3 --save'
    temp['--save'] = True
    assert make_map(temp)[0] == 0


    pretty_string = 'All test cases passed.'
    print '!' * (len(pretty_string) + 4)
    print '! '+pretty_string+' !'
    print '!' * (len(pretty_string) + 4)
