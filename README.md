## Optimal Path-Finding Tool Kit
This repository holds Python 2.7 code to find the optimal routes through a set of notes.  A common analogy is the Traveling Salesmen Problem, where a salesman is going door to door and must visit all the nodes (houses). Included are several ways to create a set of nodes, which can be though of locations on a map.  There are also a few ways to navigate through those sets of nodes.  It is very easy to integrate your own route-finding algorithm.  Additionally, you can create .gif's of the results, like below:
<p align="center">
  <img width="800" height="600" src="https://github.com/astronomerhunter/pathfinding/blob/master/data/sample_maps_and_solutions/MID34287/solutions/SID02096/movie/animated_solution.gif?raw=true">
</p>

Nodes can be generated using build in algorithms (see src/map_creation) or you can use external data sets.  After the solution is calculated, it is possible to make an animated .gif of the result.  Each node of a set containing n nodes is identified by N<sub>n</sub> should be described by two values p<sub>1</sub> and p<sub>2</sub> (think: latitude and longitude).  This software was orgionally designed to estimate solutions of the Traveling Salesman Problem so the code itself uses words like "cities" to desribe the sets of nodes. It is designed in such a way that non-Python experts should be able to integrate their own aglorthims into the code base.  


### Sets of Nodes
Sets of nodes can be created using this code.  In the Traveling Salesman Problem, the nodes are the locations the salesman must visit.  The algorthiums to create such sets exist in /src/map_creation/ and currently available built-in options include:
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
  
  
  ### To Do:
  1.  Make a "--demo" flag that a user can run immediatly upon cloning repo in order to get an idea for what this codebase can do
  1.  Rename everything away from cities and toward nodes.
1.  Automated test cases so when building a feature we can tell what fails and what passes.
1.  CLI
1.  Convert all JSON config files to YAMl?
1.  Remove configs entirely?
1.  Make input checking standard for create map and do this via a YAMl config file with a single script to run for the logic
1.  Make config JSON into a CLI with flags, one key/val pair should be all the info needed to make the map specific to that map creation type
1.  create_map.py needs to also produce a plot with the correct flag
1.  Fix save method such that non serilizable objects (2+ dimenionsal arrays) play nice with JSON format requirements
1.  for now, all algorithms should find shortest path through system using the first city as the origin city. do not return home