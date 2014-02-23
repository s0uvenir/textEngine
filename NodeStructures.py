# File containing Graph, Node, and Edge classes

from WatchDog import WatchDogException

class Graph:
    DEFAULT_PROMPT_STRING = 'What would you like to do?'
    
    def __init__(self, promptString = DEFAULT_PROMPT_STRING):
        self.nodes = []    # nodes, stored in creation order
        self.keys  = {}    # nodes indexed by name
        self.m = None      # adjacency matrix
        self.mPrime = None # transitive closure matrix
        self.islandM = None # island matrix (each cell is the number of the
                            # island that the edge is in)
        self.startIndex = -1 # index of start node
        self.endIndex = -1 # index of end node
        self.promptString = promptString # the string appended to each node's
                                         # description (except the last node
    
    def node(self,name):
        "returns a old node from cache or a new node"
        if not name in self.keys:
            self.keys[name] = self.newNode(name)
        return self.keys[name]
    
    def newNode(self,name):
        " create a new node"
        id = len(self.nodes) 
        tmp = Node(self,id,name)
        if Node.START in name:
            if self.startIndex >= 0:
                raise WatchDogException('Start Node already declared.')
            tmp.start = True
            tmp.name = tmp.name.replace(Node.START, '')
            self.startIndex = id
        if Node.END in name:
            if self.endIndex >= 0:
                raise WatchDogException('End Node already declared.')
            tmp.stop = True
            tmp.name = tmp.name.replace(Node.END, '')
            self.endIndex = id
        
        self.nodes += [tmp]
        return tmp

    def nodePartial(self, partialName, nodeSubset = None):
        '''Returns the unique node that matches the supplied partial name,
           from the nodes in nodeSubset. If no subset is supplied, the entire
           list of nodes in the graph is searched. A WatchDogException is
           raised if no name matches or if multiple names match.'''
        if not nodeSubset:
            nodeSubset = self.nodes
        
        matchedNodes = []
        for node in nodeSubset:
            if node.name.startswith(partialName):
                # if there is an exact match, disregard other partial matches
                if node.name == partialName:
                    return node
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
            if not node.stop:
                node.also(self.promptString)

    def __repr__(self):
        return 'Graph Nodes:\n' + str(self.nodes)

class Node:
    END   = "."
    START = "!"
    
    def __init__(self,g,id,name,stop=False,start=False):
        self.id = id
        self.graph = g          # where do i live?
        self.name = name        # what is my name?
        self.description = ""   # tell me about myself
        self.stop = stop        # am i a stop node?
        self.start = start      # am i a start node?
        self.out = []           # where do i connect to (edges, not nodes)
        self.contents = [] # list of strings representing what is added
                           # to the inventory when this node is entered
        self.prereqs = [] # list of strings representing what is removed
                          # from the inventory when this node is entered
        self.islandNum = None # the number of the island that this node is in
    
    def also(self,txt):
        "adds text to description"
        sep = "\n" if self.description else ""
        self.description += sep + txt
    
    def __repr__(self):
        return "\nN( :id " + str(self.id) + \
               "\n   :name " + self.name + \
               "\n   :about '" + self.description + "'" + \
               "\n   :out " + str(self.out) + ") " + \
               ("\n   :contents " + str(self.contents) if self.contents != [] \
               else "") + \
               ("\n   :pre-reqs " + str(self.prereqs) if self.prereqs != [] \
               else "")

class Edge:
    def __init__(self,here,there,txt):
        self.description = txt     # why am i making this jump? 
        self.here        = here    # where do i start
        self.there       = there   # where to i end
        self.here.out   += [self]  # btw, tell here that they can go there
    
    def __repr__(self):
        return "E(" + self.here.name + " > " + self.there.name + ")"

