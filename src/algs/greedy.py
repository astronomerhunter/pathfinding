# -------------------------------------------------------------------------------------- #
# This solver script estimates the shortest path through a cityMap.  It does that by
# choosing the nearest city to go to next.  It prints a progress bar in 10% increments.
# -------------------------------------------------------------------------------------- #
import numpy as np
import itertools
import time
import sys


# -------------------------------------------------------------------------------------- #
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


def create_progress_bar(N):
    # Returns a list of 0's that is N long.
    #
    return [0]*N


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
    distanceMatrix = create_distance_matrix(cityMap, nCities)
    print '\t\t- done'

    # create list storing data about if a city has been visited yet
    guestLog = [False]*nCities

    # select a random starting city
    currentCity = np.random.randint(0,nCities)
    guestLog[currentCity] = True
    
    # define variables to track journey
    journeyDistance = 0.0
    journeyPath = [currentCity]

    # create progress bar for tracking
    progressBar = create_progress_bar(10)

    # loop through cities until all have been hit choosing to visit nearest neighbor
    print '\t- begining nearest neighbor path'
    while False in guestLog:

        # be verbose
        progressBar = print_progress_bar(progressBar,
                                         len(np.where(guestLog == False)[0]),
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
        currentCity = np.copy(nearestNeighbor)
        guestLog[currentCity] = True
        journeyPath.append(currentCity)
        
        
        
    # wrap up
    end_time = time.strftime("%H:%M:%S")
    print '\t- end time:', end_time

    # save values in solution
    solution['start_time'] = start_time
    solution['end_time'] = end_time
    solution['distanceMatrix'] = distanceMatrix
    solution['journeyDistance'] = journeyDistance
    solution['journeyPath'] = journeyPath

    return solution
