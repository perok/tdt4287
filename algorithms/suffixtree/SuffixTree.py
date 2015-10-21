
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
        self.edges[char] = Edge(fr, to, node)

        return self.edges[char]

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

        # (active_node, active_edge, active_length)
        active = {
            'node'  : self.root,
            'edge'  : '\00',
            'length': 0
        }

        # How many new suffixes that need to be inserted. 
        # Set to one at the beginning of each step
        remainder = 0

        ENDCHAR = len(self.string)

        # Iterate over all steps in input string.
        # From pos 0 to pos len(string) - 1
        # Step is position in string
        # todo this can be made to a addChar method? Step is obviously not needed
        for step in xrange(len(self.string)):
            c_char = self.string[step] 

            # How many new suffixes that need to be inserted. 
            # Set to one at the beginning of each step
            remainder += 1 

            nodeNeedSuffixLink = None

            # Work through all remainders for each character
            while remainder > 0:
                # Make sure correct active edge is set
                if active['length'] == 0: active['edge'] = step

                # If current edge is not found current node
                if self.string[active['edge']] not in active['node'].edges:
                    # Insert the current char at current node
                    active['node'].setEdge(self.string[active['edge']], step, ENDCHAR)
                    # rule 2
                    if nodeNeedSuffixLink is not None and not nodeNeedSuffixLink.isRoot:
                        nodeNeedSuffixLink.link = active['node']
                    nodeNeedSuffixLink = active['node']

                # There an outgoing edge from the current node
                else:
                    # The active edge node
                    edge = active['node'].edges[self.string[active['edge']]]

                    # If at some point active_length is greater or equal to the 
                    # length of current edge (edge_length), we move our active
                    # point down until edge_length is not strictly greater than
                    # active_length.
                    if active['length'] >= len(edge):
                        active['edge'] += len(edge)
                        active['length'] -= len(edge)
                        active['node'] = edge.node
                        continue

                    # the char is next in the existing edge
                    if self.string[edge.start + active['length']] == c_char: # observation 1
                        # We set this edge to be the active edge 
                        active['length'] += 1
                        # observation 3
                        if nodeNeedSuffixLink is not None and not nodeNeedSuffixLink.isRoot:
                            nodeNeedSuffixLink.link = active['node']
                        nodeNeedSuffixLink = active['node']
                        break # Time to go to next character

                    # Since the char was not the next, we will split

                    # Overwrite old edge with new split
                    splitEdge = active['node'].setEdge(
                            self.string[active['edge']], 
                            edge.start, 
                            edge.start + active['length'])

                    # Insert the new char
                    splitEdge.node.setEdge(c_char, step, ENDCHAR)

                    # Old edge start a bit further now
                    edge.start += active['length']

                    # Insert the old edge to the new split edge
                    splitEdge.node.edges[self.string[edge.start]] = edge

                    # rule 2
                    if nodeNeedSuffixLink is not None and not nodeNeedSuffixLink.isRoot:
                        nodeNeedSuffixLink.link = splitEdge.node
                    nodeNeedSuffixLink = splitEdge.node

                # We have inserted one char
                remainder -= 1

                #  Rule 1
                if active['node'].isRoot and active['length'] > 0:
                    active['length'] -= 1
                    active['edge'] = step - remainder + 1
                else:
                    #  Rule 3
                    if active['node'].link is not None and not active['node'].link.isRoot:
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
            if substring[i] not in c_node.edges:
                return -1
            edge = c_node.edges[substring[i]]

            edge_to = min(len(edge), len(substring) - i)

            if substring[i:i+edge_to] != self.string[edge.start:edge.start+edge_to]:
                return -1

            i += len(edge)
            c_node = edge.node

        return edge.start - len(substring) + edge_to


if __name__ == "__main__":
    st = SuffixTree("TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG")
    print st.find_substring("CTCC")

    from SuffixGrapher import createGraphviz
    createGraphviz(st.root, st.string)

