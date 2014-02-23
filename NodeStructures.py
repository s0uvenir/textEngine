# File containing Graph, Node, and Edge classes

from WatchDog import WatchDogException

class Graph:
    PROMPT_STRING = 'What would you like to do?'
    
    def __init__(self):
        self.nodes = []    # nodes, stored in creation order
        self.keys  = {}    # nodes indexed by name
        self.m = None      # adjacency matrix
        self.mPrime = None # transitive closure matrix
        self.startIndex = -1 # index of start node
        self.endIndex = -1 # index of end node
    
    def node(self,name):
        "returns a old node from cache or a new node"
        if not name in self.keys:
            self.keys[name] = self.newNode(name)
        return self.keys[name]
    
    def newNode(self,name):
        " create a new node"
        id = len(self.nodes) 
        tmp = Node(self,id,name)
        if Node.start in name:
            if self.startIndex >= 0:
                raise WatchDogException('Start Node already declared.')
            tmp.start = True
            tmp.name = tmp.name.replace(Node.start, '')
            self.startIndex = id
        if Node.end in name:
            if self.endIndex >= 0:
                raise WatchDogException('End Node already declared.')
            tmp.end = True
            tmp.name = tmp.name.replace(Node.end, '')
            self.endIndex = id
        
        self.nodes += [tmp]
        return tmp

    def nodePartial(self, partialName):
        '''Returns the unique node that matches the supplied partial name.
           A WatchDogException is raised if no name matches or if multiple
           names match.'''
        matchedNodes = []
        for node in self.nodes:
            if node.name.startswith(partialName):
                matchedNodes.append(node)

        length = len(matchedNodes)
        if(length == 0):
            raise WatchDogException('No matching name found for: \'' +
                                    partialName + '\'.')
        if(length > 1):
            message = 'Ambiguous name: \'' + partialName + '\'.\n' + \
                      'Could match: '
            isFirst = True
            for node in matchedNodes:
                if isFirst: isFirst = False
                else: message += ', '
                message += '\'' + node.name + '\''
            message += '.'
            raise WatchDogException(message)
        return matchedNodes[0]

    def appendPromptToNodes(self):
        '''Appends the prompt string to the descriptions of all existing
           nodes. This should be called after all nodes have been added.'''
        for node in self.nodes:
            if not node.end:
                node.also(Graph.PROMPT_STRING)

    def __repr__(self):
        return 'Graph Nodes:\n' + str(self.nodes)

class Node:
    end   = "."
    start = "!"
    
    def __init__(self,g,id,name,stop=False,start=False):
        self.id = id
        self.graph = g          # where do i live?
        self.name = name        # what is my name?
        self.description = ""   # tell me about myself
        self.stop = stop        # am i a stop node?
        self.start = start      # am i a start node?
        self.out = []           # where do i connect to (edges, not nodes)
    
    def also(self,txt):
        "adds text to description"
        sep = "\n" if self.description else ""
        self.description += sep + txt
    
    def __repr__(self):
        return "\nN( :id " + str(self.id) + \
               "\n   :name " + self.name + \
               "\n   :about '" + self.description + "'" + \
               "\n   :out " + str(self.out) + ") "

class Edge:
    def __init__(self,here,there,txt):
        self.description = txt     # why am i making this jump? 
        self.here        = here    # where do i start
        self.there       = there   # where to i end
        self.here.out   += [self]  # btw, tell here that they can go there
    
    def __repr__(self):
        return "E(" + self.here.name + " > " + self.there.name + ")"
