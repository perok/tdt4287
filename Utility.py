#!/usr/bin/env python
# -*- coding: utf-8 -*-

from algorithms.suffixtree.SuffixTree import SuffixTree
from algorithms.suffixtree.SuffixGrapher import Grapher

from contextlib import contextmanager
from timeit import default_timer
from timeit import timeit

from Queue import Queue

@contextmanager
def elapsed_timer():
    """
    Timer from http://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python
    """
    start = default_timer()
    elapser = lambda: default_timer() - start
    yield lambda: elapser()
    end = default_timer()
    elapser = lambda: end-start

def create_gst_on_file(filename, gprint=False, strip=False):
    """
    Opens a file and create a suffix tree on every string
    """
    st = SuffixTree()

    print "Opening file \"{0}\".".format(filename)
    time_start = default_timer()

    with open(filename) as text_file:
        i = -1
        for line in text_file:
            st.add_string(line.strip() if strip else line)#.strip())#.strip())
            i += 1

            if i % 100000 == 0:
                print "\tProcessed {0} elements".format(i)

    if gprint:
        g = Grapher(st)
        g.createGraphviz()

    print "Suffix tree for \"{0}\" complete in {1} seconds".format(filename, default_timer() - time_start)

    return st

def generate_strings(filename):
    """
    Generator for each string seperated by "\n" in filename.
    """
    st = SuffixTree()

    with open(filename) as text_file:
        for line in text_file:
            yield line.strip()

def count_and_show_suffixes(suffix_tree):
    queue = Queue()
    queue.put((suffix_tree.root, ""))

    suffixes = {}

    while not queue.empty():
        cNode, label = queue.get()

        if len(cNode.edges) == 0:
            if len(label) < 20 or cNode.suffixes < 1000 or label == '$':
                continue

            suffixes[label] = cNode.suffixes

        for key, nNode in cNode.edges.iteritems():
            #print nNode.suffixes_visited_by
            newLabel = str(label) + suffix_tree.get_internal_subtring(nNode, nNode.start, nNode.end)
            queue.put((nNode, newLabel))


    # Sort them suffixes
    sortedSuffixes = sorted(suffixes.items(), key=lambda x: int(x[1]))

    for (label, value) in sortedSuffixes:
        l = label.replace('\n', '')
        print "{0}:\t{2}\t{1}".format(value, l, len(l))

def plot_graph_from_length_distribution(length_distribution, name=False):
    import matplotlib.pyplot as plt

    plt.bar(range(len(length_distribution)), length_distribution.values(), align='center')
    plt.xticks(range(len(length_distribution)), length_distribution.keys())
    plt.xlabel("Length")
    plt.ylabel("Count")

    plt.show()

    if name:
        plt.savefig(name)

def csv_distribution(distribution, name="distribution.csv"):
    import csv

    with open(name, 'wb') as d_file:
        wr = csv.writer(d_file, delimiter=',', quoting=csv.QUOTE_ALL)
        wr.writerow(['length', 'count'])
        for length, count in distribution.iteritems():
            wr.writerow([length, count])


def length_distribution_on_suffix(filename, adaptersequence):
    st = SuffixTree()
    number_of_matches = 0
    length_distribution = {}

    #Reverse adaptersequence to create prefixtree
    reversed_adaptersequence = adaptersequence[::-1]
    st.add_string(reversed_adaptersequence)

    #Loop through the sequences in the file
    for line in generate_strings(filename):
        reversed_line = line[::-1]
        #Get longest suffix-prefix match for given string
        longest_match = st.find_prefixmatch_nr(reversed_line, st.root, 0.0)
        #Check number of matches
        length_match = len(longest_match)
        if length_match > 0:
            number_of_matches += 1
        length_rest = len(line) - length_match
        if length_rest in length_distribution:
            length_distribution[length_rest] += 1
        else:
            length_distribution[length_rest] = 1

    return number_of_matches, length_distribution
