
# In development.
# 

import numpy as np
import itertools
import time
import sys
from functions import complex as cmplx
import random






def solve(configParams, citygraph, graphMeta):
    start_time = time.strftime("%H:%M:%S")
    print ' INFO: Begining solve().'
    print '\t- start time:', start_time
    print '\t- method:', __file__
    nCities = graphMeta['number_of_nodes']
    print '\t- nCities:', nCities

    solution = {}
    
    # populate distance matrix
    print '\t- populating distance matrix'
    distanceMatrix = cmplx.create_distance_matrix(citygraph, nCities)
    print '\t\t- done'

    # create progress bar for tracking
    progressBar = [0]*10

    # number of reevaluations to do
    if configParams['nCities'] < 10:
        nIterations = configParams['nCities']
    else:
         nIterations = configParams['nCities']/2
         
    nWalkers = 50
    lengthOfForecast = configParams['nCities']/3
    
    # to start, randomly pick starting citites for walkers
    currentLocations = np.random.randint(0, 
                                         configParams['nCities'], 
                                         size=nWalkers)
    
    # then make guestLogs for each of them
    guestLogs = {}
    citiesToVisit = {}
    for walker_index in range(0, len(nWalkers)):
        guestLogs[walker_index] = []
        citiesToVisit[walker_index] = range(0, configParams['nCities'])

    for walker_index in range(0, len(nWalkers)):
        currentCity = currentLocations[walker_index]
        guestLogs[walker_index].append(currentCity)
        citiesToVisit[walker_index].remove(currentCity)

    # then shuffle the remaining cities and make an iteneray for that walker
    iteneray = {}
    for walker_index in range(0, len(nWalkers)):
        iteneray[walker_index] = []
        random.shuffle(citiesToVisit[walker_index])
        iteneray[walker_index] = citiesToVisit[walker_index][:lengthOfForecast]

    # calculate distance of forecast
    forecastDistance = {}
    for walker_index in range(0, len(nWalkers)):
        forecastDistance[walker_index] = 0
        for node_index in range(0, len(iteneray[walker_index])-1):
            startNodeIndex = iteneray[walker_index]
            endNodeIndex = iteneray[walker_index+1]
            forecastDistance[walker_index] = forecastDistance[walker_index] + distanceMatrix[startNodeIndex, endNodeIndex]
    
    # pick the minimum distance among the forecastDistances for that node, then take the next step in that forecast.
        

        
    # after hitting all cities, return home if needed
    if 'returnHome' in configParams.keys():
        if configParams['returnHome'] == True:
            journeyDistance = journeyDistance + distanceMatrix[currentCity,originCity]
            journeyPath.append(originCity)

    # wrap up
    end_time = time.strftime("%H:%M:%S")
    print '\t- end time:', end_time

    # save values in solution
    solution['start_time'] = start_time
    solution['end_time'] = end_time
    solution['distanceMatrix'] = distanceMatrix.tolist()
    solution['journeyPath'] = journeyPath
    solution['alg'] = 'foresight'

    return solution
