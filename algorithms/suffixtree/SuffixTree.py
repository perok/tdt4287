from itertools import izip_longest

alphabet = 'ACTG$'

class Node(object):
    """
    Node class that represents parent and children pointers.

    Children dict has edges ((pos, ENDCHAR), Node(self)).

    If start, end, or string_id is None, then the node is root

    """
    # Avoid using dict on class properties
    __slots__ = ['id', 'start', 'end', 'string_id', 'edges', 'link', 'suffixes']

    counter = 0

    def __init__(self, string_id=None, start=None, end=None):
        self.id = Node.counter
        Node.counter += 1

        self.start = start
        self.end = end
        self.string_id = string_id
        self.edges = {} # recordclass with alphabet?
        self.link = None

        self.suffixes = 0

    def setEdge(self, char, string_id, start, end):
        """
        Add one pointing to a new node that is [start, end) on string string_id.
        char -> Node
        Returns the new node.
        """
        self.edges[char] = Node(string_id, start, end)

        return self.edges[char]

    def addSuffix(self, string_id, char):
        self.suffixes += 1
        # append((string_id, char))

    def is_root(self):
        return self.start is None

    def __len__(self):
        """
        Get the lenght the substring for the edge to the node
        """
        return self.end - self.start

    def __repr__(self):
        s =  "N({0}, {1}, {2})".format(self.id, self.is_root(), self.link is not None)
        for key, value in self.edges.iteritems():
            s += "\n\t{0} -> Node(id={1}, start={2}, end={3})".format(
                    key,
                    value.string_id,
                    value.start,
                    value.end)
        return s

class SuffixTree(object):
    """
    Generalized Suffix Tree
    """

    def __init__(self, verbose=False):
        self.active_string = -1
        self.strings = []
        self.root = Node()

        # Triplet for the active state
        self.active_node   = self.root
        self.active_edge   = '\00'
        self.active_length = 0

        # How many new suffixes that need to be inserted.
        self.remainder = 0

        self.nodeNeedSuffixLink = None

        self.verbose = verbose

    def __repr__(self):
        s =  "#" * 5 + " Generalized Suffix Tree state " + "#" * 5
        s+= "\n\tActive node " + str(self.active_node)
        s+= "\n\tActive edge " + str(self.active_edge)
        s+= "\n\tActive length " + str(self.active_length)
        s+= "\n\tRemainder " + str(self.remainder)
        s+= "\n\tNode need suffix link: " + str(self.nodeNeedSuffixLink.id) if self.nodeNeedSuffixLink is not None else "False"
        s+=  "\n" + "#" * 41

        return s

    def get_char(self, pos):
        """
        Gets the a char at pos from active string
        """
        return self.strings[self.active_string][pos]

    def get_char_from_string(self, stringId, pos):
        """
        Gets the a char at pos from given string
        """
        return self.strings[stringId][pos]

    def get_string(self):
        """
        Return the current active string
        """
        return self.strings[self.active_string]

    def walk_down(self, edge):
        """
        If at some point self.active_length is greater or equal to the
        length of current edge (edge_length), we move our active
        point down until edge_length is not strictly greater than
        self.active_length.
        """
        if self.active_length >= len(edge):
            self.active_edge += len(edge)
            self.active_length -= len(edge)
            self.active_node = edge
            return True
        return False

    def set_suffix_link(self, node):
        if self.nodeNeedSuffixLink is not None:
            self.nodeNeedSuffixLink.link = node
        self.nodeNeedSuffixLink = node

    def add_string(self, string, prefix_char='', suffix_char='$'):
        """
        Build suffix tree with Ukkonen's algoritm.
        """
        self.active_string += 1
        self.strings.append("{0}{1}{2}".format(prefix_char, string, suffix_char))

        start = 0

        ENDCHAR = len(self.get_string())# - 1
        #print ENDCHAR
        #for i in xrange(len(self.get_string())):
        #    print i, self.get_char(i),
        #print '\n'
        #if self.active_string > 0 and False:
        #    start = self._find_first_mistmatch(self.get_string())
        #    if self.verbose: print "\tNew string starting on pos:", start,"which is char:", self.get_char(start)

        #    # Entire string is encoded
        #    if start <= 0:
        #        if self.verbose: print string, "is allready encoded"
        #        return

        if self.verbose: print self

        active_node = self.root
        active_edge = '\00'
        active_length = 0

        self.remainder = 0

        # Iterate over all steps in input string.
        # From pos 0 to pos len(string) - 1
        # Step is position in string
        # todo this can be made to a addChar method? Step is obviously not needed
        for step in xrange(start, len(self.get_string())):
            c_char = self.get_char(step)

            # How many new suffixes that need to be inserted.
            # Set to one at the beginning of each step

            self.remainder += 1

            self.nodeNeedSuffixLink = None

            # Work through all self.remainders for each character
            while self.remainder > 0:
                # Make sure correct active edge is set
                if self.active_length == 0: self.active_edge = step

                if self.verbose: print "\tStep {0}: New while. self.remainder is {1} active node is {2}".format(step, self.remainder,self.active_node)

                # If current edge is not found current node
                try:
                    balle = self.get_char(self.active_edge)
                except IndexError:
                    print "IndexError aka fml"
                    print self.active_string
                    print self.active_edge
                    print self.get_string(), len(self.get_string())
                    print self

                if self.get_char(self.active_edge) not in self.active_node.edges:
                    if self.verbose: print "\tActive edge", self.get_char(self.active_edge), "not in active node"
                    # Insert the current char at current node
                    newLeaf = self.active_node.setEdge(
                            self.get_char(self.active_edge),
                            self.active_string,
                            step,
                            ENDCHAR)
                    newLeaf.addSuffix(self.active_string, step - self.remainder - 1)

                    # rule 2
                    self.set_suffix_link(self.active_node)

                # There an outgoing edge from the current node
                else:
                    # Jump forward
                    # TODO wierd bug, must be removed if string is stripped.
                    if self.active_node.is_root():
                        self.active_edge = step - self.remainder + 1 # testing
                        self.active_length = self.remainder - 1 # testing

                    # The active node
                    edge = self.active_node.edges[self.get_char(self.active_edge)]

                    if self.walk_down(edge):
                        continue

                    # the char is next in the existing edge
                    # observation 1
                    if self.get_char_from_string(edge.string_id, edge.start + self.active_length) == c_char:
                        if self.verbose: print "\tObs 1:", c_char, "in edge"

                        if c_char == '$':
                            # We ended on a suffix
                            edge.addSuffix(self.active_string, step - self.remainder - 1)
                        else:
                            # We set this edge to be the active edge
                            self.active_length += 1
                            # observation 3
                            self.set_suffix_link(self.active_node)
                            break # Time to go to next character
                    else:
                        # Since the char was not the next, we will split

                        # Overwrite old edge with new split
                        # Once a leaf, always a leaf
                        splitEdge = self.active_node.setEdge(
                                self.get_char(self.active_edge),
                                edge.string_id,
                                edge.start,
                                edge.start + self.active_length) #-1 testings

                        # Insert the new char
                        newLeaf = splitEdge.setEdge(
                                c_char,
                                self.active_string,
                                step,
                                ENDCHAR)
                        newLeaf.addSuffix(self.active_string, step - self.remainder - 1)

                        # Old edge start a bit further now
                        edge.start += self.active_length
                        #edge.string_id = self.active_string

                        # Insert the old edge to the new split edge
                        splitEdge.edges[self.get_char_from_string(edge.string_id, edge.start)] = edge

                        # rule 2
                        self.set_suffix_link(splitEdge)

                # We have inserted one char
                self.remainder -= 1

                #  Rule 1
                if self.active_node.is_root() and self.active_length > 0:
                    self.active_length -= 1
                    self.active_edge = step - self.remainder + 1
                else:
                    #  Rule 3
                    if self.active_node.link is not None:
                        self.active_node = self.active_node.link
                    else:
                        self.active_node = self.root

    def get_internal_subtring(self, node, start, end):
        """
        Gets the internal substring from a node in a given range.
        """
        return self.strings[node.string_id][start:end]

    def _find_first_mistmatch(self, substring):
        """
        Returns index of substring or -1 if not found.

        Will changes the internal active point state.
        """
        if not substring:
            return -1, None

        self.active_node = self.root
        i = 0
        while i < len(substring):
            if self.verbose: print "Current", i, self.active_node
            self.active_length = i
            self.active_edge = i

            # Explicit mismatch
            if substring[i] not in self.active_node.edges:
                if self.verbose: print "Explicit mismatch"
                return i + 1

            node = self.active_node.edges[substring[self.active_edge]]

            node_to = min(len(node), len(substring) - i)

            s1 = substring[i:i+node_to]
            s2 = self.get_internal_subtring(node, node.start, node.start+node_to)

            # Implicit mismatch
            if s1 != s2:
                longest = _find_string_first_mismatch(s1, s2)
                self.active_length += longest
                return i + longest + 1

            i += len(node)
            self.active_node = node

        # Entire string matches, return -1
        return -1

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

            s1 = substring[i:i+edge_to]
            s2 = self.get_internal_subtring(edge, edge.start, edge.start+edge_to)
            if s1 != s2:
                return -1

            i += len(edge)
            c_node = edge

        return edge.start - len(substring) + edge_to

    def hamming_distance(self, s1, s2):
        """
        Return the Hamming distance between equal-length sequences
        """
        if len(s1) != len(s2):
            raise ValueError("Undefined for sequences of unequal length")
        return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))

    def find_prefixmatch(self, current_substring, node, error_limit, current_match = "", longest_match = ""):
        string = current_substring
        for edge in node.edges:
            child_node = node.edges[edge]
            edge_substring = self.get_internal_subtring(child_node, child_node.start, child_node.end)
            #Logic if leaf node
            if edge_substring[-1] == "$":
                without_endchar = edge_substring[:-1]
                string_substring = string[:len(without_endchar)]
                if len(without_endchar) == len(string_substring):
                    substring_error = self.hamming_distance(string_substring, without_endchar)
                    match = current_match+string_substring
                    if substring_error <= error_limit and len(match) > len(longest_match):
                        longest_match = match

            #Logic if an internal node
            else:
                string_substring = string[:len(edge_substring)]
                substring_error = self.hamming_distance(string_substring, edge_substring)

                if substring_error > error_limit:
                    continue
                else:
                    new_error_limit = error_limit-substring_error
                    new_current_match = current_match + string_substring
                    new_current_substring = string[len(edge_substring):]
                    match = self.find_prefixmatch(new_current_substring, child_node, new_error_limit, new_current_match, longest_match)
                    if len(match) > len(longest_match):
                        longest_match = match

        return longest_match

def _find_string_first_mismatch(s1, s2):
    """
    Returns position of first mismatch between s1 and s2.
    """
    return sum(c1!=c2 for c1,c2 in izip_longest(s1,s2))

def cmd_line_main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Suffix Tree creator",
        epilog="Tips:\nabcabxabcd\ncdddcdc\nTGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG")

    parser.add_argument("strings", nargs='+', help="Make Suffix tree on these strings")
    parser.add_argument("-s", "--search", help="Keyword to search for")
    parser.add_argument("-p", "--gprint", help="Print graphviz file", action="store_true")
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    parser.add_argument("-i", "--interactive", help="Start interactive", action="store_true")
    args = parser.parse_args()

    st = SuffixTree(verbose=args.verbose)

    for string in args.strings:
        st.add_string(string)

    if args.verbose: print "ST build complete."
    if args.verbose: print st

    if args.search:
        if args.verbose: print "Search for", args.search, "found on pos:",
        print st.find_substring(args.search)

    if args.gprint:
        from SuffixGrapher import Grapher
        g = Grapher(st)
        g.createGraphviz()

    if args.interactive:
        try:
            from IPython import embed
        except ImportError:
            print "Install IPython.. doh.. nut"
            exit(1)
        embed()

if __name__ == "__main__":
    cmd_line_main()
