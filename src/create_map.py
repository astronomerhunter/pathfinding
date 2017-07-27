"""
USAGE: Type python create_map.py -h for useage information.
"""
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------- #
# This function creates a map of nodes to visit.  The properties of that map draw from a
# configuration file at /config/map_config.json.  If the number of nodes
# is small enough, their locations are printed out by this function.
#
# Please use with Python 2.7
#
# Created by Hunter Brooks on 7/12/2016.
# -------------------------------------------------------------------------------------- #
import numpy as np
import json
from functions import complex as cmplx
import sys
import os


# -------------------------------------------------------------------------------------- #
def make_meta(configParams, map_ID):
    # This function returns a dictionary that makes up the metadata.
    return { "map_ID" : map_ID,
             "number_of_nodes" : configParams['number_of_nodes']}


def save_map(nodeMap, mapMeta):
    # This function creates a map ID and saves the map to "data/maps/<map_ID>/<map_ID>_locations.txt".
    # It also saves metadata at "data/maps/<map_ID>/<map_ID>_meta.txt".
    #
    # INPUTS:
    #    -nodeMap:	2d array of x and y locations of each city.
    #	 -mapMeta	dict containing meta data about map, like map_ID
    # OUTPUTS:
    #    -nothing is returned
    #
    map_ID = mapMeta['map_ID']
    mapSavePath, metaSavePath = cmplx.get_filepath_to_map_data(map_ID)
    print '\t- saving nodeMap as text file @ '+mapSavePath

    pathToTestExistance = cmplx.get_filepath_to_repo()
    foldersToMake = ['data','maps',map_ID]
    for index in range(0, len(foldersToMake)):
        folderToAdd = foldersToMake[index]
        if os.path.exists(pathToTestExistance+os.path.sep+folderToAdd) == False:
            os.mkdir(pathToTestExistance+os.path.sep+folderToAdd)
        pathToTestExistance = pathToTestExistance + os.path.sep + folderToAdd

    try:
        np.savetxt(mapSavePath, cityMap)
    except Exception as e:
        print
        print ' ERROR saving nodeMap txt file'
        print '\t- attempted to save @', mapSavePath
        print '\t- exact Python error:', e
        print
        sys.exit(1)

    print '\t- saving mapMeta as JSON @ '+metaSavePath
    try:
        with open(metaSavePath, 'w') as outfile:
            json.dump(mapMeta, outfile)
    except Exception as e:
        print
        print ' ERROR saving mapMeta JSON file'
        print '\t- attempted to save @', metaSavePath
        print '\t- exact Python error:', e
        print
        sys.exit(1)



def process_to_create_map(configParams):
    # The purpose of this function is to create a map based on 
    # configParams['city_placement_technique'] for configParams['number_of_cities']
    # cities. It does this by finding the "<configParams['city_placement_technique']>.py" 
    # in tsp/src/map_creation/ and calling its create_cityMap() function.
    # 
    # INPUTS:
    #     -configParams:  dict, straight from config file
    # OUTPUTS:
    #     -cityMap:	    		X,Y coordinates of cities. shape=[number_of_cities,2]
    #	  -mapMeta:			dict with meta data about map
    #
    assert type(configParams) == type({})
    temp_resource = __import__('map_creation.'+configParams['city_placement_technique']
                               , globals(), locals(), ['map_creation'], -1)
    cityMap = temp_resource.create_map(configParams)
    print ' INFO: cityMap created succesfully.'
    print '\t- city_placement_technique: ',configParams['city_placement_technique']
    print '\t- number_of_cities:',configParams['number_of_cities']
    
    # TODO ensure this is unique by checking folder to see if ID exists
    map_ID = cmplx.generate_ID('MID',5)
    print ' INFO: non-unique map_ID created successfully.'
    print '\t- map_ID: '+ map_ID
    mapMeta = make_meta(configParams, map_ID)

    return cityMap, mapMeta


# -------------------------------------------------------------------------------------- #
def main(configParams):
        
    # create cityMap
    cityMap, mapMeta = process_to_create_map(configParams)
	
    # save cityMap if applicable
    if "save_map" in configParams and configParams["save_map"] in [True,'true',1,'True']:
        save_map(cityMap, mapMeta)
    else:
        print ' INFO: Not saving results because "save_map" not found in configParams.'
    
    # print results if there aren't a lot of them
    if 'number_of_city_print_thresh' in configParams:
        if configParams['number_of_cities'] <= configParams['number_of_city_print_thresh']:
            print ' cityMap:'
            print cityMap
        else:
            print '\t- map too large to display, number_of_cities > number_of_city_print_thresh'
    else:
        print ' INFO: Not printing results because "number_of_city_print_thresh" not found in configParams'

    print ' OUTPUT:'
    print '\t- map_ID:',mapMeta["map_ID"]

    print ' INFO: Ending script.\n'
    return cityMap, mapMeta



# -------------------------------------------------------------------------------------- #	
if __name__ == "__main__":
    
    # see if users is asking for help
    nSeperatorStars = 55
    helpOptions = ['-h','--h','-help','--help']
    if any((True for x in helpOptions if x in sys.argv)) or len(sys.argv) == 1:
        print
        print '*'*nSeperatorStars
        print 'INFO:'
        print '\tThis script is designed to create a 2d set of coordinates that represent city'
        print '\tlocations through which a traveling salesman would travel if he was selling'
        print '\tgoods. The coordinates are created by a map creation algorithm. Available'
        print '\talgorithsm are located at tsp/src/map_creation/*.py .'

        print 'USE:'
        print '\tParameters serve as input to various map creation techniques. Parameters are'
        print '\tpassed via the command line or can be set in a config file located at'
        print '\ttsp/config/map_creation/parameters.congif . Use the command "python create_map.py"'
        print '\tor "python create_map.py --config" to generate a map using params in the config file.'
        print '\tParameters can also be passed into the script via the command line by using'
        print "\tpython create_map.py '{<JSON formatted key/values go here>}'. Note the single quotes"
        print '\tencasing the JSON formatted parameters!'

        print 'PARAMETERS:'
        print '\tFormat is "key": example_value (data type) [condition]. Indention shows condition too.'
        print '\t"number_of_cities": 10 (integer)'
        print '\t"save_map": 1 (integer, 0 or 1)'

        print '\t"city_placement_technique": "random_uniform"'

        print '\t"city_placement_technique": "fixed_number_of_groups"'
        print '\t  "number_of_groups": 3 (integer) [<= number_of_cities]'
        print '\t  "std_dev_of_offset": 0.05 (decimal)'

        print '\t"city_placement_technique": "donut"'

        print '\t"city_placement_technique": "ball"'
        
        print 'SAMPLE COMMAND:'
        print """\tpython create_map.py '{"number_of_cities":10,"city_placement_technique":"random_uniform"}'"""
        print '*'*nSeperatorStars
        print
        sys.exit(1)

    else:
        print '\n INFO: Begining script.'
        
        # get the parameters by which to create a map with
        if sys.argv[1] == '--config':
            # command looks like "python create_map.py config" and again get from file
            configParams = cmplx.get_config_params('map_creation')
            
        elif len(sys.argv) == 2:
            # command looks like "python create_map.py '{"number_of_cities":10}'
            print ' INFO: Attempting to get configParams from system inputs'
            try:
                configParams = json.loads(sys.argv[1])
            except Exception as e:
                print ' ERROR: Unable to load configuration parameters as JSON. Try...'
                print '''     $ python create_map.py '{"number_of_cities":10,"city_placement_technique":"random_uniform"}' '''
                print ' Exact Python error: '+str(e)
                sys.exit(1)
                
        else:
            print ' ERROR: Too many system arguments. Be sure to wrap JSON in single quotes'
            print """\t$ python create_map.py '{"alg":"brute"}'"""
            sys.exit(1)

        # if script is still running we must have gotten config params, so start up the process!
        main(configParams)



