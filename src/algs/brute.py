# -------------------------------------------------------------------------------------- #
# This solver script finds all the possible paths.  There are (N-1)! many where N is the 
# number of cities. It can take an extreamly long time when there are more than 10 cities.
# This solver prints a progress bar in 10% increments.
# -------------------------------------------------------------------------------------- #
import numpy as np
import itertools
import time
import sys
from functions import complex as cmplx


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


def get_all_possible_routes(N, originCity, method):
    # Returns all possible routes, using Python indicies (first = 0) to as references
    # for cities.
    # 
    #    INPUTS:
    #        - N: integer, number of cities to calculate possible route for
    #        - originCity: index of the origin city
    #        - method: how to get all possible routes, ['iterator','manual']
    #    OUTPUTS:
    #        - possibleRoutes: [(N-1)!/2,N] sized array where each row is a unique route path. 
    #
    if method == 'iterator':
        # make a list of cities. be sure not to visit the origin city
        listOfCities = range(0,N-1)
        for index in range(0, len(listOfCities)):
            if listOfCities[index] > originCity or listOfCities[index] == originCity:
                listOfCities[index] = listOfCities[index] + 1
            else:
                pass
        # the fancy method to get the possible routes
        possibleRoutes = list( itertools.permutations(listOfCities) )
        # possibleRoutes is symetrical, ex: path [1,2,3]==[3,2,1]. only first half is unique
        possibleRoutes = possibleRoutes[:len(possibleRoutes)/2]
        # arrays are cool
        possibleRoutes = np.asarray(possibleRoutes)
        # tac on origin city as first and last city in each path
        originAdjPosRts = np.zeros([np.shape(possibleRoutes)[0],
                                    np.shape(possibleRoutes)[1]+2])
        originAdjPosRts[:,0] = originCity
        originAdjPosRts[:,-1] = originCity
        # fill the meat of the paths array with the old routes
        originAdjPosRts[:,1:-1] = possibleRoutes
        return originAdjPosRts

    elif method == 'manual':
        print " ERROR: get_all_possible_routes(method='manual') isn't build yet"
        sys.exit(100)
    else:
        print " ERROR: get_all_possible_routes() needs 'method' argument, see function comments"
        sys.exit(100)



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

    # see if an origin city has been defined
    if "origin_city" not in configParams or configParams['origin_city'] == '':
        originCity = np.random.randint(0, nCities)
        print '\t- origin city randomly selected'
    else:
        originCity = int(configParams['origin_city'])
        print '\t- origin in config file as',originCity

    # list each possible path
    print '\t- getting all possible paths'
    paths = get_all_possible_routes(nCities, originCity, 'iterator')
    print '\t\t- aquired '+str(len(paths))+' of them'
    
    # populate distance matrix
    print '\t- populating distance matrix'
    distanceMatrix = cmplx.create_distance_matrix(cityMap, nCities)
    print '\t\t- done'

    # calculate the total distance of each path
    print '\t- begining calculation of each path length'
    progressBar = [0]*10
    distances = np.zeros(np.shape(paths)[0])
    for i in range(0, len(distances)):
        thisPath = paths[i,:]
        thisDistance = 0
        for j in range(0, len(thisPath)-1):
            cityAindex = int(thisPath[j])
            cityBindex = int(thisPath[j+1])
            thisDistance = thisDistance + distanceMatrix[cityAindex,cityBindex]
        distances[i] = thisDistance
        progressBar = cmplx.print_progress_bar(progressBar, i, len(distances))

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
    solution['alg'] = 'brute'

    return solution
