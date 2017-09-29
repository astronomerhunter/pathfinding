# -------------------------------------------------------------------------------------- #
import numpy as np
import os
import matplotlib.pylab as plt
import sys
from functions import complex as cmplx
from functions import simple as smpl

# -------------------------------------------------------------------------------------- #
def generate_static_PNG_of_map(node_locations, map_ID):
    #
    #
    x = node_locations[:,0]
    y = node_locations[:,1]
    nNodes = np.shape(node_locations)[0]
    print ' INFO: number of nodes to plot:', nNodes
    plt.scatter(x,y)

    xLowerLimit = min(x) - 0.10*(np.abs(max(x)-min(x)))
    xUpperLimit = max(x) + 0.10*(np.abs(max(x)-min(x)))
    yLowerLimit = min(y) - 0.10*(np.abs(max(y)-min(y)))
    yUpperLimit = max(y) + 0.10*(np.abs(max(y)-min(y)))
    print ' INFO: lower and upper bounds indentified'
    print '\t - xLowerLimit:',xLowerLimit
    print '\t - xUpperLimit:',xUpperLimit
    print '\t - yLowerLimit:',yLowerLimit
    print '\t - yUpperLimit:',yUpperLimit
    plt.xlim([xLowerLimit,xUpperLimit])
    plt.ylim([yLowerLimit,yUpperLimit])

    plt.xlabel('p_1 value')
    plt.ylabel('p_2 value')
    plt.title('p_1 and p_2 of all Nodes')

    pathToMapFile, pathToMetaFile = cmplx.get_filepath_to_map_data(map_ID)
    pathToMapFolder_list = pathToMapFile.split(os.path.sep)[:-1]
    pathToMapFolder_list.append(map_ID+'_static.png')
    # TODO: use filepath_list_to_string() in simple.py instead of the following line
    pathToStatic = str('/'+os.path.join(*pathToMapFolder_list))
    plt.savefig(pathToStatic)
    return pathToStatic

def make_PNGs_for_greedy(pathToSol, solution, node_locations):
    #
    #
    pathToSol = pathToSol.split('/')[:-1] + ['movie']
    pathToMovie = smpl.filepath_list_to_string(pathToSol) + '/'
    if os.path.exists(pathToMovie) == False:
        os.mkdir(pathToMovie)
        print ' INFO: created directory to hold all the movie still images'
    else:
        print ' INFO: no need to create movie directory, one already exists'
        print '\t- path:',pathToMovie

    progressBar = [0]*10
    listOfStillPaths = []
    x = node_locations[:,0]
    y = node_locations[:,1]

    nNodes = len(x)
    for i in range(0, len(solution['journeyPath'])-1):
        originIndex = solution['journeyPath'][i]
        destinationIndex = solution['journeyPath'][i+1]
        x1 = x[originIndex]
        y1 = y[originIndex]
        x2 = x[destinationIndex]
        y2 = y[destinationIndex]
        # draw a line from one city to another
        plt.plot([x1,x2],[y1,y2], 'k')

        # make sure we add leading 0's before numbers that have less digits than others
        if len(str(i)) != len(str(nNodes-1)):
            maxNumbDigits = len(str(nNodes-1))
            thisNumbDigits = len(str(i))
            nMissingDigits = maxNumbDigits - thisNumbDigits
            indexString = '0'*nMissingDigits + str(i)
        else:
            indexString = str(i)
                    
        stillFilePath = pathToMovie+'frame'+indexString+'.png'
        plt.savefig(stillFilePath)
        listOfStillPaths.append(stillFilePath)
        cmplx.print_progress_bar(progressBar, i, len(solution['journeyPath'])-1)
    return pathToMovie, listOfStillPaths

def make_GIF_from_PNGs(pathToMovie, listOfStillPaths):
    #
    #
    try:
        gifSavePath = pathToMovie+'animated_solution.gif'
        import imageio
        images = []
        for filename in listOfStillPaths:
            images.append(imageio.imread(filename))
            imageio.mimsave(gifSavePath, images)
        print '\t- GIF made!'
        print '\t- saved @',gifSavePath
        print '\t- HINT: To view the .gif file on Mac OSX, select it in finder then press space bar key'

    except Exception as e:
        print '\n ERROR: Ran into an issue creating GIF.'
        print '\t- Exact Python error:', e
        print '\n'

# -------------------------------------------------------------------------------------- #
def main(parameters):
    print ' INFO: Parameters:'
    for key in parameters.keys():
        print '\t- '+key+' : '+parameters[key]

    pathToMap, pathToMeta = cmplx.get_filepath_to_map_data(parameters['map_ID'])
    try:
       	node_locations = np.loadtxt(pathToMap)
        print ' INFO: found a cityMap @',pathToMap
    except Exception as e:
        print '\n ERROR loading City Locations file'
        print '\t- looked @', pathToMap
        print '\t- exact Python error:', e
        print '\n'
        sys.exit(1)

    pathToStatic = generate_static_PNG_of_map(node_locations, parameters['map_ID'])
    print ' INFO: saved a static image of the map @',pathToStatic
    
    if 'sol_ID' not in parameters.keys():
        print 'INFO: Script ending\n'
        sys.exit(0)
    else:
        pathToSol = cmplx.get_filepath_to_solution_data(parameters['map_ID'], parameters['sol_ID'])
        try:
            import json
            with open(pathToSol,'r') as f:
                solution = json.load(f)
            print ' INFO: solution JSON found @',pathToSol
        except Exception as e:
            print '\n ERROR loading solutions file'
            print '\t- looked @',pathToSol
            print '\t- exact Python error:',e
            print
            sys.exit(1)
        
        if solution['alg'] in ['greedy', 'random_neighbor', 'nearest_neighbor']
            print ' INFO: solution["alg"] detected as "'+solution['alg']+'", commencing movie creation'
            pathToMovie, listOfStillPaths = make_PNGs_for_greedy(pathToSol, solution, node_locations)
            print ' INFO: Creating animated GIF'
            make_GIF_from_PNGs(pathToMovie, listOfStillPaths)
        else:
             print ' INFO: visualize.py not built to handle',solution['alg']
        
        print 'INFO: Script done.'
        print '\n'
        
# -------------------------------------------------------------------------------------- #
if __name__ == '__main__':
    helpOptions = ['-h','--h','-help','--help']
    if any((True for x in helpOptions if x in sys.argv)):
        # TODO: lets rewrite this guy
        print
        print 'INFO:'
        print '\tthis needs to be written!'
        print
        sys.exit(0)
    else:
        print '\n INFO: Begining script.'
        # get the parameters by which to create a visualization with
        if len(sys.argv) == 1:
            # command looks like "python visualize.py"
            print ' ERROR: This script needs inputs passed as JSON encased in single quotes'
            print '''      $ python visualize.py '{"map_ID":"MID12345"}' '''
            print '\n'
            sys.exit(1)
        else:
            # try to intrepret command line argument as a JSON
            print ' INFO: Attempting to get parameters from command line input'
            try:
                import json
                parameters = json.loads(sys.argv[1])
            except Exception as e:
                print ' ERROR: Unable to intrepret command line argument as JSON. Try...'
                print '''     $ python visualize.py '{"map_ID":"MID12345"}' '''
                print ' Exact Python error:', e
                print '\n'
                sys.exit(1)
    main(parameters)
