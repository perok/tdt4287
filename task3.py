#!/usr/bin/env python
# -*- coding: utf-8 -*-

from algorithms.suffixtree.SuffixTree import SuffixTree
from algorithms.suffixtree.SuffixGrapher import Grapher
#import matplotlib.pyplot as plt
import Utility

# TODO also process s_3_sequence_1M.txt.gz and Seqset3.txt.gz

filename = "dataset/S_1-1_1M.txt"
#filename = "dataset/S_3_sequence_1M.txt"

#from guppy import hpy
#h = hpy()
#h.setref()
suffix_tree = Utility.create_gst_on_file(filename)
#print h.heap()
#raw_input()

#suffix_tree = SuffixTree()
#suffix_tree.add_string("GATCGGAAGAGCACACGTCTGAACTCCAGTCACATCACGAATCTCGTATGCCGTCATCAGATTGAAAAAAAAAACC")
# suffix_tree.add_string("ABABC")
# suffix_tree.add_string("BABCABC")
# suffix_tree.add_string("ABCBABC")
#suffix_tree.add_string("ippississim")
#suffix_tree.add_string("mississippi")

#
# TODO Find most probable adapter sequence
# TODO Are there other common sequences? That can mean problems.
#
Utility.count_and_show_suffixes(suffix_tree)

#
# TODO Find all sequences with that adapter
#

adapter = raw_input("Select adapter sequence (type \'exit\' for.. exit):\n")
lengthCount = {}
lengthCount = Utility.length_distribution_on_suffix(filename, adapter)
print "Created length count. Time to show it"
print lengthCount

#
# TODO Store length distribution on them
#

#Utility.create_graph_from_length_distribution(lengthCount, name="task3.png")

try:
    from IPython import embed
except ImportError:
    print "Install IPython.. doh.. nut"
    exit(1)
embed()
