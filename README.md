<p align="center">
  <img width="800/1.2" height="600/1.2" src="https://github.com/astronomerhunter/pathfinding/blob/master/data/sample_solutions/animated_solution.gif">
</p>

### Introduction
Finding the most desirable path between some locations is a general, previlent problem.  This codebase facilitates finding the most desireable path among a set of locations, so long as information about those locations is provided.  In this quanitative exploration, we refer to these locations as "Nodes", each having some position in space, such as longitude and latitude.  The "most desirable path" between nodes is normally the path that visits all the nodes, but minimizes some cost funciton, such as time taken to traverse the path or distance traveled along the path.  In other words, we want to go everywhere but while costing us the least.  We can generalize this problem and use an algorithmic approach to find the most desirable path.

This repository allows one to apply algorithms designed to quickly obtain the most desirable path.  Such algorithms are useless without a set of nodes to test them on, so the feature to create sets of nodes with various characteristics is included.  This codebase also makes it very easy to create and test user-created algorithms.  To learn more about the code, read `The Codebase` section.


### A Quantitative Description of the Problem
Given a set of N static nodes, each having p<sub>1</sub> and p<sub>2</sub> where 0 <= p<sub>1</sub>, p<sub>2</sub> <= 1, find the minimum cost path that touches all N nodes, where the cost is defined as the 2 dimensional cartesian distance between any two nodes.


### The Codebase
Calculating the the minimum cost path through a set of notes is a computational taxing problem.  One must perform on the order of N! calculations to find the optimal path through a set of N nodes.  This becomes impractical on a standard Macbook when N > 10.  Estimating the optimal solution using intellegent algorithms is much more effective technique that normally results within 10% of the optimal solution with the most pragmatic algorithms.

This software package allows users to rapidly develop and test algorithms to estimate the optimal path.  With the code in this repository, one leverage the easy-to-use CLI to focus on the development of the interesting bits: the pathfinding algorithm itself.  Users of this codebase can:
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

### Notes
Some important notes:
  1.  Solutions visit all nodes
  1.  The first node in the cityLocations file is considered the origin.  This is unchangeable.
  1.  From any node one can visit any other node as long as they assume the cost in the cost matrix
    1.  This is important because in some Traveling Salesmen Problems, not every node can visit each other node.  We can account for this case by setting the cost of this path and its inverse (A->B has inverse B->A) to infinity in the cost matrix.  By doing this we introduce the subcase where a set of nodes may be intrinsicly unable to travel to another set of nodes, resulting in the cost of the lowest cost path equal to infinity.
  1.  Once a path from A->B is taken, it and its inverse is removed from possible future paths to be taken.  AKA no repeats.
    1.  To explain, consider set {A, B, C, D}.  The path A->B->C->D is obvious, but the above statement disallows A->B->C->B->A->D.  If we considered paths like this I believe there would huge, but finitely many paths to consider on a set of finite size.  


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
1.  Clear up why JSON is saved the way it is.  Fix save method such that non serilizable objects (2+ dimenionsal arrays) play nice with JSON format requirements.
  1.  Update: curretly using `toList()` to make 2D arrays serializable.
1.  Add functionality to define an origin node and to define the ability to have to end at that origin node.
1.  Add vocabulary section.
  1.  Combinatorial Optimization
  1.  node
  1.  optimal path
  1.  optimal cost
  1.  
1.  Redo CLI.
1.  Use YAML...
