import os

def createGraphviz(root, stri, step=0):

    string = "digraph {\n"
    string +="\trankdir = LR;\n"
    string +="\tedge [arrowsize=0.4,fontsize=10]\n"
    string +="\tnode"+str(root.id)+" [label=\"\",style=filled,fillcolor=lightgrey,shape=circle,width=.1,height=.1];\n"
    string +="//------leaves------\n"
    string += _printLeaves(root) + "\n"
    string +="//------internal nodes------\n"
    string += _printInternalNodes(root) + "\n"
    string +="//------edges------\n"
    string += _printEdges(root, stri, step) + "\n"
    string +="//------suffix links------\n"
    string += _printSLinks(root) + "\n"
    string +="\n}"
    
    filepath = "graphviz/step{0}.dot"
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    with open(filepath.format(step), "w") as text_file:
        text_file.write(string)

def _printLeaves(node, name="root"):
    string = ""
    if len(node.edges) is 0:
        string += "\tnode" + str(node.id) + " [label=\"\",shape=point]\n"
    else:
        for char, edge in node.edges.iteritems():
            string += _printLeaves(edge.node, char)
    return string

def _printInternalNodes(node, name="root"):
    string = ""
    if not node.isRoot and len(node.edges) > 0:
        string += "\tnode" + str(node.id) + "[label=\"\",style=filled,fillcolor=lightgrey,shape=circle,width=.07,height=.07]\n"

    for char, edge in node.edges.iteritems():
        string += _printInternalNodes(edge.node, char)
    return string

def _printEdges(node, treeString, step,  name="root"):
    string = ""
    for char, edge in node.edges.iteritems():
        # todo, accessing correct?
        edgeString = "{0} [{1}, {2}]".format(treeString[edge.start:min(edge.end, len(treeString))], edge.start, edge.end)

        #print edgeString, char, edge.start, edge.start + len(edge)
        #edgeString = string[edge.start: len(string) if edge[1] is ENDCHAR else edge[1]]

        string +="\tnode"+str(node.id)+" -> node"+str(edge.node.id)+"[label=\""+edgeString+"\",weight=3]\n"
        string += _printEdges(edge.node, treeString, step,  char)
    return string

def _printSLinks(node, name="root"):
        string = ""
        if node.link is not None:
            string += "\tnode"+str(node.id)+" -> node"+str(node.link.id)+" [label=\"\",weight=1,style=dotted]\n"

        for char, edge in node.edges.iteritems():
            string += _printSLinks(edge.node, char)
        return string


