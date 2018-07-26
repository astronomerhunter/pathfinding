"""
This graph creation algorithm creates a donut shaped graph. The cities are uniformly 
distributed among [1,360] degrees and the radial distance is from a normal distrubtion
with mean = 0.5 and std dev = 0.05.
"""
import numpy as np


def get_angle_and_radius():
    # returns one angle in degrees (integer between [0,359]) and one radius.  radii are
    # chosen from a random normal distribution with mean of 0.5 and std dev of 0.05.
    theta = np.random.randint(low=0,high=360)
    R = np.random.normal(loc=0.5,scale=0.05)
    return theta, R


def polar_to_cartesian(theta, R):
    # converts polar coordinates (angle in degrees and distance from center) to cartesian
    # (X and Y)
    theta_rad = theta * (2.0*np.pi/360.0)
    x = np.sin(theta_rad) * R
    y = np.cos(theta_rad) * R
    return x,y


def create_graph(args):
    node_locations = np.zeros(shape=[ args['N'], 2])
    for dummy_index in range(0, args['N']):
        x = -1.0
        y = -1.0
        while x < 0.0 or x > 1.0 or y < 0.0 or y > 1.0:
            theta, R = get_angle_and_radius()
            x,y = polar_to_cartesian(theta, R)
            x = x + 0.5
            y = y + 0.5
        node_locations[dummy_index,0] = x
        node_locations[dummy_index,1] = y
    return node_locations


if __name__ == '__main__':
    pass
