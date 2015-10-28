import os

class Grapher(object):
    def __init__(self, gst):
        self.gst = gst

    def createGraphviz(self, step=""):

        string = "digraph {\n"
        string +="\trankdir = LR;\n"
        string +="\tedge [arrowsize=0.4,fontsize=10]\n"
        string +="\tnode"+str(self.gst.root.id)+" [label=\"\",style=filled,fillcolor=lightgrey,shape=circle,width=.1,height=.1];\n"
        string +="//------leaves------\n"
        string += self._printLeaves(self.gst.root) + "\n"
        string +="//------internal nodes------\n"
        string += self._printInternalNodes(self.gst.root) + "\n"
        string +="//------edges------\n"
        string += self._printEdges(self.gst.root) + "\n"
        string +="//------suffix links------\n"
        string += self._printSLinks(self.gst.root) + "\n"
        string +="\n}"
        
        filepath = "graphviz/step{0}.dot"
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        with open(filepath.format(step), "w") as text_file:
            text_file.write(string)

    def _printLeaves(self, node, name="root"):
        string = ""
        if len(node.edges) is 0:
            string += "\tnode" + str(node.id) + " [label=\""+str(node.id)+"\",shape=circle]\n" #shape=point
        else:
            for char, edge in node.edges.iteritems():
                string += self._printLeaves(edge, char)
        return string

    def _printInternalNodes(self, node, name="root"):
        string = ""
        if not node.is_root() and len(node.edges) > 0:
            string += "\tnode" + str(node.id) + "[label=\""+str(node.id)+"\",style=filled,fillcolor=lightgrey,shape=circle,width=.07,height=.07]\n"

        for char, edge in node.edges.iteritems():
            string += self._printInternalNodes(edge, char)
        return string

    def _printEdges(self, node, name="root"):
        string = ""
        for char, edge in node.edges.iteritems():
            # todo, accessing correct?
            internalString = self.gst.get_internal_subtring(edge, edge.start, edge.end)#min(edge.end, len(treeString)))
            edgeString = "{0} ({1})[{2}, {3}]".format(internalString, edge.string_id, edge.start, edge.end)

            #print edgeString, char, edge.start, edge.start + len(edge)
            #edgeString = string[edge.start: len(string) if edge[1] is ENDCHAR else edge[1]]

            string +="\tnode"+str(node.id)+" -> node"+str(edge.id)+"[label=\""+edgeString+"\",weight=3]\n"
            string += self._printEdges(edge, char)
        return string

    def _printSLinks(self, node, name="root"):
            string = ""
            if node.link is not None:
                string += "\tnode"+str(node.id)+" -> node"+str(node.link.id)+" [label=\"\",weight=1,style=dotted]\n"

            for char, edge in node.edges.iteritems():
                string += self._printSLinks(edge, char)
            return string


