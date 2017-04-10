# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------- #
import numpy as np

# -------------------------------------------------------------------------------------- #
def create_map(configParams):

    # make sure configParams has correct keys within it
    necesaryKeys = ['number_of_groups','number_of_cities','std_dev_of_offset']
    for key in necesaryKeys:
        assert key in configParams.keys(), "Missing necesary key ("+key+") in map_creation configParams."

    # make sure we have atleast as many cities as there are groups to be created
    assert configParams['number_of_groups'] <= configParams['number_of_cities'] , "number_of_groups > number_of_cities !"

    # decide on the center of number_of_groups many groups
    groupCenters = np.random.uniform(low = 0.0,
                            high = 1.0,
                            size = [ configParams['number_of_groups'], 2 ] )

    # find out which group remaining cities will become part of
    whichGroup = np.random.randint(low=0, 
                                   high=configParams['number_of_groups'], 
                                   size=[configParams['number_of_cities']-configParams['number_of_groups']])

    # assign X and Y coordinates to those remaining cities
    otherCityLocations = np.zeros([len(whichGroup),2])
    for otherCityIndex in range(0, len(whichGroup)):
        
        groupIndex = whichGroup[otherCityIndex]

        xCoordOfGroupCenter = groupCenters[groupIndex,0]
        yCoordOfGroupCenter = groupCenters[groupIndex,1]

        # get polar coordinates of this cities location ofset from group HQ
        angle = np.random.randint(low=0,high=180) # degrees
        distance = np.random.normal(loc=0.0, scale=configParams['std_dev_of_offset'])

        # convert polar offset to cartesian (=X,Y) offset
        xOffset = np.cos(angle*np.pi/180.0)*distance
        yOffset = np.sin(angle*np.pi/180.0)*distance

        # TODO: make sure all cities end up wthin [0,1] in both axis

        otherCityLocations[otherCityIndex,0] = xCoordOfGroupCenter + xOffset
        otherCityLocations[otherCityIndex,1] = yCoordOfGroupCenter + yOffset

    map = np.vstack((groupCenters,otherCityLocations))
    return map

# -------------------------------------------------------------------------------------- #
