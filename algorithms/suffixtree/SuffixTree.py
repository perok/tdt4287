import os
ENDCHAR = '#'

class Node(object):
    """
    Node class that represents parent and children pointers.

    Children dict has edges ((pos, ENDCHAR), Node(self)).

    No parent means that it is the root node.
    """

    def __init__(self, isRoot=False):
        self.isRoot = isRoot 
        self.edges = {}
        self.link = None

    def setEdge(self, char, fr, to):
        """ 
        Add one edge to node.
        Edge is representent with tuple (start, end, ->Node)
        char -> (from, to, node)
        """
        node = Node(self)
        self.edges[char] = [fr, to, node]

    # TODO make edge a class
 #@property
 #   def length(self):
 #       return self.last_char_index - self.first_char_index

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
        activePoint = [self.root, '\00', 0]

        # Value for where the end char is
        endChar = 0

        # How many new suffixes that need to be inserted. 
        # Set to one at the beginning of each step
        remainder = 1 

        # Iterate over all steps in input string.
        # From pos 0 to pos len(string) - 1
        # Step is position in string
        # todo this can be made to a addChar method? Step is obviously not needed
        for step in xrange(len(self.string)):

            cChar = self.string[step] 

            # How many new suffixes that need to be inserted. 
            # Set to one at the beginning of each step
            remainder += 1 

            # Update # so that current char is included in the other nodes
            endChar += 1 # TODO this is step?

            nodeNeedSuffixLink = None


            # Work through all remainders for each character
            while remainder > 0:
                # Make sure correct active edge is set
                if activePoint[2] is 0: activePoint[1] = self.string[step]

                # Char not found in current nodes outgoing edges 
                if cChar not in activePoint[0].edges:
                    # Insert the current char at current node
                    activePoint[0].setEdge(cChar, step, ENDCHAR)
                    # rule 2
                    if nodeNeedSuffixLink is not None:
                        nodeNeedSuffixLink.link = activePoint[0]
                    nodeNeedSuffixLink = activePoint[0]

                # There an outgoing edge from the current node
                else:
                    edge = activePoint[0].edges[activePoint[1]] # The active edge
                    cNextPos = edge[0] + activePoint[2] # edgeStart + active_length

                    # TODO observation 2

                    # the char is next in the existing edge
                    if cChar == self.string[cNextPos]: # observation 1
                        # We set this edge to be the active edge 
                        activePoint[2] += 1
                        # observation 3
                        if nodeNeedSuffixLink is not None:
                            nodeNeedSuffixLink.link = activePoint[0]
                        nodeNeedSuffixLink = activePoint[0]
                        break # Time to go to next character

                    # Since the char was not the next, we will split
                    # Overwrite old edge to new split edge 
                    # TODO can this splitting be a cause of problems? Should the old node not be moved? Think about suffix links and how they are moved..
                    activePoint[0].setEdge(activePoint[1], edge[0], edge[1])
                    newEdge = activePoint[0].edges[activePoint[1]]

                    # update old edge to start + active_length
                    edge[0] += activePoint[2]

                    # Add edge with new char
                    newEdge[2].setEdge(self.string[cNextPos], step, ENDCHAR)
                    # Add old edge
                    newEdge[2].edges[self.string[edge[0]]] = edge

                    # rule 2
                    if nodeNeedSuffixLink is not None:
                        nodeNeedSuffixLink.link = activePoint[0]
                    nodeNeedSuffixLink = newEdge[2] # the split node

                # We have inserted one char
                remainder -= 1

                #  Rule 1
                if activePoint[0].isRoot and activePoint[2] > 0:
                    activePoint[2] -= 1
                    activePoint[1] = self.string[step - remainder + 1] 
                else:
                    #  Rule 3
                    if activePoint[0].link is not None:
                        activePoint[0] = activePoint[0].link
                    else:
                        activePoint[0] = self.root

    def find_substring(self, substring):
        """
        Returns index of substring or -1 if not found.
        """
        if not substring:
            return -1

        c_node = self.root
        i = 0
        while i < len(substring):
            # Find the edge
            if substring[i] not in c_node.edges:
                return -1
            edge = c_node.edges[substring[i]]
            print "edges", c_node.edges
            print "edge", edge
            edge_to = min(edge[1] - edge[0] + 1, len(substring) - 1)

            if substring[i:edge_to] is not self.string[edge[0]:edge[0] + edge_to]:
                return -1

            i += edge[1] - edge[0] + 1
            c_node = edge[2]
        return edge[0] - len(substring) + edge_to




if __name__ == "__main__":
    st = SuffixTree("TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG")
    st = SuffixTree("aaab")
    print st.find_substring("a")
