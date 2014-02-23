import copy, sys
from NodeStructures import *
from WatchDog import *
#from StageTextReader import *

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

def _computeIslandMatrix(graph):
    '''Computes the island matrix for the supplied graph. If the
       adjecency and/or transitive matrices have not already been computed, they
       will also be computed.'''
    if not graph.m:
        graph.m = _computeMatrix(graph)
    if not graph.mPrime:
        graph.mPrime = _convertMatrix(copy.deepcopy(graph.m))

    # Nodes a and b are in the same island iff (a can reach b) or (b can reach a)
    # or (a and b each can reach a common node) or (a common node can reach a and b)

    currIslandNum = 1
    # compute which island each node is in
    for i in range(len(graph.nodes)):
        # check if we already know what island nodes[i] is in
        if not graph.nodes[i].islandNum:
            # check if nodes[i] is related to any node that is in a known island
            for j in range(len(graph.nodes)):
                # check if nodes[j] is in a known island
                if graph.nodes[j].islandNum:
                    # check if either node can reach the other
                    if (graph.mPrime[i][j] or graph.mPrime[j][i]):
                        # nodes[j] can reach nodes[i] or vice versa,
                        # so nodes[i] must be in nodes[j]'s island
                        graph.nodes[i].islandNum = graph.nodes[j].islandNum
                        break
                    # check if both nodes can reach the same node or vice versa
                    for k in range(len(graph.nodes)):
                        if (graph.mPrime[k][i] and graph.mPrime[k][j])\
                            or (graph.mPrime[i][k] and graph.mPrime[j][k]):
                            # nodes[i] and nodes[j] can reach nodes[k] (or vice versa),
                            # so nodes[i], nodes[j], and nodes[k] must be in the same island
                            graph.nodes[i].islandNum = graph.nodes[j].islandNum
                            graph.nodes[k].islandNum = graph.nodes[j].islandNum
                            break
            if not graph.nodes[i].islandNum:
                # no known island was found, so it is in a new island
                graph.nodes[i].islandNum = currIslandNum
                currIslandNum += 1

    # the island matrix is a copy of the adjacency matrix, with the '1's
    # replaced by the number of the island
    graph.islandM = copy.deepcopy(graph.m)
    for rowNum in range(len(graph.nodes)):
        for colNum in range(len(graph.nodes)):
            if graph.islandM[rowNum][colNum]:
                # internal assertion
                if graph.nodes[rowNum].islandNum != graph.nodes[colNum].islandNum:
                    raise WatchDogException('Problem with island matrix.')
                graph.islandM[rowNum][colNum] = graph.nodes[rowNum].islandNum

def computeMatrices(graph):
    '''Utility method that combines both matrix methods.'''
    graph.m = _computeMatrix(graph)
    graph.mPrime = _convertMatrix(copy.deepcopy(graph.m))
    _computeIslandMatrix(graph)

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

def printMatrices(graph):
    '''Prints all 3 matrices for the graph (calculating them if neccessary).'''
    if not (graph.m and graph.mPrime and graph.islandM):
        computeMatrices(graph)

    print 'Adjacency Matrix:\n'
    printMatrix(graph.m, graph)
    print '\nIsland Matrix:\n'
    printMatrix(graph.islandM, graph)
    print '\nTransitive Closure of Adjacency Matrix:\n'
    printMatrix(graph.mPrime, graph)

# Graph validity tests
def validateGraph(graph):
    matrix = graph.mPrime
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

