import re, copy, sys
from NodeStructures import *
from WatchDog import *

class _EdgeMetaData:
    '''Container class to hold Edge information to be processed once
       the entire file has been read.'''
    def __init__(self, sourceNode, destNodePartialName, desc, lineNum):
        self.sourceNode = sourceNode
        self.destNodePartialName = destNodePartialName
        self.desc = desc
        self.lineNum = lineNum

def readStageTextFile(fileName):
    '''Parses the file with the supplied name and returns a graph
       representing the contents of the file. A WatchDogException is
       raised if a syntax error is detected.'''
    def errTextPrefix(fileName, lineNum = 0):
        tmp = 'Syntax error in file \'' + fileName + '\''
        if lineNum > 0:
            tmp += ' on line ' + str(lineNum)
        tmp += ':\n'
        return tmp
        
    graph = Graph()
    edgeList = []
    lineNum = 0
    currNode = None
    try:
        for line in file(fileName):
            lineNum += 1
            line = line.strip()
            if not line:
                currNode = None
            elif line.startswith('#'):
                continue
            elif line.startswith('>'):
                if not currNode:
                    raise WatchDogException(errTextPrefix(fileName, lineNum) +
                          'A source node name must precede ' +
                          'edge definitions.')
                match = re.match(r'>\s*(\w+)\s+(.+)', line)
                if not match:
                    raise WatchDogException(errTextPrefix(fileName, lineNum) +
                          'Edge definition must contain a ' +
                          'destination node name and description.')
                edgeList.append(_EdgeMetaData(currNode, match.group(1),
                                              match.group(2), lineNum))
            elif line.startswith('-c'):
                if not currNode:
                    raise WatchDogException(errTextPrefix(fileName, lineNum) +
                          'A source node name must precede ' +
                          'content definition.')
                match = re.match(r'-c\s*(.+)', line)
                if not match:
                    raise WatchDogException(errTextPrefix(fileName, lineNum) +
                          'Content definition must contain an element' +
                          ' name.')
                currNode.contents.append(match.group(1))
            elif line.startswith('-p'):
                if not currNode:
                    raise WatchDogException(errTextPrefix(fileName, lineNum) +
                          'A source node name must precede ' +
                          'pre-req definition.')
                match = re.match(r'-p\s*(.+)', line)
                if not match:
                    raise WatchDogException(errTextPrefix(fileName, lineNum) +
                          'Pre-req definition must contain an element' +
                          ' name.')
                currNode.prereqs.append(match.group(1))
            elif not currNode:
                if re.search(r'\s+', line):
                    raise WatchDogException(errTextPrefix(fileName, lineNum) +
                          'Node name must not contain white space.')
                else:
                    try:
                        currNode = graph.node(line)
                    except WatchDogException as e:
                        raise WatchDogException(errTextPrefix(fileName,
                                    lineNum) +
                                    str(e))
            else:
                currNode.also(line)
    except IOError:
        raise WatchDogException('Could not find/open file: \'' + fileName +
                                '\'')

    for edge in edgeList:
        try:
            Edge(edge.sourceNode, graph.nodePartial(edge.destNodePartialName),
                 edge.desc)
        except WatchDogException as e:
            raise WatchDogException(errTextPrefix(fileName, edge.lineNum) +
                                    str(e))
    
    # ensure start and end node exist
    missingNode = None
    if graph.startIndex < 0:
        missingNode = 'Start Node'
        if graph.endIndex < 0:
            missingNode += ' and End Node'
    elif graph.endIndex < 0:
        missingNode = 'End Node'

    if missingNode:
        raise WatchDogException(errTextPrefix(fileName) + 'Missing ' +
                                missingNode + ' declaration.')
    
    graph.appendPromptToNodes()
    return graph
