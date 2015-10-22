
class Node(object):
    """
    Node class that represents parent and children pointers.

    Children dict has edges ((pos, ENDCHAR), Node(self)).

    If start, end, or string_id is None, then the node is root

    """
    counter = 0
    def __init__(self, string_id=None, start=None, end=None):
        self.id = Node.counter
        Node.counter += 1

        self.start = start
        self.end = end
        self.string_id = string_id
        self.edges = {}
        self.link = None

    def setEdge(self, char, string_id, start, end):
        """
        Add one pointing to a new node that is [start, end) on string string_id.
        char -> Node
        Returns the new node.
        """
        self.edges[char] = Node(string_id, start, end)

        return self.edges[char]

    def is_root(self):
        return self.start is None

    def __len__(self):
        """
        Get the lenght the substring for the edge to the node
        """
        return self.end - self.start 

    def __repr__(self):
        s =  "N({0}, {1}, {2})\n".format(self.id, self.is_root, self.link is not None)
        for key, value in self.edges.iteritems():
            s += "\t{0} -> Node(id={1}, start={2}, end={3}\n".format(
                    key, 
                    value.string_id, 
                    value.start, 
                    value.end)
        return s

class SuffixTree(object):
    """
    Generalized Suffix Tree
    """

    def __init__(self):
        self.active_string = -1
        self.strings = {}
        self.root = Node()

    def get_char(self, pos):
        """
        Gets the a char at pos from active string
        """
        return self.strings[self.active_string][pos]

    def get_string(self):
        """
        Return the current active string
        """
        return self.strings[self.active_string]

    def add_string(self, string):
        """
        Build suffix tree with Ukkonen's algoritm.
        """
        self.active_string += 1
        self.strings[self.active_string] = string

        # Triplet for the active state
        active_node   = self.root
        active_edge   = '\00'
        active_length = 0

        # How many new suffixes that need to be inserted. 
        remainder = 0

        ENDCHAR = len(self.get_string())

        # Iterate over all steps in input string.
        # From pos 0 to pos len(string) - 1
        # Step is position in string
        # todo this can be made to a addChar method? Step is obviously not needed
        for step in xrange(len(self.get_string())):
            c_char = self.get_char(step)

            # How many new suffixes that need to be inserted. 
            # Set to one at the beginning of each step
            remainder += 1 

            nodeNeedSuffixLink = None

            # Work through all remainders for each character
            while remainder > 0:
                # Make sure correct active edge is set
                if active_length == 0: active_edge = step

                # If current edge is not found current node
                if self.get_char(active_edge) not in active_node.edges:
                    # Insert the current char at current node
                    active_node.setEdge(
                            self.get_char(active_edge),
                            self.active_string,
                            step,
                            ENDCHAR)

                    # rule 2
                    if nodeNeedSuffixLink is not None and not nodeNeedSuffixLink.is_root():
                        nodeNeedSuffixLink.link = active_node
                    nodeNeedSuffixLink = active_node

                # There an outgoing edge from the current node
                else:
                    # The active node
                    edge = active_node.edges[self.get_char(active_edge)]

                    # If at some point active_length is greater or equal to the 
                    # length of current edge (edge_length), we move our active
                    # point down until edge_length is not strictly greater than
                    # active_length.
                    if active_length >= len(edge):
                        active_edge += len(edge)
                        active_length -= len(edge)
                        active_node = edge
                        continue

                    # the char is next in the existing edge
                    if self.get_char(edge.start + active_length) == c_char: # observation 1
                        # We set this edge to be the active edge 
                        active_length += 1
                        # observation 3
                        if nodeNeedSuffixLink is not None and not nodeNeedSuffixLink.is_root():
                            nodeNeedSuffixLink.link = active_node
                        nodeNeedSuffixLink = active_node
                        break # Time to go to next character

                    # Since the char was not the next, we will split

                    # Overwrite old edge with new split
                    splitEdge = active_node.setEdge(
                            self.get_char(active_edge),
                            self.active_string,
                            edge.start, 
                            edge.start + active_length)

                    # Insert the new char
                    splitEdge.setEdge(
                            c_char,
                            self.active_string,
                            step,
                            ENDCHAR)

                    # Old edge start a bit further now
                    edge.start += active_length

                    # Insert the old edge to the new split edge
                    splitEdge.edges[self.get_char(edge.start)] = edge

                    # rule 2
                    if nodeNeedSuffixLink is not None and not nodeNeedSuffixLink.is_root():
                        nodeNeedSuffixLink.link = splitEdge
                    nodeNeedSuffixLink = splitEdge

                # We have inserted one char
                remainder -= 1

                #  Rule 1
                if active_node.is_root and active_length > 0:
                    active_length -= 1
                    active_edge = step - remainder + 1
                else:
                    #  Rule 3
                    if active_node.link is not None and not active_node.link.is_root:
                        active_node = active_node.link
                    else:
                        active_node = self.root

    def get_internal_subtring(self, node, start, end):
        """
        Gets the internal substring from a node in a given range.
        """
        return self.strings[node.string_id][start:end]

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

            if substring[i:i+edge_to] != self.get_internal_subtring(edge, edge.start, edge.start+edge_to):
                return -1

            i += len(edge)
            c_node = edge

        return edge.start - len(substring) + edge_to


def cmd_line_main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Suffix Tree creator",
        epilog="Tips:\nabcabxabcd\ncdddcdc\nTGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG")

    parser.add_argument("string", help="Make Suffix tree on this string")
    parser.add_argument("search", help="Keyword to search for")
    parser.add_argument("--gprint", help="Print graphviz file", action="store_true")
    args = parser.parse_args()

    st = SuffixTree()
    st.add_string(args.string)
    print st.find_substring(args.search)

    if args.gprint:
        from SuffixGrapher import Grapher
        g = Grapher(st)
        g.createGraphviz()

if __name__ == "__main__":
    cmd_line_main()

