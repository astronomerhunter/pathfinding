# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------- #
# This function houses the more complex functions. Unless you're a dev, hands off.
# -------------------------------------------------------------------------------------- #
import os
import json
import numpy as np
from . import simple as smpl


# -------------------------------------------------------------------------------------- #
def get_config_params(whichConfig):
    # This function reads parmaters from a configuration file stored at 
    # "tsp/config/<whichConfig>/parameters.config" and passes them back. The config
    # file is JSON-like. 
    #
    # INPUTS:
    #     -none
    # OUTPUTS:
    #     -cfgPrms:	JSON with everything in the config file.
    #
    assert type(whichConfig) == type('')
    pathToThisFile_str = smpl.get_path_to_this_file()
    pathToThisFile_list =  smpl.filepath_string_to_list(pathToThisFile_str)
    # remove 'src', 'functions', 'simple.py' to get tsp/
    pathToTPS_list = pathToThisFile_list[:-3]
    pathToConfigFile_list = pathToTPS_list + ['config',whichConfig,'parameters.config']
    pathToConfigFile_str = smpl.filepath_list_to_string(pathToConfigFile_list)
    # load JSON-like config parameters
    configParams_str = open(pathToConfigFile_str).read()
    # convert long string into JSON
    configParams = json.loads(configParams_str)
    print ' INFO: Got '+whichConfig+' configuration parameters.'
    print '\t- source: '+pathToConfigFile_str
    print '\t- keys and values:'
    dict_keys = list(configParams.keys())
    for i in range(0, len(configParams.keys())):
        print '\t\t- '+str(dict_keys[i])+' : '+str(configParams[dict_keys[i]])
    # return JSON with configuration parameters
    return configParams
    
    
def get_filepath_to_map_data(map_ID):
    # This functions returns the filepath to a map and its meta data given
    # a map_ID.
    #
    pathToFunctSimple_str = smpl.get_path_to_this_file()
    pathToFunctSimple_list =  smpl.filepath_string_to_list(pathToFunctSimple_str)
    # remove 'src', 'functions', 'simple.py' to get tsp/
    pathToTPS_list = pathToFunctSimple_list[:-3]
    pathToMapID_list = pathToTPS_list + ['data','maps',map_ID,map_ID]
    pathToMapID_str = smpl.filepath_list_to_string(pathToMapID_list)
    pathToMap = pathToMapID_str+'.txt'
    pathToMeta = pathToMapID_str+'_meta.txt'
    # make sure directories exist
    pathToMapIDFolder = smpl.filepath_list_to_string(pathToMapID_list[:-1])
    if os.path.exists(pathToMapIDFolder) == False:
        os.mkdir(pathToMapIDFolder)

    return pathToMap, pathToMeta


def get_filepath_to_solution_data(map_ID, sol_ID):
    # This functions returns the filepath to a map and its meta data given 
    # a map_ID.
    #
    pathToFunctSimple_str = smpl.get_path_to_this_file()
    pathToFunctSimple_list =  smpl.filepath_string_to_list(pathToFunctSimple_str)
    # remove 'src', 'functions', 'simple.py' to get to tsp/
    pathToTPS_list = pathToFunctSimple_list[:-3]
    pathToSolID_list = pathToTPS_list + ['data','maps',map_ID,'solutions',sol_ID]
    pathToSolID_str = smpl.filepath_list_to_string(pathToSolID_list)
    # make sure directories exist
    pathToSolFolder = smpl.filepath_list_to_string(pathToSolID_list[:-2])
    pathToSolIDFolder = smpl.filepath_list_to_string(pathToSolID_list[:-1])
    if os.path.exists(pathToSolFolder) == False:
        os.mkdir(pathToSolFolder)
    if os.path.exists(pathToSolIDFolder) == False:
        os.mkdir(pathToSolIDFolder)
    return pathToSolID_str


def generate_ID(prefix, nDigits):
    # This function attempts to generate an ID, which is a string of
    # "<prefix><nDigits of random numbers>".
    #
    assert type(prefix) == type('')
    assert type(nDigits) == type(0)
    numbersToAdd = np.random.random_integers(low=0,high=9,size=[nDigits])
    ID = 'MID'
    for i in range(0, nDigits):
        ID = ID + str(numbersToAdd[i])
    return ID


def save_solution(saveMethod, solution):
    # This function saves a solution by saving solution,a python dictionary,
    # as ether raw text files, a JSON, or a numpy compressed pickled file.
    #
    try:
        assert type(saveMethod) == type('')
        assert type(solution) == type({})
    except:
        print ' ERROR: improper inputs into save_solution():'
        print '\t- saveMethod should be string, is ', type(saveMethod)
        print '\t- solution should be dictionary, is', type(solution)
        return None

    filePathPrefix = get_filepath_to_solution_data(solution['map_ID'],
                                                   solution['sol_ID'])

    if saveMethod == 'txt':
        pass
    elif saveMethod == 'json':
        print " ERROR: cannot save as JSON b/c some arrays aren't serizible"
        """
        with open(filePathPrefix+'.json', 'w') as fp:
            json.dump(solution, fp)
        """
        pass
    elif saveMethod == 'npy':
        pass
    else:
        print ' INFO: unrecognized saveMethod ('+saveMethod+'), skipping...'


def print_progress_bar(progressBar, currentIndex, maxIndex):
    # This function attempts to print a % update every at intervals of
    # len(progressBar)/ 100 %.
    #
    #    INPUTS:
    #        - progressBar: if element = 0 it hasnt been printed yet. normalized
    #                       to 100%, ex: if len() = 4 then print @ 25%,50%,75%,100%
    #        - currentIndex: current index loop is at
    #        - maxIndex: max index of loop, after index = max index loop should end
    #    OUTPUTS:
    #        - progressBar: return so it can be passed back into this function next
    #                       loop
    #
    percentComplete = int(100.0 * currentIndex / maxIndex)
    nIntervals = len(progressBar)
    nIntervalsDone = (percentComplete-(percentComplete%nIntervals))/nIntervals
    if progressBar[nIntervalsDone] == 0:
        progressBar[nIntervalsDone] = 1
        numberToPrint = nIntervals * nIntervalsDone
        print '\t\t- % done:', numberToPrint
    return progressBar



def create_distance_matrix(cityMap, nCities):
    # When searching each possible path for the shortest overall path, you'll need to
    # repeatidly calculate the distance between any two cities.  Rather than doing
    # this at run time, this function returns a matrix that shows the distance from
    # any city to any other city.
    #
    distanceMatrix = np.zeros([nCities,nCities])
    # TODO: make this loop more efficent; it doesnt need to loop through every elemnt
    for i in range(0, np.shape(distanceMatrix)[0]):
        for j in range(0, np.shape(distanceMatrix)[1]):
            distanceMatrix[i,j] = get_2d_euclidean_dist(cityMap[i,0],
                                                        cityMap[i,1],
                                                        cityMap[j,0],
                                                        cityMap[j,1])
    return distanceMatrix



def get_2d_euclidean_dist(Ax,Ay,Bx,By):
    # This function returns the distance between cityA and cityB.
    #
    return np.sqrt((Ax - Bx)**2 + (Ay - By)**2)
