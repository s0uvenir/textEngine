import copy, sys
from NodeStructures import *
from WatchDog import *
from StageTextReader import *

def _computeMatrix(graph):
    matrix, temp = [], []
    while len(temp) < len(graph.nodes):
        temp.append(0)
    while len(matrix) < len(graph.nodes):
        matrix.append(temp[:])
    
    for node in graph.nodes:
        for edge in node.out:
            matrix[edge.there.id][node.id] = 1
    return matrix

def _convertMatrix(matrix):
    for k in range(len(matrix)):        
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                matrix[i][j] = matrix[i][j] or (matrix[i][k] and matrix[k][j])
    return matrix

def computeMatrices(graph):
    '''Utility method that combines both matrix methods.'''
    graph.m = _computeMatrix(graph)
    graph.mPrime = _convertMatrix(copy.deepcopy(graph.m))

_mySyms=list('0123456789abcdefghojklmnopqrstuvwzyz=?+*-@$:;' + 
            'ABCDEFGHIJKLMNOPQRSTUVWYZ')

def _mySym(n) :
  return _mySyms[n% len(_mySyms)]

def printMatrix(matrix, graph):
    '''Prints the supplied matrix using the node names from the supplied
       graph.'''
    COL_HEADING = 'SOURCE'
    ROW_HEADING = 'DEST'
    
    # width and length are measured in total chars (including spaces)
    width = len(matrix) * 2 - 1
    length = len(matrix)
    rowHeadingStartIndex = (length - len(ROW_HEADING)) / 2
    indexInRowHeading = 0
    
    # print centered column heading
    sys.stdout.write('   ') # indentation
    print ' ' * ((width - len(COL_HEADING)) / 2) + COL_HEADING

    # print heading abbreviations
    sys.stdout.write('   ') # indentation
    for x in range(len(graph.nodes)):
        sys.stdout.write(_mySym(x) + ' ')
    print

    rowNum = -1
    for row in matrix:
        rowNum += 1
        sys.stdout.write(ROW_HEADING[indexInRowHeading] if 
                         rowNum >= rowHeadingStartIndex and 
                         indexInRowHeading < len(ROW_HEADING) else ' ')
        if rowNum >= rowHeadingStartIndex:
            indexInRowHeading += 1
        sys.stdout.write('  ')
        for col in row:
            sys.stdout.write(('.' if col == 0 else str(col)) + ' ')
        print ' ' + _mySym(rowNum) + ' ' + graph.nodes[rowNum].name


# Graph validity tests
def validateGraph(graph):
    matrix = g.mPrime
    for row in range(len(matrix)):
        for col in range(len(matrix)):
            if col == graph.startIndex and matrix[row][col]==0 and col != row:
                raise WatchDogException('Start node unable to reach \'' +
                                        graph.nodes[row].name + '\' node.')
            if col == graph.endIndex and matrix[row][col] == 1:
                raise WatchDogException('End node able to reach \'' +
                                        graph.nodes[row].name + '\' node.')
            if row == graph.startIndex and matrix[row][col]==1:
                raise WatchDogException('Start node able to be reached from \'' +
                                        graph.nodes[col].name + '\' node.')
            if row == graph.endIndex and matrix[row][col] == 0 and col != row:
                raise WatchDogException('End node unable to be reached by \'' +
                                        graph.nodes[col].name + '\' node.')


# Uncomment for sample usage

g = readStageTextFile('games/bloodcell.txt')
computeMatrices(g)
printMatrix(g.m, g)
print
printMatrix(g.mPrime, g)
validateGraph(g)
