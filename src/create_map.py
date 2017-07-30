"""
Creates an X and Y location for each of N nodes using the given placement technique.  Some
placement techniques require more parameters than others.  Below, required parameters are
represented by capital letters.  Note their order.

Usage:
    create_map.py random_uniform N [--save | --save --display]
    create_map.py ball N [--save | --save --display]
    create_map.py donut N [--save | --save --display]
    create_map.py fixed_number_of_groups N GROUPS OFFSET_STD_DEV [--save | --save --display]
    create_map.py sinusoidal N X_PEAKS Y_PEAKS [--save | --save --display]
    create_map.py -h
    create_map.py --help
    create_map.py --version

Options:
  -h --help     Show this screen.
  -s --save     Include if you would like to save a file with the script output.
  -d --display  Requires "--save" option, include if you would like to generate a .png file of the output.
  --version     Show version.

"""
import sys
import os
import json
import matplotlib.pylab as plt
import numpy as np
from functions import complex as cmplx
from docopt import docopt


def save_map(node_locations, node_metadata):
    """
    For a map with map_id, node_locations is saved as plain text along 
    data/maps/<map_id>/<map_id>.txt and the metadata is saved as a JSON
    along data/maps/<map_id>/<map_id>_meta.txt.  The metadata is done this
    way because I haven't found an easy way to save 2+ dimensional arrays 
    as a serializable JSON yet.  TODO: fix that ish.
    """
    map_save_path, meta_save_path = cmplx.get_filepath_to_map_data(node_metadata['map_id'])

    path_to_test_existance = cmplx.get_filepath_to_repo()
    folders_to_generate = ['data', 'maps', node_metadata['map_id']]
    for folder in folders_to_generate:
        if os.path.exists(path_to_test_existance+os.path.sep+folder) is False:
            os.mkdir(path_to_test_existance+os.path.sep+folder)
        path_to_test_existance = path_to_test_existance + os.path.sep + folder

    print '- saving node_locations as text file @ '+map_save_path
    try:
        np.savetxt(map_save_path, node_locations)
    except Exception as e:
        print 'ERROR saving nodeMap txt file'
        print '- exact Python error:', e
        sys.exit(1)

    print '- saving node_metadata as JSON @ '+meta_save_path
    try:
        with open(meta_save_path, 'w') as outfile:
            json.dump(node_metadata, outfile)
    except Exception as e:
        print 'ERROR saving mapMeta JSON file'
        print '- exact Python error:', e
        sys.exit(1)


def generate_static_PNG_of_map(node_locations, node_metadata):
    """
    some description
    """
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
    plt.title('Parameter values for '+node_metadata['map_id'])

    path_to_node_loc, path_to_meta_data = cmplx.get_filepath_to_map_data(node_metadata['map_id'])
    path_to_png = path_to_node_loc[:-4] + '_static.png'
    plt.savefig(path_to_png)
    print 'Saved a .png file @', path_to_png


def make_map(args):
    """
    Imports the required file, access its create_map() function and
    builds the node_locations and node_metadata variables.
    """
    try:    
        temp_resource = __import__('map_creation.'+args['TECHNIQUE'],
                               globals(), locals(), ['map_creation'], -1)
    except ImportError:
        print 'Unable to import node placement techinque for '+args['TECHNIQUE']
        sys.exit(1)

    node_locations = temp_resource.create_map(args)
    print 'INFO: node_locations created succesfully.'
    
    # TODO: ensure this is unique by checking folder to see if ID exists
    map_id = cmplx.generate_ID('MID', 5)
    print '- map_ID: '+ map_id
    
    node_metadata = {"map_id" : map_id,
                     "number_of_nodes" : args['N']}

    if args['--save'] is True:
        save_map(node_locations, node_metadata)
        if args['--display'] is True:
            generate_static_PNG_of_map(node_locations, node_metadata)
    else:
        print 'INFO: Not saving results.'

    return 0


if __name__ == "__main__":

    cli_arguments = docopt(__doc__, version='Create Map 1.0')
    cli_arguments['TECHNIQUE'] = sys.argv[1]

    try:
        cli_arguments['N'] = int(cli_arguments['N'])
    except ValueError:
        print 'N must be an integer.'
        sys.exit(1)

    make_map(cli_arguments)
