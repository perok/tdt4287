
def createGraphviz(root, step=0):
    string = "digraph {\n"
    string +="\trankdir = LR;\n"
    string +="\tedge [arrowsize=0.4,fontsize=10]\n"
    string +="\tnode1 [label=\"\",style=filled,fillcolor=lightgrey,shape=circle,width=.1,height=.1];\n"
    string +="//------leaves------\n"
    string += printLeaves.py(root) + "\n"
    string +="//------internal nodes------\n"
    string += printInternalNodes(root) + "\n"
    string +="//------edges------\n"
    string += printEdges(root) + "\n"
    string +="//------suffix links------\n"
    string += printSLinks(root) + "\n"
    string +="\n}"
    
    filepath = "graphviz/step{0}.dot"
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    with open(filepath.format(step), "w") as text_file:
        text_file.write(string)

def _printLeaves.py(node, name="root"):
    string = ""
    if len(node.edges) is 0:
        string += "\tnode" + name + " [label=\"\",shape=point]"
    else:
        for char, edge in node.edges.iteritems():
            string += printLeaves.py(edge[2], char)
    return string

def _printInternalNodes(node, name="root"):
    string = ""
    if not node.isRoot and len(node.edges) > 0:
        string += "\tnode" + name + " [label="",style=filled,fillcolor=lightgrey,shape=circle,width=.07,height=.07]"
    else:
        for char, edge in node.edges.iteritems():
            string += printInternalNodes(edge[2], char)
    return string

def _printEdges(node, name="root"):
    string = ""
    for char, edge in node.edges.iteritems():
        edgeString = self.string[edge[0]: len(self.string) if edge[1] is ENDCHAR else edge[1]]
        string +="\tnode"+name+" -> node"+char+" [label=\""+edgeString+"\",weight=3]"
        string += printEdges(edge[2], char)
    return string

def _printSLinks(node, name="root"):
        string = ""
        if node.link is not None:
            string += "\tnode"+name+" -> node"+"HERE BE LINK"+" [label=\"\",weight=1,style=dotted]"
        else:
            for char, edge in node.edges.iteritems():
                string += printSLinks(edge[2], char)
        return string


