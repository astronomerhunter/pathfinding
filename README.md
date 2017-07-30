### The Problem
Given a set of N static nodes, each having p<sub>1</sub> and p<sub>2</sub> where 0 <= p<sub>1</sub>, p<sub>2</sub> <= 1, find the minimum cost path that touches all N nodes, where the cost is defined as the 2 dimensional cartesian distance between any two nodes.


### Path Finding through Set of Nodes
Calculating the the minimum cost path through a set of notes is a computational taxing problem.  One must perform on the order of N! calculations to find the optimal path through a set of N nodes.  This becomes impractical on a standard Macbook when N > 10.  Estimating the optimal solution using intellegent algorithms is much more effective technique that normally results within 10% of the optimal solution with the most pragmatic algorithms.

This software package allows users to rapidly develop and test algorithms to estimate the optimal path.  With the code in this repository, one leverage the easy-to-use CLI to focus on the development of the interesting bits: the pathfinding algorithm itself.


### Sample Solution
The below animated solution uses the "nearest_neighbor" algorithm, also called the "greedy" algorithm, to estimate the optimal path through 100 nodes.  Hint: if the .gif isn't loading, give it a minute, its about 5 MB large.  

<p align="center">
  <img width="800/1.2" height="600/1.2" src="https://github.com/astronomerhunter/pathfinding/blob/master/data/sample_solutions/animated_solution.gif">
</p>


### The Codebase
Users of this codebase can:
1.  Create sets of nodes using `src/create_map.py`.  The placement of the nodes is based on some sort of 2D distriubtion.  A user can create their own distribution function or use any of the built in ones available at `src/map_creation/*.py`.  A distribution function can take various other parameters, for example `fixed_number_of_groups` requires the user to specify how many groups to create.  For examples of built in distribution functions, see `data/sample_maps/*.png`.  Currently the build in distribution functions are:
    1.  `random_uniform`: randomly distribute nodes
    1.  `ball`: a normal distribution in p<sub>1</sub> and p<sub>2</sub> centered at (0.5, 0.5)
    1.  `donut`: centers the peak of a normal distriubtion some distance away from (0.5, 0.5)
    1.  `fixed_number_of_groups`: creates a handful of clusters randomly around the map
    1.  `sinusoidal`: the distriubtion function is sin<sup>2</sup>(p<sub>1</sub>, p<sub>2</sub>)
1.  Calculate a path through the set of nodes using `src/execute.py`.  The path is calculated via one of the solvers available at `src/solvers/*.py`.  Again, a user can integrate their own solver.  They'd do this by writting the code and putting it in the `src/solvers` folder and enabling it in the "USAGE" section of the document string at the top of `src/execute.py`.  The included solvers are:
    1.  `brute`: calculate the cost of all possible paths through a set and return the minimum cost path.  This is the only surefire way to get the optimal path but is incredably slow when N is large.
    1.  `nearest_neighbor`: algorithm that, when at any given node, travels to the next closest node
    1.  `random_neighbor`: when at any given node, randomly selects another unvisited node to travel to next.  Expect this to be far form the optimal pathh through the city list. Do not return home to origin city after visiting every city.


### Want To Contribute?
The goal of this project is to create an infrastructure for estimating solutions of the problem.  The infrastructure should:
  - allow for a user to easily create an randomly generated node map:
    - using premade algorithums
    - by creating their own map creation algorithm
  - allow for a user to easily apply a solution estimation algorithm to a node map:
    - using premade algorithms
    - by creating their own solution algorithm
  - visualize solutions to previously executed solution algorithms
  - easily apply various solution algorithms to maps created from various map creation algorithms
  
  
### To Do:
1.  Make a "--demo" flag that a user can run immediatly upon cloning repo in order to get an idea for what this codebase can do
1.  Automated test cases so when building a feature we can tell what fails and what passes.
1.  Clear up why JSON is saved the way it is.  Fix save method such that non serilizable objects (2+ dimenionsal arrays) play nice with JSON format requirements
1.  Add functionality to define an origin node and to define the ability to have to end at that origin node.
