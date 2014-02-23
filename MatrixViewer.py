# This file is used to print the Matrices for game files.

from WatchDog import *
from StageTextReader import *
from Matrix import *

def main():
    print '---Matrix Printer---'
    print 'Enter the name of the game file to print:'
    fileName = raw_input()
    try:
        printMatrices(readStageTextFile(fileName))
    except WatchDogException as e:
        print 'Error encountered:'
        print str(e)

main()
