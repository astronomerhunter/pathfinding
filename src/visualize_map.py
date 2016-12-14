# This code is from travelingsalesmen/ and is not up to date
# handle imports
import numpy as np
import os
import matplotlib.pylab as plt

# describe file you wanna load
saveFilePath = os.getcwd() + '/citylocations/'
saveFileName = 'alpha.txt'

# import city list
if os.path.isfile(saveFilePath+saveFileName) == True:
        city_locations = np.loadtxt(saveFilePath+saveFileName)
        
        
# plot image
plt.scatter(city_locations[:,0], 
            city_locations[:,1])
            
plt.ylim([0,1])
plt.xlim([0,1])
            
plt.xlabel('x axis location')
plt.ylabel('y axis location')
plt.title('Location of Citys')

plt.show()
