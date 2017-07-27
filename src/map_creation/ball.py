# -*- coding: utf-8 -*-
# This map creation algorithm creates a donut shaped map. The cities are uniformly 
# distributed among [1,360] degrees and the radial distance is from a normal distrubtion
# with mean = 0.5 and std dev = 0.05.
# -------------------------------------------------------------------------------------- #
import numpy as np

# -------------------------------------------------------------------------------------- #  
def get_angle_and_radius():
    # returns one angle in degrees (integer between [0,359]) and one radius.  radii are
    # chosen from a random normal distribution with mean of 0.5 and std dev of 0.05.
    theta = np.random.randint(low=0,high=180)
    R = np.random.normal(loc=0.0,scale=0.05)
    return theta, R


def polar_to_cartesian(theta, R):
    # converts polar coordinates (angle in degrees and distance from center) to cartesian
    # (X and Y)
    theta_rad = theta * (2.0*np.pi/360.0)
    x = np.sin(theta_rad) * R
    y = np.cos(theta_rad) * R
    return x,y


# -------------------------------------------------------------------------------------- #
def create_map(configParams):
    # first define empty arrays
    map = np.zeros(shape=[ configParams['number_of_nodes'], 2])
    # loop through each element, populating map with nonzero x's and y's
    for index in range(0, configParams['number_of_nodes']):
        # define initial values that are certainly not allowed 
        x = -1.0
        y = -1.0
        # keep randomly picking values until you get some allowed ones
        while x < 0.0 or x > 1.0 or y < 0.0 or y > 1.0:
            theta, R = get_angle_and_radius()
            x,y = polar_to_cartesian(theta, R)
            # make (0.5,0.5) the middle of the donut
            x = x + 0.5
            y = y + 0.5
        map[index,0] = x
        map[index,1] = y

    return map
# -------------------------------------------------------------------------------------- #
if __name__ == '__main__':
    print create_map({'number_of_cities':10})
    
