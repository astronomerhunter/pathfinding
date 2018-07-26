# -*- coding: utf-8 -*-

# This function houses the more complex functions. Unless you're a dev, hands off.

import os
import json
import numpy as np
from . import simple as smpl



def get_filepath_to_repo():    
    # Retuns the path to the pathfinding/ folder.  This function is included so that a user
    # of this code doesn't have to set a bash variable with the path to the repo.
    #
    pathToFunctSimple_str = smpl.get_path_to_this_file()
    pathToFunctSimple_list =  smpl.filepath_string_to_list(pathToFunctSimple_str)
    pathToRepo_list = pathToFunctSimple_list[:-3] 
    return smpl.filepath_list_to_string(pathToRepo_list)

def get_filepath_to_graph_data(graph_ID):
    # This functions returns the filepath to a graph and its meta data given
    # a graph_ID.
    #
    pathToFunctSimple_str = smpl.get_path_to_this_file()
    pathToFunctSimple_list =  smpl.filepath_string_to_list(pathToFunctSimple_str)
    # remove 'src', 'functions', 'simple.py' to get tsp/
    pathToTPS_list = pathToFunctSimple_list[:-3]
    pathTographID_list = pathToTPS_list + ['data','graphs',graph_ID,graph_ID]
    pathTographID_str = smpl.filepath_list_to_string(pathTographID_list)
    pathTograph = pathTographID_str+'.txt'
    pathToMeta = pathTographID_str+'_meta.txt'
    return pathTograph, pathToMeta


def get_filepath_to_solution_data(graph_ID, sol_ID):
    # This functions returns the filepath to a graph and its meta data given 
    # a graph_ID.
    #
    pathToFunctSimple_str = smpl.get_path_to_this_file()
    pathToFunctSimple_list =  smpl.filepath_string_to_list(pathToFunctSimple_str)
    
    # remove 'src', 'functions', 'simple.py' to get to tsp/
    pathToTPS_list = pathToFunctSimple_list[:-3]
    
    pathToSolFile_list = pathToTPS_list + ['data','graphs',graph_ID,'solutions',sol_ID,sol_ID]
    pathToSolFile_str = smpl.filepath_list_to_string(pathToSolFile_list)
    
    # make sure directories exist
    pathToSolFolder = smpl.filepath_list_to_string(pathToSolFile_list[:-2])
    pathToSolIDFolder = smpl.filepath_list_to_string(pathToSolFile_list[:-1])

    if os.path.exists(pathToSolFolder) == False:
        os.mkdir(pathToSolFolder)
    if os.path.exists(pathToSolIDFolder) == False:
        os.mkdir(pathToSolIDFolder)
    
    return pathToSolFile_str+'.json'


def generate_ID(prefix, nDigits):
    # This function attempts to generate an ID, which is a string of
    # "<prefix><nDigits of random numbers>".
    #
    assert type(prefix) == type('')
    assert type(nDigits) == type(0)
    numbersToAdd = np.random.random_integers(low=0,high=9,size=[nDigits])
    ID = prefix
    for i in range(0, nDigits):
        ID = ID + str(numbersToAdd[i])
    return ID



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
        print('\t\t- % done:', numberToPrint)
    return progressBar



def create_vertex_weights_matrix(citygraph, nCities):
    # When searching each possible path for the shortest overall path, you'll need to
    # repeatidly calculate the distance between any two cities.  Rather than doing
    # this at run time, this function returns a matrix that shows the distance from
    # any city to any other city.
    #
    distanceMatrix = np.zeros([nCities,nCities])
    # TODO: make this loop more efficent; it doesnt need to loop through every elemnt
    for i in range(0, np.shape(distanceMatrix)[0]):
        for j in range(0, np.shape(distanceMatrix)[1]):
            distanceMatrix[i,j] = get_2d_euclidean_dist(citygraph[i,0],
                                                        citygraph[i,1],
                                                        citygraph[j,0],
                                                        citygraph[j,1])
    return distanceMatrix



def get_2d_euclidean_dist(Ax,Ay,Bx,By):
    # This function returns the distance between cityA and cityB.
    #
    return np.sqrt((Ax - Bx)**2 + (Ay - By)**2)


