from WatchDog import *
from StageTextReader import *
from Matrix import *

def start():
    inventory = []
    filename = ""
    while (filename == ""):
        print "Enter a filename:"
        filename = raw_input()
        try:
            graph = readStageTextFile("games/" + filename)
            computeMatrices(graph)
            validateGraph(graph)
        except WatchDogException, e:
            print e
            filename = ""
    currentNode = graph.nodes[graph.startIndex]
    while (not currentNode.stop):
        printNode(currentNode)
        currentNode = tryMatch(currentNode).there
        if(not currentNode.prereqs):
            inventory += currentNode.contents
        else:
            for x in range(len(currentNode.prereqs)):
                if(currentNode.prereqs[x] in inventory):
                    inventory.remove(currentNode.prereqs[x])
                    inventory += [currentNode.contents[x]]

    printNode(currentNode)
    if(inventory):
        for x in inventory:
            print x

def printNode(node):
    print '\n' + node.description
    for x in node.out:
        print ">" + x.description

def tryMatch(node):
    whereToGo = []
    while (whereToGo == []):
        string = raw_input()
        for x in node.out:
            if(re.match("^" + string + ".*", x.description, flags = re.IGNORECASE)):
                whereToGo.append(x)
        if(len(whereToGo) == 1):
            return whereToGo[0]
        else:
            if(len(whereToGo) < 1):
                print "Did not match."
            else:
                print "Matched multiple choices."
            whereToGo = []
            printNode(node)
    
start()
