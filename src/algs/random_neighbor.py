# -------------------------------------------------------------------------------------- #  
# Randomly travels to cities.  Does not return to the origin city at end.
# -------------------------------------------------------------------------------------- #
import numpy as np
import itertools
import time
import sys
from functions import complex as cmplx


# -------------------------------------------------------------------------------------- #
# Functions go here


# -------------------------------------------------------------------------------------- #
def solve(configParams, cityMap, mapMeta):
    # This function finds the fastest route through the cityMap.
    #
    start_time = time.strftime("%H:%M:%S")
    print ' INFO: Begining solve().'
    print '\t- start time:', start_time
    print '\t- method:', __file__
    nCities = mapMeta['number_of_cities']
    print '\t- nCities:', nCities

    solution = {}

    # see if an origin city has been defined
    if "origin_city" not in configParams or configParams['origin_city'] == '':
        originCity = np.random.randint(0, nCities)
        print '\t- origin city randomly selected'
    else:
        originCity = int(configParams['origin_city'])
        print '\t- origin in config file as',originCity
    
    # populate distance matrix
    print '\t- populating distance matrix'
    distanceMatrix = cmplx.create_distance_matrix(cityMap, nCities)
    print '\t\t- done'

    # calculate the total distance of each path
    print '\t- forming list of city indicies'
    unvisitedCities = range(0,nCities)
    unvisitedCities.remove(originCity)
    unvisitedCities.insert(0,originCity)
    print '\t\t- unvisitedCities: '+ str(unvisitedCities)

    # step through list of unvisited cities, keeping track of the distance traveled
    distance = 0.0
    for index in range(0, len(unvisitedCities)-1):
        distance = distance + distanceMatrix[unvisitedCities[index],unvisitedCities[index+1]]
    
    # wrap up
    end_time = time.strftime("%H:%M:%S")
    print '\t- end time:', end_time

    # save values in solution
    solution['start_time'] = start_time
    solution['end_time'] = end_time
    solution['distanceMatrix'] = distanceMatrix
    solution['distances'] = distance
    solution['end_time'] = end_time
    solution['unvisitedCities'] = unvisitedCities
    solution['alg'] = 'random_neighbor'

    return solution
