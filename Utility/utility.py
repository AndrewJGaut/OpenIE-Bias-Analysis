'''
This file contains some functions used in several different files and functions used generally throughout the project
'''

import os

'''
Parameters:
    dirName - the name of the directory the text file is in
    fileName - the name of the text file
What it does:
    Finds the text file in the project at path dirName/fileName as long as the textFile's
    directory is a parent of the directory in which this function is called
    Returns the file itself in read mode
'''
def getTextfile(dirName, fileName):
    while(not os.path.isdir(dirName)):
            os.chdir('../')
    return open(os.path.join(dirName, fileName), 'r')
