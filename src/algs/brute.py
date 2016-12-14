# -------------------------------------------------------------------------------------- #
# This solver script finds all the possible paths.  There are (N-1)! many where N is the 
# number of cities. It can take an extreamly long time when there are more than 10 cities.
# This solver prints a progress bar in 10% increments.
# -------------------------------------------------------------------------------------- #
import numpy as np
import itertools
import time
import sys


# -------------------------------------------------------------------------------------- #
def get_perms(N):
    # returns N!, or the number of permutations. Ex: if N=3, function returns 6. This
    # function exists only because I may someday want to create a get_all_possible_routes()
    # by hand.  I would use this function in that.
    #
    result = 1
    for i in range(1, N+1):
        result = result*i
    return result


def get_all_possible_routes(N, method):
    # Returns all possible routes, using Python indicies (first = 0) to as references
    # for cities.
    # 
    #    INPUTS:
    #        - N: integer, number of cities to calculate possible route for
    #        - method: how to get all possible routes, ['iterator','manual']
    #    OUTPUTS:
    #        - possibleRoutes: [N!,N] sized array where each row is a route path. 
    #
    if method == 'iterator':
        possibleRoutes = list( itertools.permutations( range(0,N) ) )
        return np.asarray(possibleRoutes)
    elif method == 'manual':
        print " ERROR: get_all_possible_routes(method='manual') isn't build yet"
        sys.exit(100)
    else:
        print " ERROR: get_all_possible_routes() needs 'method' argument, see function comments"
        sys.exit(100)


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
    # This function finds the fastest route through the cityMap.
    #
    start_time = time.strftime("%H:%M:%S")
    print ' INFO: Begining solve().'
    print '\t- start time:', start_time
    print '\t- method:', __file__
    nCities = mapMeta['number_of_cities']
    print '\t- nCities:', nCities

    minCitiesToSlowCode = 9
    if nCities > minCitiesToSlowCode:
        proceedResponse = ''
        print ('\n WARNING: There are more than '+str(minCitiesToSlowCode)+' cities in this map, brute forcing may take a while.')
        proceedResponse = raw_input('\t\tWould you like to proceed? ["y" to continue]  ')
        print '\n'
        if proceedResponse == 'y':
            pass
        else:
            print ' INFO: user input cancelled solve().'
            return None

    solution = {}

    # list each possible path
    print '\t- getting all possible paths'
    paths = get_all_possible_routes(nCities, 'iterator')
    print '\t\t- aquired '+str(len(paths))+' of them'
    
    # populate distance matrix
    print '\t- populating distance matrix'
    distanceMatrix = create_distance_matrix(cityMap, nCities)
    print '\t\t- done'

    # calculate the total distance of each path
    print '\t- begining calculation of each path length'
    progressBar = create_progress_bar(10)
    distances = np.zeros(np.shape(paths)[0])
    for i in range(0, len(distances)):
        thisPath = paths[i,:]
        thisDistance = 0
        for j in range(0, len(thisPath)-1):
            cityAindex = thisPath[j]
            cityBindex = thisPath[j+1]
            thisDistance = thisDistance + distanceMatrix[cityAindex,cityBindex]
        distances[i] = thisDistance
        progressBar = print_progress_bar(progressBar, i, len(distances))

    # find shortest path
    shortest_path_index = np.where(distances == min(distances))[0]

    # wrap up
    end_time = time.strftime("%H:%M:%S")
    print '\t- end time:', end_time

    # save values in solution
    solution['start_time'] = start_time
    solution['end_time'] = end_time
    solution['paths'] = paths
    solution['distanceMatrix'] = distanceMatrix
    solution['distances'] = distances
    solution['end_time'] = end_time
    solution['shortest_path_index'] = shortest_path_index

    return solution