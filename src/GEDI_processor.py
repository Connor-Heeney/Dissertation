import os
import h5py
import numpy as np
import pandas as pd
import geopandas as gp
import matplotlib.pyplot as plt
import shapely

'''
Plan:

1. Create an overall class to hold all the methods - Something like GEDI_processor

2. Create a method that will read metadata from files to give more information

3. Create a method that will plot the GEDI data 

4. Create a method to clip the GEDI data to the boundary of interest

5. Create a method to plot the PAVD of one or multiple files
    - This is essential to create the time series

6. Create a method to plot the PAI (same reasoning as step 5)

7. We need something to look at the different peaks in the waveformt so that 
it can be interpreted where the over/understory is 
    - Also need to Decipher this from the plotted PAI and PAVD too

8. Potentially make this modular if necessary??

9. Keep in mind that all of this needs to be done whilst accounting for memory management

'''

class GediProcessor():

    def workspace():
        # inDir = os.getcwd()  # Set input directory to the current working directory
        # os.chdir(inDir)
        # print(inDir)

        # gediFiles = [g for g in os.listdir(inDir+'/src/data/gedi/') if g.startswith('processed') and g.endswith('.h5')]  # List all GEDI L2B .h5 files in inDir
        # gediFiles
        # print(gediFiles)
        pass

    def retrieve_metadata():
        '''
        Allows the user to view the supporting data associated with the files, such as:
        - General metadata (ie., creation date, purpose etc).
        - The SDS data (i.e., the varying beams and variables within - PAI, PAVD, lon, lat etc).
        '''
        pass

    def quality_check():
        '''
        Looks at the quality flags
        within each file and removes values which are 0 
        (i.e., doesn't pass the quality check).
        '''
        pass

    def plot_coverage():
        pass

    def clip_gedi():
        pass

    def gedi_pavd():
        # '''
        # So I'm basically just opening the GEDI files in a given folder,
        # and as all the information is stored hierarchical I just need to pull out the 
        # PAVD from each beam and plot it
        # '''
        pass

    def gedi_pai():
        pass

if __name__ == "__main__":
    pass