## Optimal Path-Finding Tool Kit

<p align="center">
  <img width="460" height="300" src="https://github.com/astronomerhunter/pathfinding/blob/master/data/sample_maps_and_solutions/MID34287/solutions/SID02096/movie/animated_solution.gif?raw=true">
  A .gif of the the "greedy" algorithm (also known as the nearest neighbor algorithm) being applied to a randomly generated set of nodes.  The node locations were picked via the algorithm at src/map_creation/fixed_number_of_groups.py.
</p>


This software package uses Python 2.7 to find the most desireable path through a set of nodes.  Nodes can be generated using build in algorithms or you can use external data sets.  After the solution is calculated, it is possible to make an animated .gif of the result.  Each node should be described by two values (think: latitude and longitude).  This software was orgionally designed to estimate solutions of the Traveling Salesman Problem so the code itself uses words like "cities" to desribe the sets of nodes. It is designed in such a way that non-Python experts should be able to integrate their own aglorthims into the code base.  


### Sets of Nodes
Sets of nodes, (or "maps", or sets of "cities") can be created using this code.  The algorthiums to create such sets exist in /src/map_creation/ and currently available built-in options include:
  - random_uniform : Randomly distribute cities on a map.
  - donut : Center a normal distribution some distance away from the middle of the map and at random degrees of rotation.  With enough cities, this map becomes donut shaped.
  - ball : Center a normal distribution on the middle of the map.  The distribution of cities decreases with radius from the middle of the map.
  - fixed_number_of_groups : Create a handful of clusters and the map.  Randomly locate these clusters.  Each city belongs to a cluster and is located nearby the cluster center.  This offset is a normal distrbution.
  - sinusoidal : The distriubtion function is sin^2(x,y).
Alternatively, one could put external node sets in conjunction with the solving algorithms in this repository if they convert their node sets to the expected data types.  The best way to go about this is to generate a map using one of the built in algorithms, inspect the output, and convert external data to match the format.
Soon, I'll add the exact distribution functions to this document.

### Path Finding Algorithms
The algorithms that navigate through the node sets are located at src/algs/.  Currently there is:
  - brute : Calculates each possible path through the nodeset and returns the shortest.  Computation time goes as (N-1)! where N is the number of nodes.  Not practical when N > 10.
  - greedy : From the starting node, always travels to the next closest node.
  - random_neighbor : Choose a random path through the city list. Do not return home to origin city after visiting every city.

### Want To Contribute?
The goal of this project is to create an infrastructure for estimating solutions of the traveling salesmen problem.  Please follow the file system structure outlined in file_tree_graphic.txt. The infrastructure should:
  - allow for a user to easily create an randomly generated city map:
    - using premade algorithums
    - by creating their own map creation algorithm
  - allow for a user to easily apply a tsp solution estimation algorithum to a city map:
    - using premade algorithms
    - by creating their own solution algorithm
  - visualize solutions to previously executed solution algorithms
  - easily apply various solution algorithms to maps created from various map creation algorithms
