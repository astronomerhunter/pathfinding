# handle imports
import numpy as np
import os
import matplotlib.pylab as plt
import sys
from functions import complex as cmplx



def main(parameters):

    # print parameters
    print ' INFO: Parameters:'
    for key in parameters.keys():
        print '\t- '+key+' : '+parameters[key]


    # get path to the data
    pathToMap, pathToMeta = cmplx.get_filepath_to_map_data(parameters['map_ID'])
    try:
       	city_locations = np.loadtxt(pathToMap)
        print ' INFO: found a cityMap @',pathToMap
    except Exception as e:
        print '\n ERROR loading City Locations file'
        print '\t- looked @', pathToMap
        print '\t- exact Python error:', e
        print '\n'
        sys.exit(1)


    # plot image
    x = city_locations[:,0]
    y = city_locations[:,1]
    nCities = len(x)
    print ' INFO: number of cities to plot:',nCities
    plt.scatter(x,y)
    
    # limits of plot are min/max +/- 10%
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

    # write some labels
    plt.xlabel('x axis location')
    plt.ylabel('y axis location')
    plt.title('Location of Citys')

    # plot home city with a star if one is defined



    # if pathToSol isn't defined then we're just showing the map
    if 'sol_ID' not in parameters.keys():
        plt.show()
        print 'INFO: Script ending\n'
        sys.exit(0)


    # if it is, then we need to draw the solution before we show the result
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
        
        
        if solution['alg'] == 'greedy':
            print ' INFO: solution["alg"] detected as "greedy", commencing movie creation'
            
            # make a directory to house all the images
            pathToSol = pathToSol.split('/')[:-1] + ['movie']
            from functions import simple as smpl
            pathToMovie = smpl.filepath_list_to_string(pathToSol) + '/'

            if os.path.exists(pathToMovie) == False:
                os.mkdir(pathToMovie)
                print ' INFO: created directory to hold all the movie still images'
            else:
                print ' INFO: no need to create movie directory, one already exists'
            print '\t- path:',pathToMovie

            # save first image, which is just the city map
            plt.savefig(pathToMovie+'cityMap.png')

            print ' INFO: Ready to begin making a frame for each hop through the cityMap'
            progressBar = [0]*10

            listOfStillPaths = []

            # create a whole lot of images
            for i in range(0, len(solution['journeyPath'])-1):
                # draw the line from one city to another
                originIndex = solution['journeyPath'][i]
                destinationIndex = solution['journeyPath'][i+1]
                x1 = x[originIndex]
                y1 = y[originIndex]
                x2 = x[destinationIndex]
                y2 = y[destinationIndex]
                plt.plot([x1,x2],[y1,y2], 'k')

                # make sure we add leading 0's before numbers that have less digits than others
                if len(str(i)) != len(str(nCities-1)):
                    maxNumbDigits = len(str(nCities-1))
                    thisNumbDigits = len(str(i))
                    nMissingDigits = maxNumbDigits - thisNumbDigits
                    indexString = '0'*nMissingDigits + str(i)
                else:
                    indexString = str(i)
                    
                stillFilePath = pathToMovie+'frame'+indexString+'.png'
                plt.savefig(stillFilePath)
                listOfStillPaths.append(stillFilePath)
                # print a progress bar!
                cmplx.print_progress_bar(progressBar, i, len(solution['journeyPath'])-1)

            
            # create a gif movie!
            print ' INFO: Creating animated GIF'
            outputFilePath = ''
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

            print 'INFO: Script done.'
            print '\n'
            

        else:
            print "\n ERROR: only solution['alg'] = 'greedy' is drawable at this moment"
            print '\n'
            sys.exit(1)



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
