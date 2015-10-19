ENDCHAR = '#'

class Node(object):
    """
    Node class that represents parent and children pointers.

    Children dict has edges ((pos, ENDCHAR), Node(self)).

    No parent means that it is the root node.
    """
    counter = 0
    def __init__(self, isRoot=False):
        self.isRoot = isRoot 
        self.edges = {}
        self.link = None
        self.id = Node.counter
        Node.counter += 1

    def setEdge(self, char, fr, to):
        """ 
        Add one edge to node.
        Edge is representent with tuple (start, end, ->Node)
        char -> (from, to, node)
        """
        node = Node()
        #self.edges[char] = [fr, to, node]
        self.edges[char] = Edge(fr, to, node)

    def __repr__(self):
        s =  "N({0}, {1}, {2})\n".format(self.id, self.isRoot, self.link is not None)
        for key, value in self.edges.iteritems():
            s += "\t{0} -> {1}\n".format(key, value)
        return s


class Edge(object):
    def __init__(self, start, end, node):
        self.start = start
        self.end = end
        self.node = node

    def __len__(self):
        return self.end - self.start 

    def __repr__(self):
        return "E({0} -> {1})".format(self.start, self.end)

class SuffixTree(object):
    """
    Suffix tree algorithm.
    Builds tree with Ukkonens algorithm.
    """

    def __init__(self, string):

        self.string = string

        self.root = Node(isRoot=True)

        self._buildUkkonen()

    def _buildUkkonen(self):

        # tuple (active_node, active_edge, active_length)
        active = {
            'node': self.root,
            'edge': '\00',
            'length': 0
        }

        # How many new suffixes that need to be inserted. 
        # Set to one at the beginning of each step
        remainder = 0

        ENDCHAR = len(self.string)
        print "ENDCHAR length", ENDCHAR, self.string

        print " ##### Suffix for", self.string
        # Iterate over all steps in input string.
        # From pos 0 to pos len(string) - 1
        # Step is position in string
        # todo this can be made to a addChar method? Step is obviously not needed
        for step in xrange(len(self.string)):
            raw_input()

            from SuffixGrapher import createGraphviz
            createGraphviz(self.root, self.string, step=step)

            c_char = self.string[step] 

            # How many new suffixes that need to be inserted. 
            # Set to one at the beginning of each step
            remainder += 1 

            nodeNeedSuffixLink = None

            print "### Starting step", step, "with", c_char

            # Work through all remainders for each character
            while remainder > 0:
                print "## Remainder", remainder, "active length", active['length']
                # Make sure correct active edge is set
                if active['length'] == 0: active['edge'] = self.string[step]
                print "I IS ACTIVE EDGE=", active['edge']

                # If current edge is not found current node
                if active['edge'] not in active['node'].edges:
                    print "Inserting", active['edge'], "at step", step, "to", active['node']
                    # Insert the current char at current node
                    active['node'].setEdge(active['edge'], step, ENDCHAR)
                    # rule 2
                    if nodeNeedSuffixLink is not None:
                        nodeNeedSuffixLink.link = active['node']
                    nodeNeedSuffixLink = active['node']

                # There an outgoing edge from the current node
                else:
                    # The active edge
                    edge = active['node'].edges[active['edge']]
                    # edgeStart + active_length
                    cNextPos = edge.start + active['length'] 

                    # TODO observation 2
                    # If at some point active_length is greater or equal to the 
                    # length of current edge (edge_length), we move our active
                    # point down until edge_length is not strictly greater than
                    # active_length.

                    if active['length'] >= len(edge):
                        active['edge'] = self.string[len(edge) + 

                    # the char is next in the existing edge
                    print c_char, self.string[cNextPos],
                    if self.string[cNextPos] == c_char: # observation 1
                        print "was next"
                        # We set this edge to be the active edge 
                        active['length'] += 1
                        # observation 3
                        if nodeNeedSuffixLink is not None:
                            print "Node -> need suffix", nodeNeedSuffixLink
                            nodeNeedSuffixLink.link = active['node']
                        nodeNeedSuffixLink = active['node']
                        break # Time to go to next character

                    print "was not next"
                    print "Currently active: ", active['edge'], edge
                    # Since the char was not the next, we will split
                    # Overwrite old edge to new split edge 
                    # TODO can this splitting be a cause of problems? Should the old node not be moved? Think about suffix links and how they are moved..
                    print "Transforming", self.string[edge.start:edge.end], "to", self.string[edge.start:edge.start + active['length']]

                    edge.end = edge.start + active['length']

                    edge.node.setEdge(self.string[edge.end], edge.end, ENDCHAR)
                    # new leaf
                    edge.node.setEdge(c_char, step, ENDCHAR)

                    print "the new nodes", edge.node

                    # rule 2
                    if nodeNeedSuffixLink is not None:
                        nodeNeedSuffixLink.link = edge.node
                    #nodeNeedSuffixLink = newEdge.node # the split node
                    nodeNeedSuffixLink = edge.node # the split node

                # We have inserted one char
                remainder -= 1

                #  Rule 1
                if active['node'].isRoot and active['length'] > 0:
                    active['length'] -= 1
                    active['edge'] = self.string[step - remainder + 1] 
                else:
                    #  Rule 3
                    if active['node'].link is not None:
                        active['node'] = active['node'].link
                    else:
                        active['node'] = self.root

    def find_substring(self, substring):
        """
        Returns index of substring or -1 if not found.
        """
        if not substring:
            return -1

        c_node = self.root
        i = 0
        while i < len(substring):
            #print "c_node", c_node
            # Find the edge
            #print i, substring[i]
            #print "the edges", c_node.edges
            if substring[i] not in c_node.edges:
                return -1
            edge = c_node.edges[substring[i]]
            #print "Active edge", edge

            edge_to = min(len(edge) + 1, len(substring))

            #print substring[i:i+edge_to], self.string[edge.start:edge.start+edge_to]
            if substring[i:i+edge_to] != self.string[edge.start:edge.start+edge_to]:
                return -1

            i += len(edge) + 1
            c_node = edge.node

        #print "done"
        return edge.start - len(substring) + edge_to




if __name__ == "__main__":
    #st = SuffixTree("TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG")
    st = SuffixTree("abcabxabcd")
    #st = SuffixTree("abcada")
    print "SEARCH FOR SUBSTRING"
    print st.find_substring("cab")

    from SuffixGrapher import createGraphviz
    createGraphviz(st.root, st.string)
