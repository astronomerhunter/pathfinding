"""
USAGE: Type python create_map.py -h for useage information.
"""
# -------------------------------------------------------------------------------------- #
# This script performs a TSP solution on a map.  If you provide it with the map_ID of an
# existing map, it will attempt to find the shortest path of that map.  If not, it will
# create a map using the configuration parameters in a config file.
#
# This script is most simply called by:
#    $ python execute.py
# The above command line command will draw parameters from the configuration file at
# tsp/config/execute/paramteres.config.  Additionally, the configuration parameters can
# be passed directly into the command line command via something like:
#    $ python execute.py '{"alg": "brute"}'
# The above technique might be useful for creating a wrapper script to solve many maps
# with many algorithums.
# -------------------------------------------------------------------------------------- #
import numpy as np
import json
from functions import complex as cmplx
import create_map
import sys
import ast



# -------------------------------------------------------------------------------------- #
def load_map(map_ID):
    # This function attempts to load a cityMap from 
    # "tsp/data/hist/<map_ID>/<map_ID>_locations.txt".
    #
    #     INPUTS:
    #        - map_ID: string representing the map indetifier to load
    #     OUTPUTS:
    #        - cityMap: [nCities,2] sized where 1st column is X coordindate
    #                   and 2nd column is Y cordinate for each city
    #        - mapMeta: dictionary containing metadata about cityMap
    #
    print ' INFO: Attempting to load map.'
    print '\t- map_ID:', map_ID
    mapLoadPath, metaLoadPath = cmplx.get_filepath_to_map_data(map_ID)
    
    print '\t- loading map from '+mapLoadPath
    try:
        cityMap = np.loadtxt(mapLoadPath)
    except Exception as e:
        print '\n ERROR: opening map locaiton data.'
        print '\t exact python error:',str(e)
        print '\n'
        cityMap = None
        
    print '\t- loading meta from '+metaLoadPath
    try:
        with open(metaLoadPath, 'r') as infile:
            meta_data_string = infile.read()
            mapMeta = ast.literal_eval(meta_data_string)
    except Exception as e:
        print '\n ERROR: opening map meta data.'
        print '\t exact python error:',str(e)
        print '\n'
        mapMeta = None

    return cityMap, mapMeta



def print_detail_solution(alg, solution):
    # Simply prints a more detailed view of the solution.
    # 
    if alg == 'brute':
        print '\t\t index, path, distance:'
        for i in range(0, len(solution['distances'])):
            lineToPrint = '\t\t\t'+str(i)+', '+str(solution['paths'][i,:])+', '+str(solution['distances'][i])
            if i in solution['shortest_path_index']:
                lineToPrint = lineToPrint + ' *'
            print lineToPrint
    elif alg == 'greedy':
        print "\t\t- print_detail_solution(alg='greedy') isn't built yet"
    else:
        print "\t\t- Unrecognized alg argument in print_detail_solution()"



def print_quick_solution(alg, solution):
    # Simply prints the fastest routes.
    #
    if alg == 'brute':
        for entry in solution['shortest_path_index']:
            print '\t\t', solution['paths'][entry]
    elif alg =='greedy':
        print "\t\t- print_quick_solution(alg='greedy') isn't built yet"
    else:
        print "\t\t- Unrecognized alg argument in print_quick_solution()"



def save_solution(saveMethod, solution):
    # This function saves a solution by saving solution,a python dictionary,
    # as ether raw text files, a JSON, or a numpy compressed pickled file.
    #
    saveMethodTypes = ['json']
    try:
        assert saveMethod in saveMethodTypes
        assert type(solution) == type({})
    except:
        print '\n ERROR: improper inputs into save_solution():'
        print '\t- saveMethod should be string, is ', type(saveMethod)
        print '\t- solution should be dictionary, is', type(solution)
        print '\n'
        return None

    filePathPrefix = cmplx.get_filepath_to_solution_data(solution['map_ID'],solution['sol_ID'])

    if saveMethod == 'json':
        try:
            for key in solution.keys():
                if type(solution[key]) == type(np.zeros([10,10])):
                    solution[key] = solution[key].tolist()
            with open(filePathPrefix, 'w') as outfile:
                json.dump(solution,outfile)
            print ' INFO: solution saved as json file'
            print '\t- @ '+filePathPrefix
        except Exception as e:
            print '\n ERROR: unable to save solution as json'
            print '\t- @ '+filePathPrefix
            print '\t- exact Python error:',str(e)
            print '\n'
            return None

    else:
        print '\n ERROR: save_method not recognized. Skipping save'
        print '\t- acceptable formats:',saveMethodTypes
        print '\t- input format:',saveMethod
        print '\n'
        return None



# -------------------------------------------------------------------------------------- #
def main(configParams):

    # see if we can load the map data
    if 'map_ID' in configParams and configParams['map_ID'] != '':
        cityMap, mapMeta = load_map(configParams['map_ID'])
        
    # or if we need to create it
    else:
        print ' INFO: Creating map...'
        create_map_configParams = cmplx.get_config_params('map_creation')
        cityMap, mapMeta = create_map.process_to_create_map(create_map_configParams)

    # import solver
    try:
        # name the solver module 'temp_resource'
        temp_resource = __import__('algs.'+configParams['alg'],
                                   globals(), locals(), ['algs'], -1)
    except ImportError:
        print 'Unable to import solver for algorithm named '+configParams['alg']
        sys.exit(1)

    # solve
    solution = temp_resource.solve(configParams, cityMap, mapMeta)

    # create solution ID and add to solution dictionary
    solution['sol_ID'] = cmplx.generate_ID('SID', 5)
    solution['map_ID'] = mapMeta['map_ID']

    # print solution
    if solution is not None:
        print ' INFO: solve() complete.'
        # if there arent that many cities, the solution is relatively short, so print it
        if mapMeta['number_of_cities'] < 5:
            print '\t- detailed solution:'
            print_detail_solution(configParams['alg'],solution)
        # else, there is a long solution so just print a summary
        else:
            print '\t- quick solution:'
            print_quick_solution(configParams['alg'],solution)
    # hopefully solver returned not None
    else:
        print '\n ERROR: solution is None. Something went wrong... did you check the alg file?'
        print '\n'
        sys.exit(1)

    # save solution if applicable
    if 'save_method' in configParams and configParams['save_method'] != '':
        save_solution(configParams['save_method'], solution)
    else:
        print ' INFO: "save_method" not in configParams so solution will not be saved'

    print 'INFO: Ending script...\n'


# -------------------------------------------------------------------------------------- #	
if __name__ == "__main__":
    helpOptions = ['-h','--h','-help','--help']
    if any((True for x in helpOptions if x in sys.argv)) or len(sys.argv) == 1:
        # TODO: lets rewrite this guy
        print
        print 'INFO:'
        print '\tThis script executes a TSP path finding algorithm on a set of coords'
        print '\tgenerated by create_map.py.  Available algs are located at'
        print '\ttsp/src/algs/*.py . Feel free to add some!'
        print 'USE:'
        print '\tParameters serve as input to various solver techniques. Parameters are'
        print '\tpassed via the command line or can be set in a config file located at'
        print '\ttsp/config/execute/parameters.congif . Use the command "python execute.py"'
        print '\tor "python execute.py --config" to solve a map using the params in the config file'
        print '\tParameters can also be passed into the script via the command line by using'
        print """\t"python execute.py '{"alg":"brute"}'"""
        print '\tNote the single quotes encasing the JSON formatted parameters!'
        print
        print 'PARAMETERS:'
        print '\tFormat is "key": example_value (data type) [condition]. Indention shows condition too.'
        print '\t"map_ID": "MID00000" (string, "MID"+NNNNN)'
        print '\t"save_method": "json" (currently only "json" accepted)'
        print '\t"alg": "brute"'
        print '\t"alg": "greedy"'
        print
        print 'SAMPLE COMMAND:'
        print """\tNOT WRITTEN YET """
        print
        sys.exit(0)
    else:
        print '\n INFO: Begining script.'
        if sys.argv[1] == '--config':
            # command looks like: $ python execute.py config
            configParams = cmplx.get_config_params('execute')
        else:
            # command looks like: $ python execute.py '{"alg":"brute"}'
            try:
                configParams = json.loads(sys.argv[1])
                print ' INFO: Got configParams from command line arguments'
            except Exception as e:
                print '\n ERROR: Unable to load configuration parameters as JSON. Try...'
                print '''     $ python execute.py '{"alg":"brute"}' '''
                print ' Exact Python error: '+str(e)
                print '\n'
                sys.exit(1)
        main(configParams)
