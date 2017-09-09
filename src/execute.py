"""
Write me

Usage:
    execute.py brute MAP_ID [--save | --save --gif] [--verbose] [--force]
    execute.py nearest_neighbor MAP_ID [--save | --save --gif] [--verbose]
    execute.py random_neighbor MAP_ID [--save | --save --gif] [--verbose]
    execute.py -h
    execute.py --help
    execute.py --version

Options:
  -h --help     Show this screen.
  -s --save     Include if you would like to save script output.
  -g --gif      Requires "--save", creates a .gif of the solution.
  -f --force    Ignore all warnings about lengthy runtimes. 
  -v --verbose  Print the entire solution data.
  --version     Show version.
"""
import os
import numpy as np
import json
import create_map
from docopt import docopt
import sys
import ast # used to open node_metadata files
import matplotlib.pylab as plt
from functions import complex as cmplx
from functions import simple as smpl


def load_map(map_id):
    """
    This function attempts to load a node_locations from /data/hist/<map_ID>/<map_ID>_locations.txt
    """
    map_load_path, meta_load_path = cmplx.get_filepath_to_map_data(map_id)

    print '- loading map from '+map_load_path
    try:
        node_locations = np.loadtxt(map_load_path)
    except Exception as e:
        print 'ERROR: opening map locaiton data.'
        print 'exact python error:',str(e)
        sys.exit(1)
        
    print '- loading meta from '+meta_load_path
    try:
        with open(meta_load_path, 'r') as in_file:
            meta_data_string = in_file.read()
            node_metadata = ast.literal_eval(meta_data_string)
    except Exception as e:
        print 'ERROR: opening map meta data.'
        print 'exact python error:', str(e)
        sys.exit(1)
    return node_locations, node_metadata


def make_gif(args, solution, node_locations, node_metadata):
    """
    description
    """

    # plot the nodes as blue dots
    x = node_locations[:, 0]
    y = node_locations[:, 1]

    plt.scatter(x, y)

    xLowerLimit = min(x) - 0.10*(np.abs(max(x)-min(x)))
    xUpperLimit = max(x) + 0.10*(np.abs(max(x)-min(x)))
    yLowerLimit = min(y) - 0.10*(np.abs(max(y)-min(y)))
    yUpperLimit = max(y) + 0.10*(np.abs(max(y)-min(y)))
    plt.xlim([xLowerLimit,xUpperLimit])
    plt.ylim([yLowerLimit,yUpperLimit])

    plt.xlabel('p_1 value')
    plt.ylabel('p_2 value')
    plt.title('{} ({}) {} ({})'.format(node_metadata['technique'], node_metadata['map_id'], solution['SOLVER'], solution['sol_id']))


    if args['--verbose']:
        progress_bar = [0]*10
        print 'Starting process to make individual .png files.'

    path_to_sol = cmplx.get_filepath_to_solution_data(node_metadata['map_id'],
                                                      solution['sol_id'])
    path_to_sol = smpl.filepath_string_to_list(path_to_sol)[:-1]
    path_to_gif_folder = smpl.filepath_list_to_string(path_to_sol) + os.path.sep
    if os.path.exists(path_to_gif_folder) is False:
        os.mkdir(path_to_gif_folder)
        
    list_of_still_paths = []
    x = node_locations[:,0]
    y = node_locations[:,1]

    # make individual .png files
    for i in range(0, len(solution['path'])-1):
        origin_index = solution['path'][i]
        destination_index = solution['path'][i+1]
        x_1 = x[origin_index]
        y_1 = y[origin_index]
        x_2 = x[destination_index]
        y_2 = y[destination_index]
        plt.plot([x_1, x_2],[y_1, y_2], 'k')

        # make sure we add leading 0's before numbers that have less digits than others
        if len(str(i)) != len(str(node_metadata['number_of_nodes']-1)):
            max_numb_digits = len(str(node_metadata['number_of_nodes']-1))
            this_numb_digits = len(str(i))
            n_missing_digits = max_numb_digits - this_numb_digits
            index_string = '0'*n_missing_digits + str(i)
        else:
            index_string = str(i)
                    
        still_file_path = path_to_gif_folder+'frame'+index_string+'.png'
        plt.savefig(still_file_path)
        list_of_still_paths.append(still_file_path)
        if args['--verbose']:
            cmplx.print_progress_bar(progress_bar, i, len(solution['path'])-1)

    # assemble individual .png images into a gif
    if args['--verbose']:
        print 'Starting process to combine .png files into .gif.  This will take a while.'
    try:
        gif_save_path = path_to_gif_folder+'animated_solution.gif'
        import imageio
        images = []
        for filename in list_of_still_paths:
            images.append(imageio.imread(filename))
            imageio.mimsave(gif_save_path, images)
        print '- .gif saved @',gif_save_path
        print '- HINT: To view the .gif file on Mac OSX, select it in finder then press space bar key'
    except Exception as e:
        print 'ERROR: Ran into an issue creating GIF.'
        print '- Exact Python error:', e

    plt.close()

def save_solution(solution):
    """
    Saves script output.
    """
    file_path_prefix = cmplx.get_filepath_to_solution_data(solution['map_id'], solution['sol_id'])
    print 'Attempting to save solution @ '+file_path_prefix
    try:
        for key in solution.keys():
            if type(solution[key]) == type(np.zeros([10,10])):
                solution[key] = solution[key].tolist()
        with open(file_path_prefix, 'w') as outfile:
            json.dump(solution,outfile)
        print 'INFO: solution saved as json file'
    except Exception as e:
        print 'ERROR: unable to save solution as json'
        print '- exact Python error:',str(e)


def apply_solver(args):

    node_locations, node_metadata = load_map(args['MAP_ID'])

    try:
        temp_resource = __import__('solvers.'+args['SOLVER'],
                                   globals(), locals(), ['solvers'], -1)
    except ImportError:
        print 'Unable to import solver for algorithm named '+args['SOLVER']
        sys.exit(1)

    solution = temp_resource.solve(args, node_locations, node_metadata)

    solution['sol_id'] = cmplx.generate_ID('SID', 5)
    solution['map_id'] = node_metadata['map_id']

    if args['--save']:
        save_solution(solution)
        if args['--gif']:
            make_gif(args, solution, node_locations, node_metadata)
    else:
        print 'INFO: Not saving results.'

    return 0, solution


if __name__ == "__main__":
    cli_arguments = docopt(__doc__, version='Execute 1.0')
    cli_arguments['SOLVER'] = sys.argv[1]
    apply_solver(cli_arguments)