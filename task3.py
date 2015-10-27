from algorithms.suffixtree.SuffixTree import SuffixTree
from algorithms.suffixtree.SuffixGrapher import Grapher
import matplotlib.pyplot as plt
import Utility
import re

# TODO also process s_3_sequence_1M.txt.gz and Seqset3.txt.gz

filename = "dataset/S_1-1_1M.txt"
#filename = "dataset/S_3_sequence_1M.txt"
suffix_tree = Utility.create_gst_on_file(filename)

#suffix_tree = SuffixTree()
#suffix_tree.add_string("GATCGGAAGAGCACACGTCTGAACTCCAGTCACATCACGAATCTCGTATGCCGTCATCAGATTGAAAAAAAAAACC")
#suffix_tree.add_string("ABABC")
#suffix_tree.add_string("BABCABC")
#suffix_tree.add_string("ABCBABC")
#suffix_tree.add_string("ippississim")
#suffix_tree.add_string("mississippi")

longest_label = ("", [])
longest_most_counts = ("", [])

def countSuffixes(node, label="", suffixes={}):
    """
    Counts all labels up to all leaves and returns a dict on them all
    """
    global longest_label
    global longest_most_counts

    # Process leaves
    if len(node.edges) == 0:
        suffixes[label] = node.suffixes
        if len(label) > len(longest_label[0]):
            longest_label = (label, node.suffixes)

        if node.suffixes > longest_most_counts[1]:
            longest_most_counts = (label, node.suffixes)

    if len(node.edges) > 0:
        for key, child in node.edges.iteritems():
            newLabel = str(label) + suffix_tree.get_internal_subtring(child, child.start, child.end)
            suffixes.update(countSuffixes(child, newLabel, suffixes))

    return suffixes

# Count them suffixes
suffixes = countSuffixes(suffix_tree.root)

# Sort them suffixes
sortedSuffixes = sorted(suffixes.items(), key=lambda x: x[1])

#
# TODO Find most probable adapter sequence
# TODO Are there other common sequences? That can mean problems.
#
for (key, value) in sortedSuffixes:
    #if len(key) < 5 or len(value) < 1000 or key == '$':
    #    continue
    print "{0}: {1}".format(value, key)

print "Longest label -> {0}: {1}".format(longest_label[1], longest_label[0])
print "Longest most counts -> {0}: {1}".format(longest_most_counts[1], longest_most_counts[0])

#
# TODO Find all sequences with that adapter
#

adapter = raw_input("Select adapter sequence:")
lengthCount = {}

regexp = re.compile(r''+adapter+'$')
for string in Utility.generate_strings(filename):#['ABABC', 'BABCABC', 'ABCBABC']: #Utility.generate_strings(filename):
    if regexp.search(string) is not None:
        newString = regexp.sub('', string)

        try:
            lengthCount[len(newString)] += 1
        except KeyError:
            lengthCount[len(newString)] = 1

print "Length count: {0}".format(lengthCount)
# TODO Store length distribution on them
plt.bar(range(len(lengthCount)), lengthCount.values(), align='center')
plt.xticks(range(len(lengthCount)), lengthCount.keys())
plt.xlabel("Length")
plt.ylabel("Count")

plt.show()
plt.savefig("task3.png")

try:
    from IPython import embed
except ImportError:
    print "Install IPython.. doh.. nut"
    exit(1)
embed()
