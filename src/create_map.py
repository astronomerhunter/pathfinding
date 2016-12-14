# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------- #
# This function creates a map of cities.  The properties of that map draw from a
# configuration file at /config/map_creation/parameters.config.  If the number of cities
# is small enough, they are printed out by this function.
#
# Created by Hunter Brooks on 7/12/2016.  Please don't use my code without permission.
# -------------------------------------------------------------------------------------- #
import numpy as np
import json
from functions import complex as cmplx


# -------------------------------------------------------------------------------------- #
def make_meta(configParams, map_ID):
    # This function returns a dictionary that makes up the metadata.
    return { "map_ID" : map_ID,
             "number_of_cities" : configParams['number_of_cities']}


def save_map(saveMapOption, cityMap, mapMeta):
    # This function checks if save_map is 1. If so, it creates a map ID and saves the 
    # map to "tsp/data/hist/<map_ID>/<map_ID>_locations.txt".  It also saves metadata at 
    # "tsp/data/hist/<map_ID>/<map_ID>_metadata.txt".  It checks to make sure the created
    # map_ID that is not already present.  
    #
    # INPUTS:
    #    -configParams:	to see if we even want to save the map, via configParams['save_map']
    #    -cityMap:		2d array of x and y locations of each city.
    #	 -mapMeta		dict containing meta data about map, like map_ID
    # OUTPUTS:
    #    -nothing is returned
    #
    assert type(saveMapOption) == type(0),'Function input type mismatch.'
    if saveMapOption == 1:
        map_ID = mapMeta['map_ID']
        mapSavePath, metaSavePath = cmplx.get_filepath_to_map_data(map_ID)
        print '\t- saving map @ '+mapSavePath
        np.savetxt(mapSavePath, cityMap)
        print '\t- saving meta @ '+metaSavePath
        with open(metaSavePath, 'w') as outfile:
            json.dump(mapMeta, outfile)

    if saveMapOption == 0:
        print ' INFO: Not saving cityMap, save_map = 0.'


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
    #	    -mapMeta:			dict with meta data about map
    #
    assert type(configParams) == type({})
    temp_resource = __import__('map_creation.'+configParams['city_placement_technique']
                               , globals(), locals(), ['map_creation'], -1)
    cityMap = temp_resource.create_map(configParams)
    print ' INFO: cityMap created succesfully.'
    print '\t- technique:  '+configParams['city_placement_technique']
    
    # TODO ensure this is unique by checking folder to see if ID exists
    map_ID = cmplx.generate_ID('MID',5)
    print ' INFO: non-unique map_ID created successfully.'
    print '\t- map_ID: '+ map_ID
    mapMeta = make_meta(configParams, map_ID)

    return cityMap, mapMeta


# -------------------------------------------------------------------------------------- #
def main():
    print '\n INFO: Begining script.'

    # retrieve config params
    configParams = cmplx.get_config_params('map_creation')

    # create cityMap
    cityMap, mapMeta = process_to_create_map(configParams)
	
    # call function to see if we need to save cityMap
    save_map(configParams["save_map"], cityMap, mapMeta)
    
    if configParams['number_of_cities'] <= configParams['number_of_city_print_thresh']:
        print ' VARIABLE cityMap:'
        print cityMap
    else:
        print '\t- map too large to display, number_of_cities > number_of_city_print_thresh'

    print ' INFO: Ending script.\n'


# -------------------------------------------------------------------------------------- #	
if __name__ == "__main__":
    main()
