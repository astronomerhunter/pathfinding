"""
Creates an X and Y location for each of N nodes using the given placement technique.  Some
placement techniques require more parameters than others.  Below, required parameters are
represented by capital letters.  Note their order.

Usage:
    create_graph.py random_uniform N [--save | --save --display]
    create_graph.py ball N [--save | --save --display]
    create_graph.py donut N [--save | --save --display]
    create_graph.py fixed_number_of_groups N GROUPS OFFSET_STD_DEV [--save | --save --display]
    create_graph.py sinusoidal N X_PEAKS Y_PEAKS [--save | --save --display]
    create_graph.py -h
    create_graph.py --help
    create_graph.py --version

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
from docopt import docopt

from functions import complex as cmplx

def save_graph(node_locations, node_metadata):
    """
    For a graph with graph_id, node_locations is saved as plain text along 
    data/graphs/<graph_id>/<graph_id>.txt and the metadata is saved as a JSON
    along data/graphs/<graph_id>/<graph_id>_meta.txt.
    """
    graph_save_path, meta_save_path = cmplx.get_filepath_to_graph_data(node_metadata['graph_id'])

    path_to_test_existance = cmplx.get_filepath_to_repo()
    folders_to_generate = ['data', 'graphs', node_metadata['graph_id']]
    for folder in folders_to_generate:
        if os.path.exists(path_to_test_existance+os.path.sep+folder) is False:
            os.mkdir(path_to_test_existance+os.path.sep+folder)
        path_to_test_existance = path_to_test_existance + os.path.sep + folder

    print('- saving node_locations as text file @', graph_save_path)
    try:
        np.savetxt(graph_save_path, node_locations)
    except Exception as e:
        print('ERROR saving nodegraph txt file')
        print('- exact Python error:', e)
        sys.exit(1)

    print('- saving node_metadata as JSON @ '+meta_save_path)
    try:
        with open(meta_save_path, 'w') as outfile:
            json.dump(node_metadata, outfile)
    except Exception as e:
        print('ERROR saving graphMeta JSON file')
        print('- exact Python error:', e)
        sys.exit(1)


def generate_static_PNG_of_graph(node_locations, node_metadata):
    x = node_locations[:, 0]
    y = node_locations[:, 1]

    plt.scatter(x, y)

    PLOT_MARGIN = 0.1
    xLowerLimit = 0 - PLOT_MARGIN
    xUpperLimit = 1 + PLOT_MARGIN
    yLowerLimit = 0 - PLOT_MARGIN
    yUpperLimit = 1 + PLOT_MARGIN

    plt.xlim([xLowerLimit,xUpperLimit])
    plt.ylim([yLowerLimit,yUpperLimit])

    plt.xlabel('p_1 value')
    plt.ylabel('p_2 value')
    plt.title('graph of {} ({})'.format(node_metadata['graph_id'], node_metadata['technique']))

    path_to_node_loc, path_to_meta_data = cmplx.get_filepath_to_graph_data(node_metadata['graph_id'])
    path_to_png = path_to_node_loc[:-4] + '_static.png'
    plt.savefig(path_to_png)
    print('Saved a .png file @', path_to_png)


def make_graph(args):
    """
    Imports the required file, access its create_graph() function and
    builds the node_locations and node_metadata variables.
    """
    try:    
        temp_resource = __import__(
            'graph_creation.'+args['TECHNIQUE'],
            globals(), 
            locals(), 
            ['graph_creation']
        )
    except ImportError:
        print('err')
        raise ImportError

    node_locations = temp_resource.create_graph(args)
    print('INFO: node_locations created succesfully.')
    
    graph_id = cmplx.generate_ID('GID', 5)
    print('- graph_ID: '+ graph_id)
    
    node_metadata = {
        "graph_id" : graph_id,
        'technique': args['TECHNIQUE'],
        "number_of_nodes" : args['N']
    }
    if args['--save'] is True:
        save_graph(node_locations, node_metadata)
        if args['--display'] is True:
            generate_static_PNG_of_graph(node_locations, node_metadata)
    else:
        print('INFO: Not saving results.')

    return 0, node_metadata, node_locations


if __name__ == "__main__":

    cli_arguments = docopt(__doc__, version='Create graph 1.0')
    cli_arguments['TECHNIQUE'] = sys.argv[1]

    try:
        cli_arguments['N'] = int(cli_arguments['N'])
    except ValueError:
        print('N must be an integer.')
        sys.exit(1)

    make_graph(cli_arguments)
