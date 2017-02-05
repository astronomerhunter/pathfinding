# -------------------------------------------------------------------------------------- #
# This solver script estimates the shortest path through a cityMap.  It does that by
# choosing the nearest city to go to next.  It prints a progress bar in 10% increments.
# -------------------------------------------------------------------------------------- #
import numpy as np
import itertools
import time
import sys
from functions import complex as cmplx


# -------------------------------------------------------------------------------------- #



# -------------------------------------------------------------------------------------- #
def solve(configParams, cityMap, mapMeta):
    start_time = time.strftime("%H:%M:%S")
    print ' INFO: Begining solve().'
    print '\t- start time:', start_time
    print '\t- method:', __file__
    nCities = mapMeta['number_of_cities']
    print '\t- nCities:', nCities

    solution = {}
    
    # populate distance matrix
    print '\t- populating distance matrix'
    distanceMatrix = cmplx.create_distance_matrix(cityMap, nCities)
    print '\t\t- done'

    # create list storing data about if a city has been visited yet
    guestLog = [False]*nCities

    # visit starting city
    if "origin_city" not in configParams or configParams['origin_city'] == '':
        originCity = np.random.randint(0, nCities)
        currentCity = originCity
        print '\t- origin city randomly selected'
    else:
        originCity = int(configParams['origin_city'])
        currentCity = originCity
        print '\t- origin in config file as',currentCity
    guestLog[currentCity] = True
    
    # define variables to track journey
    journeyDistance = 0.0
    journeyPath = [currentCity]

    # create progress bar for tracking
    progressBar = [0]*10

    # loop through cities until all have been hit choosing to visit nearest neighbor
    print '\t- begining nearest neighbor path'
    while False in guestLog:

        # be verbose
        progressBar = cmplx.print_progress_bar(progressBar,
                                               guestLog.count(True),
                                               len(guestLog))
    
        # create a list of distances to all cities, already visisted distances = infinite
        distancesToCities = np.copy(distanceMatrix[currentCity,:])
        for index in range(0, len(distancesToCities)):
            if guestLog[index] == True:
                distancesToCities[index] = np.inf
            else:
                pass

        # find closest city
        nearestNeighbor = np.where(distancesToCities == np.min(distancesToCities))[0]
        if len(nearestNeighbor) != 1:
            print '\t- found more than 1 equidistance nearest neighbors, randomly selecting one'
        nearestNeighborIndexToChoose = np.random.randint(0,len(nearestNeighbor))
        nearestNeighbor = nearestNeighbor[nearestNeighborIndexToChoose]

        # travel to nearest neighbor, let that city become current, do record keeping
        journeyDistance = journeyDistance + distanceMatrix[currentCity,nearestNeighbor]
        currentCity = nearestNeighbor
        guestLog[currentCity] = True
        journeyPath.append(currentCity)
        
    # after hitting all cities, you'll need to return home
    journeyDistance = journeyDistance + distanceMatrix[currentCity,originCity]
    journeyPath.append(originCity)
        
    # wrap up
    end_time = time.strftime("%H:%M:%S")
    print '\t- end time:', end_time

    # save values in solution
    solution['start_time'] = start_time
    solution['end_time'] = end_time
    solution['distanceMatrix'] = distanceMatrix.tolist()
    solution['journeyDistance'] = journeyDistance
    solution['journeyPath'] = journeyPath
    solution['alg'] = 'greedy'

    return solution
